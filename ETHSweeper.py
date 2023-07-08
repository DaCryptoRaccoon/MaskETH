import os
import sys
import glob
import csv
import requests
import cmd
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import numpy as np
import time

class EthSweepCmd(cmd.Cmd):
    intro = '''
    :::::::::: ::::::::::: :::    ::: ::::    ::::      :::      ::::::::  :::    ::: 
    :+:            :+:     :+:    :+: +:+:+: :+:+:+   :+: :+:   :+:    :+: :+:   :+:  
    +:+            +:+     +:+    +:+ +:+ +:+:+ +:+  +:+   +:+  +:+        +:+  +:+   
    +#++:++#       +#+     +#++:++#++ +#+  +:+  +#+ +#++:++#++: +#++:++#++ +#++:++    
    +#+            +#+     +#+    +#+ +#+       +#+ +#+     +#+        +#+ +#+  +#+   
    #+#            #+#     #+#    #+# #+#       #+# #+#     #+# #+#    #+# #+#   #+#  
    ##########     ###     ###    ### ###       ### ###     ###  ########  ###    ### Sweeper v1.0
    ----------------------------------------------------------------------------------------------
    Donations ETH: 0xE2f739D09e372a627c563C642321e51b9E64BcB3
    Donations BTC: 19Qz2mid5CsGQ49Zztrt8k2NhGGUMT1S8L
    Donations LTC: LTGNf2ANWQGZCXmu5NPACUhtCgNHHWCZVs
    ----------------------------------------------------------------------------------------------

    Welcome to ETHMask Sweeper!

    This script automates the process of sweeping (collecting) small amounts of Ethereum (ETH) from a large number of addresses into a single "master" address.
    
    How does it work?
    The script reads from a CSV file that contains Ethereum addresses and their private keys. 
    It checks each address's balance, and if the balance is sufficient to cover the gas fee for a transaction.
    It sends the balance (minus the gas fee) to the master address.
    
    The gas price is fetched from the Ethereum network at the time of each transaction, so it always uses the current gas price.
    
    Here's a quick guide on how to use it:

    sweep: This command sweeps the ETH from all addresses listed in a specified CSV file and sends them to a specified master address.
    For example, 'sweep' will prompt you for the master address and the number of the CSV file you wish to use, and then begin the sweep operation.

    For more information about a command, type 'help <command>'.
    For example, 'help sweep' will display more information about the 'sweep' command.
    '''
    prompt = '(ethsweeper) '

    def do_sweep(self, arg):
        'Sweep all accounts in a given CSV file to a master address: SWEEP'
        load_dotenv()

        # Connect to the testnet
        w3 = Web3(Web3.HTTPProvider(f'https://sepolia.infura.io/v3/{os.getenv("INFURA_API_KEY")}'))

        # Etherscan API key
        etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')

        # Get ETH to USD conversion rate
        response = requests.get(f'https://api.etherscan.io/api?module=stats&action=ethprice&apikey={etherscan_api_key}')
        eth_to_usd_rate = float(response.json()['result']['ethusd'])

        # Master output address
        master_address = input("Please enter your master output address DOUBLE CHECK FUNDS WILL BE SENT HERE!!!: ")

        # List all CSV files in the current directory
        csv_files = glob.glob('./Accounts/*.csv')

        # Print out all CSV files and their corresponding indices
        for i, filename in enumerate(csv_files):
            print(f"{i+1}. {filename}")

        # Ask the user to select a CSV file
        selected_file_index = int(input("Select a CSV file by entering its number: ")) - 1
        selected_file = csv_files[selected_file_index]

        print(f"You selected {selected_file}")

        # Read the selected CSV file
        with open(selected_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header

            total_eth = 0
            transactions = []

            for row in reader:
                address, private_key = row
                account = Account.from_key(private_key)

                # The amount to send is the current account's balance, minus enough to cover gas
                balance = w3.eth.get_balance(account.address)
                gas_price = w3.eth.gas_price
                gas = 21000
                amount = balance - (gas_price * gas)

                if amount > 0:
                    # Construct a transaction
                    transaction = {
                        'to': master_address,
                        'value': amount,
                        'gas': gas,
                        'gasPrice': gas_price,
                        'nonce': w3.eth.get_transaction_count(account.address),
                    }

                    # Sign the transaction with the current account's private key
                    signed_transaction = w3.eth.account.sign_transaction(transaction, account.key)

                    # Send the transaction
                    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

                    # Convert Wei to ETH
                    amount_eth = w3.from_wei(amount, 'ether')
                    total_eth += amount_eth

                    # Calculate the amount in USD
                    amount_usd = float(amount_eth) * eth_to_usd_rate

                    print(f'Sent {amount_eth} ETH (${amount_usd}) from {account.address} to {master_address} in transaction {tx_hash.hex()}')

                    # Append to transactions list
                    transactions.append([account.address, master_address, amount_eth, amount_usd, tx_hash.hex()])

                else:
                    print(f'Not enough balance in {account.address} to cover gas for transfer')

            print(f'Total ETH sent: {total_eth} (${float(total_eth) * eth_to_usd_rate})')

            # Ask the user if they want to save a receipt
            save_receipt = input('Do you want to save a receipt? (Y/n): ')
            if save_receipt.lower() != 'n':
                # Get the current date and time
                current_time = time.strftime("%Y%m%d_%H%M%S")

                # Create Receipt directory if it doesn't exist
                os.makedirs('Receipt', exist_ok=True)

                # Write transactions to CSV
                with open(f'Receipt/Receipt_Payments_{current_time}.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['From Address', 'To Address', 'Amount (ETH)', 'Amount (USD)', 'Transaction Hash'])
                    writer.writerows(transactions)

                print('Receipt saved successfully!')

    def do_exit(self, arg):
        'Exit the shell: EXIT'
        return True

if __name__ == '__main__':
    EthSweepCmd().cmdloop()
