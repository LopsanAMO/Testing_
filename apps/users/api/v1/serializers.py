from rest_framework import serializers
from users.models import Client, Address


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone')

    def to_representation(self, instance):
        ret = super(ClientSerializer, self).to_representation(instance)
        for key, value in ret.items():
            if value is None:
                ret[key] = ''
        return ret


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'country', 'region', 'town', 'neighborhood', 'zip_code', 'street',
            'street_number', 'suite_number', 'id'
        )

    def to_representation(self, instance):
        ret = super(AddressSerializer, self).to_representation(instance)
        for key, value in ret.items():
            if value is None:
                ret[key] = ''
        return ret
