from rest_framework import serializers
from users.models import Client


class ClientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'email', 'phone')

    def to_representation(self, instance):
        ret = super(ClientSerializer, self).to_representation(instance)
        for key, value in ret.items():
            if value is None:
                ret[key] = ''
        return ret
