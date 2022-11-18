import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from settings.settings import TIME_ZONE


class Mailing(models.Model):
    date_time_start = models.DateTimeField("Дата и время запуска рассылки")
    text = models.TextField("текст сообщения")
    date_time_finish = models.DateTimeField("Дата и время окончания рассылки")
    client_filter = models.CharField(
        "Выбрать клиентов по соответствию тега/коду мобильного оператора",
        max_length=50,
        blank=True,
    )

    def __str__(self):
        return (
            f"Сообщение: {self.text}, "
            f"От: {self.date_time_start}, "
            f"До: {self.date_time_finish}, "
            f"Фильтер: {self.client_filter} "
        )


class Client(models.Model):
    phone_number = models.PositiveBigIntegerField(
        "Номер телефона",
        validators=[
            RegexValidator(
                regex=r"^7\d{10}$",
                message="Номер телефона должен быть в формате 7XXXXXXXXXX (X - цифра от 0 до 9)",
            )
        ],
    )
    phone_number_code = models.CharField(
        "Код мобильного оператора", max_length=3, blank=True
    )
    tag = models.CharField("Тег", max_length=50, blank=True)
    timezone = models.CharField(
        "Временая зона",
        max_length=32,
        choices=tuple(zip(pytz.all_timezones, pytz.all_timezones)),
        default=TIME_ZONE,
    )

    def __str__(self):
        return (
            f"Номер: {self.phone_number},"
            f"Код: {self.phone_number_code}, "
            f"Тег: {self.tag}, "
            f"Временая зона: {self.timezone}"
        )

    def save(self, *args, **kwargs):
        self.phone_number_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)


class Message(models.Model):
    class StatusMessage(models.TextChoices):
        WAS_SENT = "WAS_SENT", _("Отправлено")
        NOT_SENT = "NOT_SENT", _("Не отправлено")

    time_created = models.DateTimeField("Дата и время создания", auto_now_add=True)
    message_status = models.CharField(
        "Статус отправки",
        max_length=8,
        choices=StatusMessage.choices,
        default=StatusMessage.NOT_SENT,
    )
    mailing = models.ForeignKey(
        Mailing,
        verbose_name="Рассылки",
        on_delete=models.CASCADE,
        related_name="message",
    )
    client = models.ForeignKey(
        Client, verbose_name="Клиенты", on_delete=models.CASCADE, related_name="message"
    )

    def __str__(self):
        return (
            f"Статус: {self.message_status}, "
            f"Время создания: {self.time_created}, "
            f"Рассылка: {self.mailing}, "
            f"Клиент: {self.client}"
        )
