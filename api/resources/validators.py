from functools import cached_property
import gzip
from pathlib import Path
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("このパスワードは短すぎます。少なくとも%(min_length)d文字以上にしてください。"),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "パスワードは少なくとも%(min_length)d文字以上にしてください。"
            % {'min_length': self.min_length}
        )


class CustomCommonPasswordValidator:
    @cached_property
    def DEFAULT_PASSWORD_LIST_PATH(self):
        return Path(__file__).resolve().parent / "common-passwords.txt.gz"

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        if password_list_path is CustomCommonPasswordValidator.DEFAULT_PASSWORD_LIST_PATH:
            password_list_path = self.DEFAULT_PASSWORD_LIST_PATH
        try:
            with gzip.open(password_list_path, "rt", encoding="utf-8") as f:
                self.passwords = {x.strip() for x in f}
        except OSError:
            with open(password_list_path) as f:
                self.passwords = {x.strip() for x in f}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("より複雑なパスワードを使用してください。"),
                code="password_too_common",
            )

    def get_help_text(self):
        return _("より複雑なパスワードを設定してください。")


class CustomNumericPasswordValidator:

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("このパスワードは数字のみです。文字も含めてください。"),
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return _("パスワードは数字のみにはできません。文字も含めてください。")