from django.contrib import admin
from notification.models import Client, Mailing, Message

admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)
