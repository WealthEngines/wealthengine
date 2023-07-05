import os
import seafileapi
from seafileapi.exceptions import DoesNotExist


class DownloadSeaFile:

    def __init__(self, **kwargs):
        server_link = kwargs.get("server_link", "https://oss.wealthengine.cn")
        username = kwargs.get("username", "username@wealthengine.cn")
        password = kwargs.get("password", "xxxxxxxx")

        self.filename = kwargs.get("filename", None)
        self.client = seafileapi.connect(server_link, username, password)

    def _write_file(self, to_path, file_name, file_obj):
        file_path = f'{to_path}/{file_name}'
        if os.path.exists(file_path):
            return
        with open(file_path, 'wb') as files:
            files.write(file_obj.get_content())

    def download_folder(self, folder, to_path, single_file=None):
        is_exists = os.path.exists(to_path)
        if not is_exists:
            raise Exception(f"{to_path} not exits")

        repo_list = self.client.repos.list_repos()
        repo_name_dict = {repo.name: repo.id for repo in repo_list}
        if folder not in repo_name_dict.keys() or folder is None:
            raise Exception(f"{folder} not exits in seafile or you do not have access to this directory")
        repo = self.client.repos.get_repo(repo_name_dict[folder])
        try:
            dirs = repo.get_dir("/")
            if single_file is not None:
                file_obj = repo.get_file(f'/{single_file}')
                file_name = file_obj.path
                self._write_file(to_path, file_name, file_obj)
                return True
            for entries in dirs.entries:
                file_name = entries.path
                file_obj = repo.get_file(file_name)
                self._write_file(to_path, file_name, file_obj)
            return True
        except DoesNotExist:
            raise Exception(f"dir not exits in seafile or you do not have access to this directory")


sealoder = DownloadSeaFile()
