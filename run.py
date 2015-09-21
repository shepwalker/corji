# This Python file uses the following encoding: utf-8

from flask import Flask, request
import twilio.twiml

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    body = request.values.get("Body")

    corgis = {
        "🍁": "https://s-media-cache-ak0.pinimg.com/736x/ef/94/21/ef9421da2b6da030dca07a3a5fa48107.jpg",
        "🏀": "https://s-media-cache-ak0.pinimg.com/236x/6b/bf/37/6bbf3751b876a4dbdf73ff3f6ac3d3e2.jpg"
    }
    corgi = corgis.get(body, None)
    message = ""
    if not corgi:
        message = "No corgi :("

    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        if corgi:
            m.media(corgi)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
