import threading
import urllib.parse
from eth_account import Account
import app.utils.systeminfo
import app.utils.typing_utils


def create_keystore(pwd: str):
    account = Account.create()
    keystore_json = Account.encrypt(account.key, pwd)
    return keystore_json


def single(cls):
    instance = {}
    lock = threading.Lock()

    def __single(*args, **kwargs):
        if cls not in instance:
            with lock:
                if cls not in instance:
                    instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return __single


def get_system_info():
    """Get system info

    :return: system info
    """
    return {
        "cpu": systeminfo.GetCpuInfo(),
        "memory": systeminfo.GetMemInfo(),
        "disk": systeminfo.GetDiskInfo(),
        "system": systeminfo.GetSystemVersion(),
    }


def parse_path(url):
    """Parse path from url

    :param url: url to parse
    :return: path
    """
    result = urllib.parse.urlsplit(url)
    query = dict(urllib.parse.parse_qsl(result.query))
    ip = result.netloc
    path = result.path
    new_url = result
    res = {
        "query": query,
        "ip": ip,
        "path": path,
        "netloc": new_url.netloc,
    }
    return res
