from bot import LOGGER
from re import IGNORECASE, search, escape


nsfw_keywords = [
    "porssfcsdn",
    "onlyfaddgdns",
    "nsfddddw",
    "Brazzdddders",
    "aduffdddlt",
    "xndddggesdxx",
    "xvidxxdddeos",
    "nsvhkkehejensnfwcherry",
    "harhhhjvvdcore",
    "Porhjvvhbnhub",
    "xvigvgjghgdeos2",
    "yougghjggporn",
    "pohhhhhrnrip",
    "phhlahhyboy",
    "hejkklhvvbntai",
    "erijjjjotica",
    "blojjioiwjob",
    "reggghhjdtube",
    "strnbggggipchat",
    "camnnnnngirl",
    "nudnnnnne",
    "fennnnntish",
    "cuchjjjbkold",
    "owweergy",
    "horrrrny",
    "swingersrrr",
]


def isNSFW(text):
    pattern = r'(?:^|\W|_)(?:' + '|'.join(escape(keyword) for keyword in nsfw_keywords) + r')(?:$|\W|_)'
    return bool(search(pattern, text, flags=IGNORECASE))


def isNSFWdata(data):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if any(isinstance(value, str) and isNSFW(value) for value in item.values()):
                    return True
            elif 'name' in item and isinstance(item['name'], str) and isNSFW(item['name']):
                return True
    elif isinstance(data, dict) and 'contents' in data:
        for item in data['contents']:
            if 'filename' in item and isNSFW(item['filename']):
                return True
    return False


async def nsfw_precheck(message):
    if isNSFW(message.text):
        return True
    
    reply_to = message.reply_to_message
    if not reply_to:
        return False

    if any(
        isNSFW(getattr(reply_to, attr).file_name)
        for attr in ['document', 'video']
        if hasattr(reply_to, attr) and getattr(reply_to, attr)
    ):
        return True

    return any(
        isNSFW(getattr(reply_to, attr))
        for attr in ['caption', 'text']
        if hasattr(reply_to, attr) and getattr(reply_to, attr)
    )
