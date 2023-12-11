import datetime
import hashlib


import requests

from logutil import logger


def md5(data:str):
    m = hashlib.md5()
    m.update(data.encode('utf-8'))
    return m.hexdigest()


def sha1(data:str):
    m = hashlib.sha1()
    m.update(data.encode('utf-8'))
    return m.hexdigest()


def split_path(data:str):
    return data[:2] + "/" + data[2:]


def download(url, output,
             referer="https://www.douyin.com",
             user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
             ) -> bool:
    headers = {
        'Referer': referer,
        'User-Agent': user_agent,
    }
    try:
        response = requests.get(url, headers=headers, stream=True)
        with open(output, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        logger.warning(f"download {url} failed with {str(e)}")
    return False

def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj