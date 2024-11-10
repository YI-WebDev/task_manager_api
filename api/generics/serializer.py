from rest_framework import serializers

DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

class HashIDModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for models with hash ID
    """
    id = serializers.CharField(source='hash_id', read_only=True)
    created_at = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)
    updated_at = serializers.DateTimeField(format=DATETIME_FORMAT, read_only=True)


class UserAwareModelSerializer(HashIDModelSerializer):
    """
    Serializer for models with user ownership
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=True)
    owner = serializers.DictField(source='user.get_short_profile', read_only=True)
