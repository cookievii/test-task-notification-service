from api.views import ClientViewSet, MailingViewSet, MessageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register("clients", ClientViewSet)
router.register("messages", MessageViewSet)
router.register("mailings", MailingViewSet)
