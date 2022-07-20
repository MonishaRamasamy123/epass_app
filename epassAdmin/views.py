from django.shortcuts import render, redirect, reverse
from .models import AdminUsers
from epassUser.models import UserDetails
from epassUser import helpers
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from covid_india import states
import datetime
import requests
from rest_framework.response import Response
import json
import jwt
# from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed


# class ImageViewSet(FlexFieldsModelViewSet):
#
#     serializer_class = ImageSerializer
#     queryset = Image.objects.all()
#     permission_classes = [IsAuthenticated]


def index(request):
    context = {
        "form": AdminUsers()
    }
    return render(request, 'adminLogin.html', context)


def validate_admin_login(request):
    admin_user = AdminUsers.objects.filter(email_id=request.POST['email_id']).first()
    # admin_user = authenticate(request, email_id=request.POST['email_id'], password=request.POST['password'])
    if not admin_user:
        # raise AuthenticationFailed('User not found')
        context = {
            'errMsg': 'User not found',
            'email_id': request.POST['email_id'],
            'password': request.POST['password']
        }
        json_data = json.dumps(context)
        return HttpResponse(json_data)
    elif admin_user.password not in request.POST['password']:
        # raise AuthenticationFailed('Incorrect Password')
        context = {
            'errMsg': 'Incorrect Password',
            'email_id': request.POST['email_id'],
            'password': request.POST['password']
        }
        json_data = json.dumps(context)
        return HttpResponse(json_data)
    else:
        helpers.set_token(request, admin_user.id, 'admin_jwt')
        context = {
            'email_id': request.POST['email_id'],
            'password': request.POST['password'],
        }
        json_data = json.dumps(context)

        # return redirect('/adminLogin/adminUserDetailsView')
        return HttpResponse(json_data)


def admin_user_details_view(request):
    context = {
        # "approvalCard": range(1, 5)
    }
    if helpers.validate_token(request, 'admin_jwt') is not None:
        return render(request, 'userDetailsView.html', context)
    else:
        return helpers.unauthorized_admin(request)


def get_data_by_transport(request):

    if helpers.validate_token(request, 'admin_jwt') is not None:
        user_details = UserDetails.objects.all().filter(mode_of_transport=request.POST['transport_mode'], approval_status='Processing')

    # for user in user_details:
    #     if user.from_state:
    #         from_states_data = states.getdata(user.from_state)
    #         if from_states_data:
    #             from_count = from_states_data['Active']
    #             user.from_count = from_count
    #     if user.to_state:
    #         to_states_data = states.getdata(user.to_state)
    #         if to_states_data:
    #             to_count = to_states_data['Active']
    #             user.to_count = to_count

        url="https://api.covid19india.org/state_district_wise.json"
        response = requests.request("GET", url)
        response_text = json.loads(response.text)
        for user in user_details:
            if user.from_state:
                from_state_res = response_text.get(user.from_state, None)
                if from_state_res:
                    from_city_count = from_state_res.get('districtData').get(user.from_city, None)
                    if from_city_count:
                        user.from_count = from_city_count.get('confirmed', None)
                    else:
                        user.from_count = -1
                else:
                    user.from_count = -1

            if user.to_state:
                to_state_res = response_text.get(user.to_state, None)
                if to_state_res:
                    to_city_count = to_state_res.get('districtData').get(user.to_city, None)
                    if to_city_count:
                        user.to_count = to_city_count.get('confirmed', None)
                    else:
                        user.to_count = -1
                else:
                    user.to_count = -1

        json_data = serializers.serialize('json', user_details)
        return HttpResponse(json_data)

    return helpers.unauthorized_admin(request)


def update_approval_status(request):
    if helpers.validate_token(request, 'admin_jwt') is not None:
        reason = ''
        pk = request.POST['id']
        action = request.POST['action']
        if action == 'approve':
            status_update = 'Approved'
        elif action == 'reject':
            status_update = 'Rejected'
            reason = request.POST['reason']
        else:
            status_update = '';

        user_details = UserDetails.objects.get(id=pk)
        user_details.approval_status = status_update
        user_details.approved_date = datetime.datetime.now()
        user_details.reject_reason = reason
        user_details.save()

        return redirect('/adminLogin/adminUserDetailsView')
    else:
        return helpers.unauthorized_admin(request)


def get_admin_table_details(request):
    if helpers.validate_token(request, 'admin_jwt') is not None:
        filter_val = request.POST['filter']
        from_date = request.POST['fromDate']+' 00:00:00'
        to_date = request.POST['toDate']+' 23:59:59'
        if filter_val == 'All':
            user_details = UserDetails.objects.all().filter(submitted_date__gte=from_date,
                                                            submitted_date__lte=to_date).order_by('-id')
        else:
            user_details = UserDetails.objects.all().filter(submitted_date__gte=from_date,
                                                            submitted_date__lte=to_date,
                                                            approval_status=filter_val).order_by('-id')
        json_data = serializers.serialize('json', user_details)

        return HttpResponse(json_data)
    else:
        context = {
            "message": "Not Authorized"
        }
        json_data = json.dumps(context)
        return HttpResponse(json_data)
    # return redirect('/adminLogin/unauthorized_admin')
