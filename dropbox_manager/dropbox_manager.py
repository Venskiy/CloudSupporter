import dropbox


class DropboxManager():
    def __init__(self, token):
        self.dropbox = dropbox.dropbox.Dropbox(token)

    def get_info_about_account(self):
        return self.dropbox.users_get_current_account()
