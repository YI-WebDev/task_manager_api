import datetime

from django.db import models

from generics.model import CustomBaseUser


class User(CustomBaseUser):
    """
    Customize Django user.
    Only adding properties django user model not have.
    """

    class Meta:
        db_table = 'user'

    name = models.CharField(max_length=128, verbose_name='ユーザ名')
    is_admin = models.BooleanField(default=False, verbose_name='管理者権限')
    password_expiry_date = models.DateTimeField(null=True, verbose_name='パスワード有効期限')

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.username = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{self.username}'
        super(User, self).delete()

    def get_short_profile(self):
        return {
            'id': self.hash_id,
            'name': self.name,
        }