from flask import Flask, request
import twilio.twiml


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    print request.values.get("Body")

    resp = twilio.twiml.Response()
    with resp.message("") as m:
        m.media("https://s-media-cache-ak0.pinimg.com/736x/ef/94/21/ef9421da2b6da030dca07a3a5fa48107.jpg")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
