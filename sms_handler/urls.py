try:
    from django.conf.urls import url
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import url

from sms_handler.save_sms import sms_data_api

urlpatterns = [
    url(
        r'^test/$',
        sms_data_api,
        name="test"
    ),
]
