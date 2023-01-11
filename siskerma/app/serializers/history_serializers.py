from siskerma.app.models import CooperationDucument, History, HistoryDetail
from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from rest_framework import serializers


class HistoryDetailSerializer(BaseModelSerializer):
    history = serializers.PrimaryKeyRelatedField(queryset=History.objects.all())
    status_name = serializers.ReadOnlyField(read_only=True, source='get_status_display')

    class Meta:
        model = HistoryDetail
        fields = '__all__'

    def validasi_ajuan(self, obj: CooperationDucument, validated_data):
        if validated_data['status'] == 1:
            obj.status = obj.status + 1
        else:
            obj.status = 6

        obj.step = obj.step + 1
        obj.save()

        HistoryDetail.objects.create(**validated_data)
        self.instance = obj
        return self.instance

        # validated_data['history']


class HistorySerializer(BaseModelSerializer):
    detail = HistoryDetailSerializer(many=True, read_only=True, source='historydetail_set')
    number_history = serializers.SerializerMethodField()

    def get_number_history(self, obj: History):
        return f'{obj.label} {obj.number}'

    class Meta:
        model = History
        fields = '__all__'
