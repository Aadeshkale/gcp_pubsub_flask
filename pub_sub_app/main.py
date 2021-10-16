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



# function to process the messages (publisher)
@app.route('/msg_send',methods=["POST"])
def send_msg():
    data = request.get_data().decode("utf-8")
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(config['project_id'], config['topic_name'])
    # Data must be a bytestring
    data = data.encode("utf-8")
    # Add two attributes, origin and username, to the message
    future = publisher.publish(
        topic_path, data, origin="myapp", username="gcp"
    )
    print(future.result())
    print(f"Published messages with custom attributes to {topic_path}.")
    return ("Message Sent Successfylly", 200)

# function to process the messages (consumer)
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
