from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import json

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/", methods=['POST'])
def webhook():
    record = json.loads(request.data)
    return record

if __name__ == '__main__':
    app.run()
