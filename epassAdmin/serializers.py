from rest_framework import serializers
from epassUser.models import UserDetails


# class userSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = UserDetails
#         fields = ['id', 'email_id', 'password']
#         extra_lwargs = {
#             "password": {"write_only":True}
#         }
