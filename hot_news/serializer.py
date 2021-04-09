"""
@Author: yanzx
@Date: 2020/11/29 18:56
@Description: 
"""
import re

from rest_framework import serializers

class WeiboSerializer(serializers.Serializer):
    weibo_id = serializers.CharField(max_length=20)
    author_id = serializers.CharField(max_length=255)
    author_avatar = serializers.CharField(max_length=255)
    author_gender = serializers.CharField(max_length=10)
    scheme = serializers.CharField(max_length=255)
    created_at = serializers.DateField()
    raw_text = serializers.CharField()
    comments_cnt = serializers.CharField(max_length=255)
    like_cnt = serializers.CharField(max_length=255)
    source = serializers.CharField(max_length=255)
    insert_time = serializers.DateTimeField()


class WeiboIdSerializer(serializers.Serializer):
    weibo_id = serializers.CharField(max_length=20)
    def validate_weibo_id(self, weibo_id):
        regex = r'^[0-9]+$'
        res = re.match(regex, weibo_id)
        if not res:
            message = "weibo_id is not validate"
            raise serializers.ValidationError(message)
        return weibo_id
