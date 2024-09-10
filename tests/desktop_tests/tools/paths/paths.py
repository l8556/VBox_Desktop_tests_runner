# -*- coding: utf-8 -*-
from .local_paths import LocalPaths
from .remote_paths import RemotePaths


class Paths:

    def __init__(self, remote_user_name: str = None):
        self.local = LocalPaths()
        if remote_user_name:
            self.remote = RemotePaths(user_name=remote_user_name)