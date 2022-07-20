from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('validateLogin', views.validate_admin_login),
    path('adminUserDetailsView', views.admin_user_details_view),
    path('get_data_by_transport', views.get_data_by_transport, name='get_data_by_transport'),
    path('update_approval_status', views.update_approval_status),
    path('get_admin_table_details', views.get_admin_table_details),
    # path('token/', views.generate_token, name='generate_token'),
    # path('token/refresh/', views.refresh_token, name='refresh_token'),
    # path('send_otp', views.send_otp),
    # path('verify_otp', views.verify_otp)
]