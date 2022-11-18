from notification.models import Client, Mailing, Message
from rest_framework import serializers


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    phone_number_code = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    message_status = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class MessageStatsSerializers(serializers.Serializer):
    mailing = serializers.IntegerField()
    message_status = serializers.CharField(max_length=8)
    count = serializers.IntegerField()
