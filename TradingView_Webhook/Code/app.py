from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import json
from client import send
FORMAT = 'utf-8'

app = Flask(__name__)
run_with_ngrok(app)

@app.route("/", methods=['POST'])
def webhook():
    record = json.loads(request.data)
    # with open("TEST.txt","w") as testFile:
    #     testFile.write(json.dumps(record))
    #     testFile.close()
    send(str(record))
    return jsonify("message: Successfully Posted")

@app.route("/kill", methods=['GET'])
def close_local():
    send("!DISCONNECTED")
    return "Local Server detached"

if __name__ == '__main__':
    app.run()