#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import myenv

from flask import Flask, request

# Enable logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Zabbix on trk
@app.route('/zabbix', methods=['POST'])
def resend():
    content = request.get_json()
    logger.info(f"zabbix json == > {content}")
    chat_id = content['chat_id']
    message = content['text']
    try:
        import telegram
        bot = telegram.Bot(token=myenv.token_bot)
        bot.sendMessage(chat_id=chat_id, text=message, parse_mode="Markdown")
    except:
        logger.error(f"zabbix error ==> {content}")
    return 'ok'

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
        bot = telegram.Bot(token=myenv.token_bot)
        chat_id = myenv.alert_chat_id
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

