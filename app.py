from dropbox_manager.constants import DROPBOX_TOKEN
from dropbox_manager.dropbox_manager import DropboxManager

def main():
    dropbox = DropboxManager(DROPBOX_TOKEN)
    print(dropbox.get_info_about_account())

if __name__ == '__main__':
    main()