from api.serializers import (ClientSerializer, MailingSerializer,
                             MessageSerializer, MessageStatsSerializers)
from django.db.models import Count
from notification.models import Client, Mailing, Message
from notification.tasks import message_create
from rest_framework import status, viewsets
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all().select_related("mailing").select_related("client")


class MailingViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = (
            Message.objects.select_related("mailing")
            .select_related("client")
            .values("mailing", "message_status")
            .annotate(count=Count("client"))
        )
        serializer = MessageStatsSerializers(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        message_create.apply_async(args=(serializer.data,))
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
