from rest_framework import serializers

from siskerma.app.models import CooperationDocument, CooperationFile


class CooperationFileSerializer(serializers.ModelSerializer):
    cooperation = serializers.UUIDField(write_only=True)

    def create(self, validated_data):
        doc_id = validated_data.pop('cooperation')
        file = super().create(validated_data)
        doc = CooperationDocument.objects.get(id=doc_id)
        doc.files = file

        doc.save()

        return file

    class Meta:
        model = CooperationFile
        exclude = ['created_at', 'updated_at',]
