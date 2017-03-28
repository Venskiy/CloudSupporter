import requests


class YandexDiskManager(object):
    _base_url = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token
        self.base_headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token,
            "Host": "cloud-api.yandex.net"
        }

    def get_disk_metadata(self):
        url = self._base_url
        r = requests.get(url, headers=self.base_headers)
        return r.json()
