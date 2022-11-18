import os
import time

import requests
from api.services import get_time_start_currect_finish
from celery import shared_task
from django.db.models import Q

from .models import Client, Mailing, Message


@shared_task()
def message_send(message_id, wait=0):
    time.sleep(wait)
    message = Message.objects.filter(pk=message_id)
    if not message.exists():
        return
    message = message.first()

    response = requests.post(
        url="https://probe.fbrq.cloud/v1/send/" + str(message.id),
        headers={
            "accept": "application/json",
            "Authorization": "Bearer " + os.getenv("TOKEN"),
            "Content-type": "application/json",
        },
        json={
            "id": message.id,
            "phone": message.client.phone_number,
            "text": message.mailing.text,
        },
    )

    if response.text == '{"code":0,"message":"OK"}':
        message.message_status = Message.StatusMessage.WAS_SENT
        message.save()


@shared_task()
def message_create(data):
    mailing = Mailing.objects.get(**data)
    clients = Client.objects.filter(
        Q(tag__contains=data["client_filter"])
        | Q(phone_number_code=data["client_filter"])
    )

    for client in clients:
        time_start, time_now, time_finish = get_time_start_currect_finish(mailing)

        not_sent_msg = Message.objects.create(
            time_created=data["date_time_start"], mailing=mailing, client=client
        )

        if time_start <= time_now <= time_finish:
            message_send.apply_async(args=(not_sent_msg.id,), expires=time_finish)
            continue

        else:
            wait = (time_start - time_now).total_seconds()
            message_send.apply_async(args=(not_sent_msg.id, wait), expires=time_finish)
