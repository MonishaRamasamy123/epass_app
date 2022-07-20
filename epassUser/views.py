import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
import india
import json
from datetime import date
import datetime
from django.views.generic.dates import timezone_today
from .models import UserDetails
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response # pip install djangorestframework
import random
from . import helpers
import http.client


def index(request):
    return render(request, 'index.html')


def user_form_redirect(request):
    helpers.set_token(request, request.POST['phone_number'], 'user_jwt')
    request.session['phone_number'] = request.POST['phone_number']

    return HttpResponse('')


def user_detail_form(request):
    if helpers.validate_token(request, 'user_jwt') is not None:
        user_details = UserDetails.objects.filter(phone_number=request.session['phone_number']).order_by('-id')
        context = {
            "states": india.STATES_AND_TERRITORIES,
            "to_cities": [],
            "from_cities": [],
            "submitted_requests": user_details,
            "phone_number": request.session['phone_number']
        }

        return render(request, 'userDetails.html', context)
    else:
        return helpers.unauthorized_user(request)


def get_cities(request):
    if helpers.validate_token(request, 'user_jwt') is not None:
        cities_list = []
        sel_state = request.POST.get('selVal', '')
        for city in india.CITIES:
            if str(city.state) == sel_state:
                cities_list.append(str(city.name))

        json_data = json.dumps(cities_list)
        return HttpResponse(json_data)
    else:
        return helpers.unauthorized_user(request)


def save_user(request):
    if helpers.validate_token(request, 'user_jwt') is not None:
        values_to_save = request.POST
        # json_data = json.dumps(values_to_save)
        myfile = request.FILES['aadhar_img']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        user_details = UserDetails(
                                   first_name=values_to_save['first_name'],
                                   last_name=values_to_save['last_name'],
                                   phone_number=request.session['phone_number'],
                                   mode_of_transport=values_to_save['mode_of_transport'],
                                   age=values_to_save['age'],
                                   no_of_persons=values_to_save['no_of_persons'],
                                   from_address=values_to_save['from_address'],
                                   from_state=values_to_save['from_state'],
                                   from_city=values_to_save.get('from_city', ''),
                                   from_zip=values_to_save.get('from_zip', ''),
                                   to_address=values_to_save['to_address'],
                                   to_state=values_to_save['to_state'],
                                   to_city=values_to_save.get('to_city', ''),
                                   to_zip=values_to_save['to_zip'],
                                   reason=values_to_save['reason'],
                                   covid_status=values_to_save['covid_status'],
                                   approval_status='Processing',
                                   submitted_date=datetime.datetime.now(),
                                    aadhar_img=uploaded_file_url,
                                   )
        user_details.save()
        return redirect('/epassLogin/userDetailForm')
    else:
        return helpers.unauthorized_user(request)



# def send_otp(request):
#     if request.POST['phone_number'] is None:
#         return Response({
#             'status' : 400,
#             'key' : 'phone_number is required'
#         })
#     if request.POST['password'] is None:
#         return Response({
#             'status' : 400,
#             'key' : 'password is required'
#         })


# def send_otp(request):
#     phone_number = request.POST['phone_number']
#     otp = str(random.randint(1000, 9999))
#     csrf_token = request.POST['csrfmiddlewaretoken']
#     print('phone_number', phone_number)
#     sent_otp = helpers.send_otp_to_phone(phone_number, otp, csrf_token)
#     request.session['otp'] = otp
#
#     print('otp======', otp, phone_number, csrf_token)
#
#     return HttpResponse("sent successfully")
#
#
# def verify_otp(request):
#     phone_number = request.POST['phone_number']
#     input_otp = request.POST['otp']
#     otp = request.session['otp']
#     print('checking val==', otp, input_otp, phone_number)
#     request.session['phone_number'] = phone_number
#
#     return redirect('/userDetails/userDetailForm/')




