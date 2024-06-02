import requests
import csv
from dotenv import load_dotenv
import os
import time
import sys

# Load environment variables from .env file
load_dotenv()

# Replace with your own Etherscan and Base API keys from the .env file
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
BASE_API_KEY = os.getenv('BASE_API_KEY')
ETHEREUM_BASE_URL = 'https://api.etherscan.io/api'
BASE_BASE_URL = 'https://api.basescan.org/api'
CSV_FILENAME = 'transactions.csv'
CALLS_PER_SECOND = 5
DELAY = 1 / CALLS_PER_SECOND

def get_transactions(address, api_key, base_url, start_block=0, end_block=99999999, page=1, offset=10000):
    url = f'{base_url}?module=account&action=txlist&address={address}&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort=asc&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == '1':
        return data['result']
    else:
        print(f"Error: {data['message']}")
        return []

def get_all_transactions(address, api_key, base_url):
    all_transactions = []
    page = 1
    while True:
        transactions = get_transactions(address, api_key, base_url, page=page)
        if not transactions:
            break
        all_transactions.extend(transactions)
        page += 1
        time.sleep(DELAY)  # Adding delay to handle rate limit
    return all_transactions

def save_transactions_to_csv(transactions, filename):
    # Define the CSV headers
    headers = [
        'blockNumber', 'timeStamp', 'hash', 'nonce', 'blockHash', 'transactionIndex',
        'from', 'to', 'value', 'gas', 'gasPrice', 'isError', 'txreceipt_status',
        'input', 'contractAddress', 'cumulativeGasUsed', 'gasUsed', 'confirmations', 'network'
    ]

    # Write transactions to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for tx in transactions:
            writer.writerow(tx)

def main(target_address):
    ethereum_transactions = get_all_transactions(target_address, ETHERSCAN_API_KEY, ETHEREUM_BASE_URL)
    for tx in ethereum_transactions:
        tx['network'] = 'Ethereum'

    base_transactions = get_all_transactions(target_address, BASE_API_KEY, BASE_BASE_URL)
    for tx in base_transactions:
        tx['network'] = 'Base'

    all_transactions = ethereum_transactions + base_transactions
    save_transactions_to_csv(all_transactions, CSV_FILENAME)
    print(f"All transactions have been saved to {CSV_FILENAME}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python AIWA.py <target_address>")
        sys.exit(1)
    
    target_address = sys.argv[1]
    main(target_address)

