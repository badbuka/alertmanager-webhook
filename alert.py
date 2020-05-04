#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys

from flask import Flask, request

# Enable logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Liviness test
@app.route('/', methods=['GET'])
def homepage():
    return """
    <h1>Hello heroku. I am alive</h1>
    """
# Bot alerter
@app.route('/alert', methods=['POST'])
def alert():
    content = request.get_json()
    logger.info(f"alertmanager json == > {content}")
    try:
        import telegram
        # Initial bot by Telegram access token
        bot = telegram.Bot(token="828210247:AAFGvnijvBGVaWuR80S682d7cM6bDlt1qqc")
        chat_id = "-1001332344815"
        from msg import alert_msg_handler
        for alert_json in content['alerts']:
            parse_msg = alert_msg_handler(alert_json)
            parse_msg = parse_msg.replace("_","")
            if "warning" in parse_msg:
                parse_msg = parse_msg.replace("[FIRING]", "⚠️")
            else:
                parse_msg = parse_msg.replace("[FIRING]", "‼️")
            parse_msg = parse_msg.replace("[RESOLVED]", "✅")
            logger.info(f"post json == > {parse_msg}")
            bot.sendMessage(chat_id=chat_id, text=parse_msg, parse_mode="Markdown")
    except:
        logger.error(f"parse error ==> {content}")
    return 'ok'

if __name__ == "__main__":
    # Running server
    app.run()

