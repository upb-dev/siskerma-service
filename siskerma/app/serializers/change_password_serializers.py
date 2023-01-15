from rest_framework import serializers
from rest_framework import status

from siskerma.app.models import Worker


class ChangePasswordSerializer(serializers.Serializer):
    model = Worker

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def update(self, instance, validated_data):

        if not instance.check_password(validated_data["old_password"]):
            raise serializers.ValidationError({'detail': "Wrong Password"})
        # set_password also hashes the password that the user will get
        instance.set_password(validated_data["new_password"])
        instance.save()

        self.instance = instance

        return self.instance
