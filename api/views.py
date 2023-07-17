import random

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, permissions, authentication
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.enums import FoodCategoryChoices
from core.models import Food
from . import serializers
from .utils import generate_food


class RandomFood(ListAPIView):
    """
    API Endpoint: /api/random <br/>
        Description: returns random Food and Description. <br/>
        Method: GET <br/>
    """
    serializer_class = serializers.RandomFoodSerializer

    def get(self, request, *args, **kwargs):
        foods = Food.objects.all()
        food = random.choice(list(foods))
        serializer = self.serializer_class(food)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


class FoodList(CreateAPIView):
    """
    API Endpoint: /api/food <br/>
        Description: expect "no_of_days" and/or "category", returns the Breakfast, Lunch and Dinner for the number of
        days provided in the body. If category is provided, returns only food for the provided category.<br/>
        Method: POST <br/>
        Body: {
                "no_of_days": <number_of_days: int>,
                "category": <breakfast|lunch|dinner> ** category is optional
                }<br/>
    """
    serializer_class = serializers.GetFoodSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            count = serializer.validated_data.get('no_of_days')
            category = serializer.validated_data.get('category')
            food_list = generate_food(count, category)
            data = serializers.GeneratedFoodSerializers(food_list, many=True)
            return Response({'status': status.HTTP_200_OK, 'data': data.data})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors})


class CreateUserAccount(CreateAPIView):
    """
    API Endpoint: /api/v1/register<br/>
    Description: Accept "username", "password" and inturn create a new User object, and return the access and refresh token.<br/>
    Method: POST <br/>
    Body: {"username": "john1131", "password": "password"}
    """
    serializer_class = serializers.UserCreationSerializers
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            User.objects.create_user(username=username, password=password)
            access, refresh = get_tokens(username, password)
            return Response({'status': status.HTTP_201_CREATED, 'message': 'User created success.', 'access': access,
                             'refresh': refresh})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors})


def get_tokens(username, password):
    data = {'username': username, 'password': password}
    serializer = TokenObtainPairSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    access = serializer.validated_data.get('access')
    refresh = serializer.validated_data.get('refresh')
    return access, refresh
