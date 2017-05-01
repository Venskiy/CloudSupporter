from __future__ import print_function
import httplib2
import sys
import os
import urllib.request

import dropbox
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from dropbox_manager.constants import DROPBOX_TOKEN
from dropbox_manager.dropbox_manager import DropboxManager
from yandex_disk.constants import MY_YANDEX_TOKEN
from yandex_disk.yandex_disk_manager import YandexDiskManager


MY_DROPBOX_APP_KEY = 'i58xh5qigf55ma1'
MY_DROPBOX_APP_SECRET = 'a9iwynwq94nyuca'

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'CloudManager'


def play_media_file(link):
    os.system('gst-launch-1.0 playbin uri=%s >/dev/null' % link)

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
    play_media_file(link)

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
    return credentials

def get_link_to_file(files, filename):
    print(filename)
    for file in files:
        print(file['name'])
        if file['name'] == filename:
            return file['webContentLink']
    return ''

def play_file_from_google(filename):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(fields='nextPageToken, files(name, webContentLink)').execute()
    files = results.get('files', [])

    link = get_link_to_file(files, filename)
    play_media_file(link)

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
    elif service == 'google':
        play_file_from_google(path.split('/')[len(path.split('/')) - 1])
    # yandex_disk = YandexDiskManager(MY_YANDEX_TOKEN)
    # print(yandex_disk.files_list())


if __name__ == '__main__':
    main()
