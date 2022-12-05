from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import CooperationDucument, CooperationChoice, User
from rest_framework import serializers

class CooperationChoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = CooperationChoice
        fields = ['id', 'name']

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class CooperationDocumentSerializer(BaseModelSerializer):

    status = serializers.IntegerField(write_only=True)
    period = serializers.IntegerField(write_only=True)
    type = serializers.IntegerField(write_only=True)

    document_number = serializers.SerializerMethodField()
    type_document = serializers.ReadOnlyField(read_only=True, source='get_type_display')
    period_document = serializers.ReadOnlyField(read_only=True, source='get_period_display')
    status_document = serializers.ReadOnlyField(read_only=True, source='get_status_display')
    expied_date = serializers.DateTimeField(read_only=True)

    kerjasama = serializers.PrimaryKeyRelatedField(queryset=CooperationChoice.objects.all(), write_only=True, allow_empty=True, many=True, source='choices_set')
    bentuk_kerjasama = CooperationChoiceSerializers(many=True, read_only=True, source='choices_set')
    partner = UserSerializers(source='user', read_only=True)

    def get_document_number(self, obj):

        return f'041033/{obj.get_type_display()}/{obj.created_at.year}/{obj.number}'
    class Meta:
        model = CooperationDucument
        exclude = ['number','choices_set',]