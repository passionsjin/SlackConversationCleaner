from slack_sdk import WebClient


def get_client(token):
    return WebClient(token)


def get_channels_info(client: WebClient):
    """
    channel 리스트 & 정보
    read channels 권한 필요
    :param client:
    :return:
    """
    return client.conversations_list().get('channels')


def get_conversations_history(client: WebClient, channel_id: str, latest: str | float = None,
                              oldest: str | float = None,
                              inclusive: bool = None):
    """
    특정 채널 대화 정보
    권한 필요 : mpim:history
              im:history
              groups:history
              channels:history

    :param oldest: Only messages after this Unix timestamp will be included in results.
    :param latest: Only messages before this Unix timestamp will be included in results. Default is the current time.
    :param inclusive: Include messages with oldest or latest timestamps in results. Ignored unless either timestamp is specified.
    :param client:
    :param channel_id:
    :return:
    """
    if latest:
        latest = str(latest)
    if oldest:
        oldest = str(oldest)
    return client.conversations_history(channel=channel_id, latest=latest, oldest=oldest, inclusive=inclusive).get(
        'messages')


def delete_message(client: WebClient, channel_id: str, timestamp: str | float):
    """
    메시지 삭제 from Timestamp
    필요권한 : chat:write
              chat:write:user
              chat:write:bot
    :param client:
    :param channel_id:
    :param timestamp:
    :return:
    """
    return client.chat_delete(channel=channel_id, ts=timestamp)

