from __future__ import print_function
import httplib2
import sys
import os
import requests

import dropbox
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


MY_DROPBOX_APP_KEY = 'i58xh5qigf55ma1'
MY_DROPBOX_APP_SECRET = 'a9iwynwq94nyuca'

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'CloudManager'

MY_YANDEX_APP_ID = '66fbabb28cbb4914a14466e3126b9963'
MY_YANDEX_APP_SECRET = '6f2fdf97736a4fffa48a5377526ef616'


try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('filename', nargs ='+', action = 'store')
    flags = parser.parse_args()
except ImportError:
    flags = None


def play_media_file(link):
    os.system('gst-launch-1.0 playbin uri="%s" &>/dev/null' % link)

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
    if os.path.exists('.dropbox_access_token'):
        file = open('.dropbox_access_token', 'r')
        access_token = file.read()
        file.close()
    else:
        access_token = dropbox_obtain_access_token()
        file = open('.dropbox_access_token', 'w')
        file.write(access_token)
        file.close()
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
        credentials = tools.run_flow(flow, store, flags)

    return credentials

def get_link_to_file(files, filename):
    for file in files:
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

def yandex_obtain_user_code():
    print('1. Go to: https://oauth.yandex.ru/authorize?response_type=code&client_id=66fbabb28cbb4914a14466e3126b9963')
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    code = input('Enter the authorization code here: ')
    return code

def yandex_obtain_access_token():
    code = yandex_obtain_user_code()
    response = requests.post('https://oauth.yandex.ru/token', 
                             data = {'grant_type': 'authorization_code', 
                                     'code': code,
                                     'client_id': MY_YANDEX_APP_ID,
                                     'client_secret': MY_YANDEX_APP_SECRET})
    return response.json()['access_token']

def play_file_from_yandex(path):
    if os.path.exists('.yandex_access_token'):
        file = open('.yandex_access_token', 'r')
        access_token = file.read()
        file.close()
    else:
        access_token = yandex_obtain_access_token()
        file = open('.yandex_access_token', 'w')
        file.write(access_token)
        file.close()
    url = 'https://cloud-api.yandex.net/v1/disk/resources/download?path=%s' % path
    headers = {
        'Accept': 'application/json',
        'Authorization': 'OAuth %s' % access_token,
        'Host': 'cloud-api.yandex.net'
    }
    response = requests.get(url, headers=headers)
    play_media_file(response.json()['href'])

def main():
    path = str(sys.argv[1])
    service = path.split('/')[1]
    if service == 'dropbox':
        play_file_from_dropbox(path[8:])
    elif service == 'google':
        play_file_from_google(path.split('/')[len(path.split('/')) - 1])
    elif service == 'yandex':
        play_file_from_yandex(path[7:])


if __name__ == '__main__':
    main()
