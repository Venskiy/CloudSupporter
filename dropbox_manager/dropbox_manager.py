import dropbox


class DropboxManager():
    def __init__(self, token):
        self.dropbox = dropbox.dropbox.Dropbox(token)

    def get_info_about_account(self):
        return self.dropbox.users_get_current_account()

    def delete_file(self, path):
        return self.dropbox.files_delete(path)

    def download_file(self, download_path, path):
        return self.dropbox.files_download_to_file(download_path, path)

    def upload_file(self, file, path):
            return self.dropbox.files_upload(file, path)
