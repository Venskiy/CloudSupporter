from dropbox_manager.constants import DROPBOX_TOKEN
from dropbox_manager.dropbox_manager import DropboxManager


def main():
    dropbox = DropboxManager(DROPBOX_TOKEN)
    # print(dropbox.get_info_about_account())
    # print(dropbox.download_file('pow.png', '/kolya.png'))
    # with open('requirements.txt', 'rb') as f:
    #     data = f.read()
    # dropbox.upload_file(data, '/Dropbox/requirements.txt')
    print(dropbox.files_list())


if __name__ == '__main__':
    main()
