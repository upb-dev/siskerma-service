from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import CooperationDocument, CooperationChoice, History, Institution, User
from rest_framework import serializers
from siskerma.app.serializers.cooperation_evidence_serializer import CooperationEvidenceSerializer
from siskerma.app.serializers.cooperation_file_serializer import CooperationFileSerializer
from siskerma.app.serializers.history_serializers import HistorySerializer

from siskerma.app.serializers.institution_serializer import InstitutionSerializer
from django.db.transaction import atomic

from rest_framework.exceptions import ValidationError
from datetime import datetime


class CooperationChoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = CooperationChoice
        fields = ['id', 'name']


class UserSerializers(BaseModelSerializer):
    id = serializers.UUIDField(required=False)
    institution_data = InstitutionSerializer(read_only=True, source='institution')
    institution = serializers.PrimaryKeyRelatedField(
        queryset=Institution.objects.all(), write_only=True, allow_empty=True, )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = '__all__'


class CooperationDocumentSerializer(BaseModelSerializer):
    # document_number = serializers.SerializerMethodField()
    type_document = serializers.ReadOnlyField(read_only=True, source='get_type_display')
    period_document = serializers.ReadOnlyField(read_only=True, source='get_period_display')
    status_document = serializers.ReadOnlyField(read_only=True, source='get_status_display')
    expied_date = serializers.DateTimeField(read_only=True)

    kerjasama = serializers.PrimaryKeyRelatedField(queryset=CooperationChoice.objects.all(
    ), write_only=True, allow_empty=True, many=True, source='choices_set')
    bentuk_kerjasama = CooperationChoiceSerializers(many=True, read_only=True, source='choices_set')
    partner = serializers.SerializerMethodField()
    files = CooperationFileSerializer(read_only=True)
    evidence = CooperationEvidenceSerializer(read_only=True)
    history = HistorySerializer(many=True, read_only=True, source='history_set')
    partner_data = UserSerializers(write_only=True, many=True)

    def get_partner(self, instance: CooperationDocument):
        active_partner = instance.user_set.filter(is_active=True)
        return UserSerializers(active_partner, many=True).data

    # def get_document_number(self, obj):

    #     return f'041072/{obj.get_type_display()}/{obj.created_at.year}/{obj.number:06d}'

    @atomic
    def create(self, validated_data):
        partner = validated_data.pop('partner_data')
        validated_data['prodi'] = self.context['worker'].prodi
        document = super().create(validated_data)
        for i in partner:
            User.objects.create(cooperation_document=document, **i,)

        return document

    @atomic
    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        partners = validated_data.pop('partner_data')
        instance = super().update(instance, validated_data)

        user_ids = []
        for i in partners:
            id = i.get('id', None)
            if id:
                try:
                    user = User.objects.get(id=id, cooperation_document=instance)
                    user.name = i.get('name', user.name)
                    user.address = i.get('address', user.address)
                    user.country = i.get('country', user.country)
                    user.email = i.get('email', user.email)
                    user.is_active = i.get('is_active', user.is_active)
                    user.institution = i.get('institution', user.institution)
                    user.responsible_name = i.get('responsible_name', user.responsible_name)
                    user.responsible_position = i.get('responsible_position', user.responsible_position)
                    user.responsible_approval_name = i.get('responsible_approval_name', user.responsible_approval_name)
                    user.responsible_approval_position = i.get(
                        'responsible_approval_position', user.responsible_approval_position)
                    user.updated_by = request.user
                    try:
                        user.save()
                    except Exception as e:
                        raise ValidationError({'detail': e})

                except User.DoesNotExist:
                    i['updated_by'] = request.user
                    i['created_by'] = request.user

                    try:
                        user = User.objects.create(cooperation_document=instance, **i)
                    except Exception as e:
                        raise ValidationError({'detail': e})
                user_ids.append(user.id)
            else:
                i['updated_by'] = request.user
                i['created_by'] = request.user

                try:
                    user = User.objects.create(cooperation_document=instance, **i)
                except Exception as e:
                    raise ValidationError({'detail': e})

                user_ids.append(user.id)
        User.objects.filter(cooperation_document=instance).exclude(
            id__in=user_ids).update(updated_by=request.user, is_active=False)

        return instance

    class Meta:
        model = CooperationDocument
        exclude = ['number', 'choices_set',]


class ListCooperationDocumentSerializer(BaseModelSerializer):
    is_active = serializers.SerializerMethodField()
    type_document = serializers.ReadOnlyField(read_only=True, source='get_type_display')
    status_document = serializers.ReadOnlyField(read_only=True, source='get_status_display')

    def get_is_active(self, obj: CooperationDocument):
        if obj.date_end != None:
            return True if obj.date_end > datetime.now().date() else False

        return False if obj.end_date < datetime.now().date() else True

    class Meta:
        model = CooperationDocument
        fields = ['id', 'document_number', 'name', 'type_document', 'is_active', 'status_document']


class AjukanUlangSerializer(serializers.Serializer):

    def ajukan_ulang(self, obj: CooperationDocument):
        obj.status = 0
        # obj.step = 0
        obj.save()

        self.instance = obj
        return self.instance


class AjukanSerializer(serializers.Serializer):
    def ajukan(self, instance: CooperationDocument):

        instance.status = 1  # status 1 => belom divalidasi

        # if instance.type == 2 or instance.type == 3:

        #     instance.step = 3  # => step 3 =>> persetujuan fakultas
        # else:
        instance.step = 1  # persetujuan prodi =>> untuk IA

        instance.save()
        History.objects.create(document=instance)

        self.instance = instance
        return self.instance


class SetReferenceSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def set_referenc(self, validated_data, instance: CooperationDocument):
        doc: CooperationDocument = CooperationDocument.objects.get(id=validated_data['id'])
        instance.parent = doc

        instance.save()

        self.instance = instance
        return self.instance


class ImportDataSerializer(serializers.Serializer):
    file = serializers.FileField()

    def insert_data(self, file):

        import openpyxl

        sheet_name: str = 'kerjasama'
        wb = openpyxl.load_workbook(file['file'])

        ws = wb[sheet_name]

        kerjasama_headers: list = ['document_number', 'type', 'start_date', 'end_date']

        for row in ws.iter_rows(min_row=2):
            if row[0].value is None:
                continue
            kerjasama_cells = [row[0], row[1], row[2], row[3]]
            values = []
            for i, v in enumerate(kerjasama_cells):
                if i == 0:
                    values.append(v.value)
                elif i == 1:
                    if v.value.upper() == "MOU":
                        values.append(3)
                    elif v.value.upper() == 'MOA':
                        values.append(2)
                    else:
                        values.append(1)
                else:
                    values.append(v.value)

            data_kerjasama = {}

            for key, cell in zip(kerjasama_headers, values):
                data_kerjasama[key] = cell
            data_kerjasama['period'] = 1
            data_kerjasama['status'] = 7
            data_kerjasama['updated_by'] = self.context['worker']
            data_kerjasama['created_by'] = self.context['worker']
            try:

                CooperationDocument.objects.create(**data_kerjasama)
            except Exception as e:
                print(str(e))
