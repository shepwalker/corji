import twilio.twiml

def create_response(text, image_url=None):
    """Crafts a TwiML response using the supplied text and image."""
    resp = twilio.twiml.Response()
    with resp.message(text) as m:
        if image_url:
            m.media(image_url)
            
    return str(resp)