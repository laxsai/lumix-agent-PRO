import requests
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_wallet_data(wallet_address):
    url = f"https://public-api.solscan.io/account/{wallet_address}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def explain_wallet(wallet_address):
    data = get_wallet_data(wallet_address)
    if not data:
        return "Couldn't fetch wallet data. Please check the address."

    token_count = len(data.get("tokenInfoList", []))
    sol_balance = data.get("lamports", 0) / 1_000_000_000

    message = f"This wallet holds approximately {sol_balance:.2f} SOL and {token_count} different tokens. What does this mean?"

    # Ask GPT to explain it
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in Solana blockchain."},
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message["content"]
