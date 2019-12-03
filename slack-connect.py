import os
import slack

client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

response = client.chat_postMessage(
    channel='#devopsbot',
    text="Hello world!",
    as_user=False,
    username="devopsbot")
assert response["ok"]
assert response["message"]["text"] == "Hello world!"
