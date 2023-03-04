from rest_framework import serializers

from siskerma.app.models import CooperationDocument, CooperationEvidence


class CooperationEvidenceSerializer(serializers.ModelSerializer):
    cooperation = serializers.UUIDField(write_only=True)

    def create(self, validated_data):
        doc_id = validated_data.pop('cooperation')
        evidence = super().create(validated_data)
        doc = CooperationDocument.objects.get(id=doc_id)
        doc.evidence = evidence

        doc.save()

        return evidence

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = CooperationEvidence
        exclude = ['created_at', 'updated_at',]
