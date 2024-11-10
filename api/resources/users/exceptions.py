from generics.exception import TaskManagerException

"""
Error code prefix: 4100XX
"""


class UserNameAlreadyExists(TaskManagerException):
    default_detail = '`{username}` already exists.'
    default_detail_ja = '指定の`{username}` は既に使用されています。'
    default_code = 41001

    def __init__(self, username: str):
        super().__init__(username=username)