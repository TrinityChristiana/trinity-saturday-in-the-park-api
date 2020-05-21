import json
from django.http import HttpResponse, HttpResponseServerError
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from saturdayintheparkapi.models import Customer


@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if hasattr(authenticated_user, "auth_token"):
            authenticated_user.auth_token.delete()

        if authenticated_user is not None:
            token = Token.objects.create(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

            print("is there")
        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def get_user(request):

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        token = req_body['token']
        user = Token.objects.get(key=token).user
        customer = Customer.objects.filter(user__id=user.id)[0]
        userdict = {
            "first": user.first_name,
            "last": user.last_name,
            "email": user.email,
            "username": user.username,
            "id": customer.id,
            "is_staff": user.is_staff,
            "token": token
        }
        return HttpResponse(json.dumps(userdict), content_type='application/json')


@csrf_exempt
def logout_user(request):
    req_body = json.loads(request.body.decode())

    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        token = req_body['token']
        user = Token.objects.get(key=token).user
        user.auth_token.delete()
        return HttpResponse(json.dumps({"message": "User Logged Out"}), content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    try:
        req_body = json.loads(request.body.decode())
        new_user = User.objects.create_user(
            username=req_body['username'],
            email=req_body['email'],
            password=req_body['password'],
            first_name=req_body['first_name'],
            last_name=req_body['last_name']
        )

        customer = Customer.objects.create(
            family_members=req_body['family_members'],
            user=new_user
        )
        # Commit the user to the database by saving it
        customer.save()

        # Use the REST Framework's token generator on the new user account
        # token = Token.objects.create(user=new_user)

        # Return the token to the client
        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')
    except Exception as ex:
        return HttpResponseServerError(json.dumps({"error": f"{ex}"}))
