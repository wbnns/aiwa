# AIWA (Address Interacted With Address)

![Alt](https://repobeats.axiom.co/api/embed/453912f5a3e66b04d3c7273124304c05f242fc4b.svg "Repobeats analytics image")

## Overview

AIWA is a script that fetches all transactions sent to a specific Ethereum address from both the Ethereum and Base mainnet. The results are saved to a CSV file.

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/wbnns/aiwa.git
   cd aiwa
   ```

2. Create a virtual environment and activate it:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install requests python-dotenv
   ```

4. Create a `.env` file based on the `.env.example`:

   ```sh
   cp .env.example .env
   ```

5. Edit the `.env` file and add your Etherscan and Base API keys.

## Usage

Run the script to fetch transactions for a specific address:

```sh
python aiwa.py <target_address>
```

Replace <target_address> with the Ethereum address you want to query, e.g., `0xebe9f0540df89509e5fbd4693c85ad66f73affc9`.

The transactions will be saved to `transactions.csv`.

## License

[MIT License](LICENSE)
