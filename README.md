# WRAP Chat Bot

This is the chat bot code that accompanies my talk.  It requires Python 3.

## Setup

```bash
$ git clone https://github.com/SuzeShardlow/wrap-chatbot-talk.git
$ cd wrap-chatbot-talk
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## Running the Bot

To run the bot locally:

```bash
$ export FLASK_APP=bot.py
$ flask run --host=0.0.0.0
```

You can then interact with the bot via the browser at `http://localhost:5000/`.  Start by saying "Hello" :)