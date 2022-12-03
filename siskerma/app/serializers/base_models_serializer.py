from rest_framework import serializers

class BaseModelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)

        attrs['updated_by'] = self.context['worker']
        if not self.instance:
            attrs['created_by'] = self.context['worker']

        return attrs