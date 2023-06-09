from siskerma.app.models import CooperationDocument, History, HistoryDetail
from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from rest_framework import serializers


class HistoryDetailSerializer(BaseModelSerializer):
    history = serializers.PrimaryKeyRelatedField(queryset=History.objects.all())
    status_name = serializers.ReadOnlyField(read_only=True, source='get_status_display')

    class Meta:
        model = HistoryDetail
        fields = '__all__'

    def validasi_ajuan(self, obj: CooperationDocument, validated_data):
        if validated_data['status'] == 1:
            if obj.type == 2 and obj.status == 0:
                obj.status = 3
            elif obj.type == 3 and obj.status == 0:
                obj.status = 4
            else:
                obj.status = obj.status + 1

        else:
            obj.status = 6  # di tolak

        # if obj.type == 2 or obj.type == 3:
        #     obj.step = 4
        # else:
        #     obj.step = obj.step + 1

        #  step 0 && status 0 => draft
        # statu 1 => belum divalidasi

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
