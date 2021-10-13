import base64
from datetime import time
import os
from flask import Flask, request
from google.cloud import pubsub_v1

from config import config

app = Flask(__name__)

timeout_period = 5.0


@app.route('/')
def data():
    return "Welcome this is a flask app to process incomming pubsub message!"


# function to process the messages
def callback(message):
    print(f"Received {message.data}.")
    # add message processing logic here
    message.ack()  
    return f"Message: {message} is processed successfully"


@app.route("/msg_process", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]

    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        data = base64.b64decode(pubsub_message["data"]).decode("utf-8").strip()

    print("Message Data:",data)

    return ("Message Processed Successfylly", 200)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))