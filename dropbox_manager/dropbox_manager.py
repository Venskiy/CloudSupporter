import dropbox


class DropboxManager(object):
    def __init__(self, token):
        self.dropbox = dropbox.dropbox.Dropbox(token)

    def get_info_about_account(self):
        return self.dropbox.users_get_current_account()

    def files_delete(self, path):
        return self.dropbox.files_delete(path)

    def file_download(self, download_path, path):
        return self.dropbox.files_download_to_file(download_path, path)

    def file_upload(self, file, path):
        return self.dropbox.files_upload(file, path)

    def files_list(self):
        return self.dropbox.files_list_folder('')
