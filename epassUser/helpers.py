import datetime
from rest_framework.response import Response
import jwt
from django.shortcuts import render


def set_token(request, id, token_name):
    date = str(datetime.datetime.now())
    date_exp = str(datetime.datetime.now() + datetime.timedelta(minutes=60))
    payload = {
        'id': id,
        'exp': date_exp,
        'lat': date
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256').encode('utf-8')
    response = Response()

    response.set_cookie(key=token_name, value=token, httponly=True)
    request.COOKIES[token_name] = token

    # response.data = {
    #     'jwt': token
    # }
    request.session[token_name] = str(token)


def validate_token(request, token_name):
    token = request.session.get(token_name, None)
    if not token or token is None:
        return None
    try:

        if token is not None:
            # signing_input = token.split('b\'')
            # header_segment, payload_segment = signing_input[1].split('.', 1)
            # print('chlkkkkk==', header_segment)
            # payload = jwt.utils.base64url_decode(payload_segment.split('.')[1]).decode('utf-8')
            # payload = jwt.decode(token, 'secret', algorithms='HS256')
            return token
    except Exception as e:
        return None


def unauthorized_admin(request):
    return render(request, 'unAuthorizedAdmin.html')


def unauthorized_user(request):
    return render(request, 'unAuthorizedUser.html')