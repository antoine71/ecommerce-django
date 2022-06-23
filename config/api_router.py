from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

### import your views, example below
# from ecommerce-django.sample_app.api.views import SampleViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

### register your views, example below
# router.register("sample_app", SampleViewSet)


app_name = "api"
urlpatterns = router.urls