# alertmanager-webhook
Telegram bot for forwarding prometheus and zabbix alerts, or any costum messages.
Refactored and ready for heroku.
For prometheus alerts forwarding chat_id must be defined in myenv.py.
## Usage
Configure alertmenager recievers:
```
 - name: 'telegram-webhook'
   webhook_configs:
    - url: http://your_bot.herokuapp.com/alerts
      send_resolved: true
```
For sending any other messages to any chat send json with POST to https://your_bot.herokuapp.com/webhook location
## Example json
```
{ "chat_id":"your chat id" "text":"your text" }
```
## Example curl command 
```
curl -H 'Content-Type: application/json' -XPOST -d '{ "chat_id": "-12345677899", "text": "sended by curl" }' https://your_bot.herokuapp.com
```
