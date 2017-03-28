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

    def get_info_about_account(self):
        url = self._base_url
        r = requests.get(url, headers=self.base_headers)
        return r.json()

    def files_list(self):
        url = self._base_url + 'resources/files'
        r = requests.get(url, headers=self.base_headers)
        return r.json()
