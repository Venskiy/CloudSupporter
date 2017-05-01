import sys
import os

import dropbox

from dropbox_manager.constants import DROPBOX_TOKEN
from dropbox_manager.dropbox_manager import DropboxManager
from yandex_disk.constants import MY_YANDEX_TOKEN
from yandex_disk.yandex_disk_manager import YandexDiskManager


MY_DROPBOX_APP_KEY = 'i58xh5qigf55ma1'
MY_DROPBOX_APP_SECRET = 'a9iwynwq94nyuca'


def dropbox_obtain_access_token():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(MY_DROPBOX_APP_KEY, MY_DROPBOX_APP_SECRET)
    authorize_url = flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    code = input("Enter the authorization code here: ").strip()
    access_token, user_id = flow.finish(code)
    return access_token

def play_file_from_dropbox(path):
    access_token = dropbox_obtain_access_token()
    dropbox_client = dropbox.dropbox.Dropbox(access_token)
    link = dropbox_client.files_get_temporary_link(path).link
    os.system('gst-launch-1.0 playbin uri=%s >/dev/null' % link)

def main():
    #dropbox = DropboxManager(DROPBOX_TOKEN)
    # print(dropbox.get_info_about_account())
    # print(dropbox.download_file('pow.png', '/kolya.png'))
    # with open('requirements.txt', 'rb') as f:
    #     data = f.read()
    # dropbox.upload_file(data, '/Dropbox/requirements.txt')
    #print(dropbox.files_list())
    path = str(sys.argv[1])
    service = path.split('/')[1]
    if service == 'dropbox':
        play_file_from_dropbox(path[8:])
    # yandex_disk = YandexDiskManager(MY_YANDEX_TOKEN)
    # print(yandex_disk.files_list())


if __name__ == '__main__':
    main()
