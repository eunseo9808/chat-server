from rest_framework import serializers
from django.contrib.auth.models import User


class UserManageSerializer(serializers.HyperlinkedModelSerializer):
    def create(self,validated_data):
        password = validated_data.pop('password')
        nickname = validated_data.pop('nickname')
        user = User.objects.create(**validated_data)
        user.chatter.nickname = nickname
        user.set_password(password)
        user.chatter.save()
        user.save()

        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'nickname')
        extra_kwargs = {
            'password': {'write_only': True}
        }
