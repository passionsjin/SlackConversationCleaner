from datetime import datetime
from time import sleep

from slack_sdk import errors

from slack_client import get_channels_info, get_client, get_conversations_history, delete_message

BOT_USER_OAUTH_TOKEN = ""

CLIENT = get_client(token=BOT_USER_OAUTH_TOKEN)


def get_channel_id_list():
    conversations_list = get_channels_info(CLIENT)
    channels = {}
    for c in conversations_list:
        channels[c['name']] = c['id']
    return channels


def delete_message_avoid_rate_limit(client, channel_id: str, timestamp: str | float):
    cnt = 0
    while True:
        try:
            cnt += 1
            delete_message(client, channel_id, timestamp)
            break
        except errors.SlackApiError as e:
            if cnt > 5:
                print('Max retry... pass...')
                return False
            print(e.response)
            print(f'({cnt})Retry wait...')
            sleep(1)
            continue
    return True


def get_conversation_history_generator(client, channel_id: str, latest: str | float = None,
                                       oldest: str | float = None,
                                       inclusive: bool = None):
    while True:
        history = get_conversations_history(client, channel_id, latest, oldest, inclusive)
        if not history:
            return
        for h in history:
            if h:
                latest = h['ts']
                yield h


if __name__ == "__main__":
    target_channels = ['eads-alert']
    target_ts_latest = datetime.now().replace(hour=0, minute=0, microsecond=0, second=0).timestamp()
    # channel 목록
    channel_list = get_channel_id_list()
    # message 목록
    for channel_name in channel_list.keys():
        if channel_name not in target_channels:
            continue
        _channel_id = channel_list[channel_name]
        # get conversation & delete
        for conversation in get_conversation_history_generator(CLIENT, _channel_id, latest=target_ts_latest):
            delete_message_avoid_rate_limit(CLIENT, _channel_id, conversation['ts'])
