from siskerma.app.serializers.base_models_serializer import BaseModelSerializer
from siskerma.app.models import CooperationDucument, CooperationChoice, Institution, User
from rest_framework import serializers
from siskerma.app.serializers.cooperation_file_serializer import CooperationFileSerializer

from siskerma.app.serializers.institution_serializer import InstitutionSerializer

from rest_framework.exceptions import ValidationError


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

    # status = serializers.IntegerField(write_only=True)
    # period = serializers.IntegerField(write_only=True)
    # type = serializers.IntegerField(write_only=True)

    document_number = serializers.SerializerMethodField()
    type_document = serializers.ReadOnlyField(read_only=True, source='get_type_display')
    period_document = serializers.ReadOnlyField(read_only=True, source='get_period_display')
    status_document = serializers.ReadOnlyField(read_only=True, source='get_status_display')
    expied_date = serializers.DateTimeField(read_only=True)

    kerjasama = serializers.PrimaryKeyRelatedField(queryset=CooperationChoice.objects.all(
    ), write_only=True, allow_empty=True, many=True, source='choices_set')
    bentuk_kerjasama = CooperationChoiceSerializers(many=True, read_only=True, source='choices_set')
    partner = UserSerializers(source='user_set', many=True)
    files = CooperationFileSerializer(read_only=True)
    # partner_data = UserSerializers(write_only=True, many=True)

    def get_document_number(self, obj):

        return f'041033/{obj.get_type_display()}/{obj.created_at.year}/{obj.number}'

    def create(self, validated_data):
        partner = validated_data.pop('user_set')
        document = super().create(validated_data)
        for i in partner:
            User.objects.create(**i, cooperation_document=document)

        return document

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        partners = validated_data.pop('user_set')
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
                        user = User.objects.create(coopertaion_document=instance, **i)
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
        model = CooperationDucument
        exclude = ['number', 'choices_set',]


class ListCooperationDocumentSerializer(BaseModelSerializer):
    document_number = serializers.SerializerMethodField()
    type_document = serializers.ReadOnlyField(read_only=True, source='get_type_display')
    status_document = serializers.ReadOnlyField(read_only=True, source='get_status_display')

    def get_document_number(self, obj):

        return f'041033/{obj.get_type_display()}/{obj.created_at.year}/{obj.number}'

    class Meta:
        model = CooperationDucument
        fields = ['id', 'document_number', 'name', 'type_document', 'status_document']
