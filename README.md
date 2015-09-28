# Corji
A distributed\*, resilient\*, high-availability\* CDN (Corgi Delivery Network) using SMS as a transport layer.

![A corgi!](http://media.giphy.com/media/KY7SQGKthgplm/giphy.gif)

*note: at time of writing, Corji is neither distributed not resilient nor particularly high availability.*

## The Stack

We're using [Flask](http://flask.pocoo.org/) to deliver TwiML via [Twilio](http://twilio.com).  The images are stored in an external Google Spreadsheet.  All of this is cached locally on a Heroku instance.

## The API

1. Text `+16693420943` with an emoji.
2. Receive a corresponding Corgi.
3. Rejoice.

## Roadmap

(Issues will probably be more accurate/detailed than this, but this will serve as a high-level overview.)

- [x] MVP
- [x] Remote data storage
- [ ] Support for emoticons
- [ ] Support for multiple corgis per emoji.
- [ ] Actual frontend
- [ ] Logging and metrics
- [ ] Testing + CI.
