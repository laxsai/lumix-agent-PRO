from flask import Flask, request, jsonify
from wallet_summary import explain_wallet

app = Flask(__name__)

@app.route('/')
def home():
    return "LAXS Agent API is running!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    
    if not wallet_address:
        return jsonify({"error": "No wallet address provided"}), 400
    
    response = explain_wallet(wallet_address)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
