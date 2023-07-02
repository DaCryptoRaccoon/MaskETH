# ETHMask An Ethereum Transaction Mixing Tool

ETHMask is a command-line interface (CLI) tool for mixing Ethereum transactions.

## Overview

ETHMask provides a simple and secure way to mix Ethereum transactions, allowing users to enhance their transaction privacy. It generates new Ethereum accounts and sends transactions to those accounts, making it difficult to trace the original sender.

## Features

- Create new Ethereum accounts securely
- Send transactions to the generated accounts
- Customizable transaction amount based on percentage or custom value
- Integration with Infura for RPC endpoint
- Support for proxy configuration
- Consolidation script to further enhance privacy

## Prerequisites

Before using ETHMask, make sure you have the following:

- Python 3.7 or higher installed
- Ethereum wallet addresses and their corresponding private keys stored in a CSV file
- Infura API key (sign up at [https://infura.io/](https://infura.io/))
- Etherscan API key (sign up at [https://etherscan.io/](https://etherscan.io/))

## Installation

1. Clone the ETHMask repository:

git clone https://github.com/your-username/ETHMask.git

Change into the project directory:

cd ETHMask

Install the required Python packages:

pip install -r requirements.txt

Create a .env file and add the following variables:

PRIVATE_KEY=<your-private-key>
MY_ADDRESS=<your-wallet-address>
INFURA_API_KEY=<your-infura-api-key>
ETHERSCAN_API_KEY=<your-etherscan-api-key>

Run ETHMask:

python ETHMask.py

Follow the prompts to execute the desired commands:
rpc <RPC_endpoint>: Set the RPC endpoint for Ethereum network connection.
proxy <Proxy_URL>: Set the Proxy URL for network connection (optional).
new_accounts <number>: Generate a specified number of new Ethereum accounts.
send_transactions: Send transactions to the generated accounts.

Examples

Generate 100 new Ethereum accounts:
new_accounts 100

Send transactions to the accounts:
send_transactions

# ETHSweeper After Stage 1

ETHSweeper is a script that automates the process of sweeping small amounts of Ethereum.
(ETH) from multiple addresses into a single "master" address.

## Overview

ETHSweeper reads from a CSV file containing Ethereum addresses and their private keys. It checks the balance of each address and, if the balance is sufficient to cover the gas fee for a transaction, it sends the balance (minus the gas fee) to the master address specified by the user.

The gas price is fetched from the Ethereum network at the time of each transaction, ensuring that the script always uses the current gas price.

## Features

- Sweep ETH from multiple addresses to a master address
- Dynamic gas price retrieval
- Support for multiple CSV files
- Calculation of ETH to USD conversion rate

How to Use:

The ETH Sweeper requires the same env file as ETHMixer.

Start the Ethereum Sweeper by running the script with a Python interpreter. The CLI will provide you with the following commands:

sweep: Sweeps all the Ethereum from addresses listed in a selected CSV file into a single "master" address.

exit: Exits the program.

## How It Works:
The sweep command prompts you for the master address, lists all CSV files in the ./Accounts directory, and asks you to select one. For each address, the command checks the balance. If it is sufficient to cover the gas fee, the command sends the balance (minus the gas fee) to the master address.

## Additional Information:
The Ethereum Sweeper is designed to run on Ethereum's Sepolia Testnet. Change the HTTP Provider URL in the Web3.HTTPProvider function if you want to use it on the Ethereum Mainnet or a different testnet.

Be cautious when entering the "master" Ethereum address as all the ETH from the other addresses will be transferred to it. Always double-check addresses before transferring funds and ensure that you never share your private keys.

## License
This project is licensed under the MIT License.

## Disclaimer

**ETHMask is experimental software, provided as-is and without any warranty. Use it at your own risk.**

ETHMask is an experimental script developed for educational and informational purposes only. It is not intended for use in production environments, and its use in real-world scenarios may carry inherent risks.

By using ETHMask, you acknowledge and accept all risks associated with its use. This includes, but is not limited to, the potential loss of funds, incorrect transactions, and security vulnerabilities.

The developers and contributors of ETHSweeper cannot be held responsible for any damages, losses, or liabilities incurred while using this software. It is your responsibility to thoroughly understand the script's functionality, review and validate the code, and take appropriate precautions to ensure the security of your private keys and funds.

Always exercise caution and use common sense when dealing with cryptocurrencies. Before using ETHMask, we recommend consulting with a qualified professional or conducting thorough research to understand the potential risks involved.

Please note that using this software may be subject to legal and regulatory restrictions in your jurisdiction. It is your responsibility to comply with applicable laws and regulations.
