from django.urls import path
from . import views, helpers
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('userForm', views.user_form_redirect),
    path('userDetailForm', views.user_detail_form),
    path('save_user', views.save_user, name='save_user'),
    path('get_cities', views.get_cities, name='get_cities'),
    # path('unauthorized_admin', helpers.unauthorized_admin),
    # path('validate_token', helpers.validate_token)
    # path('send_otp', views.send_otp),
    # path('verify_otp', views.verify_otp)
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)