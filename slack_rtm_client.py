import os
import slack
from kubernetes_api.client import core_client
from kubernetes_api.client import apps_client
from kubernetes_api.database import database_status
from kubernetes_api.storage import check_pvc_storage
from nlp import find_env

def get_apps_kubernetes_client():
    return apps_client()

def get_core_kubernetes_client():
    return core_client()

@slack.RTMClient.run_on(event='message')
def slack_communicate(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    env = find_env(data.get('text'))

    if 'down' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text='OK, checking ' + env + ' environment',
            thread_ts=thread_ts,
            username="devopsbot"
        )        

        for status in database_status(get_apps_kubernetes_client()):
            web_client.chat_postMessage(
                channel=channel_id,
                text=status,
                thread_ts=thread_ts,
                username="devopsbot"
            )

        web_client.chat_postMessage(
            channel=channel_id,
            text='Checking free space available in all the pods, please wait...',
            thread_ts=thread_ts,
            username="devopsbot"
        )

        storage_result = check_pvc_storage(get_core_kubernetes_client())
        web_client.chat_postMessage(
            channel=channel_id,
            text=storage_result,
            thread_ts=thread_ts,
            username="devopsbot"
        )

def start():
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()