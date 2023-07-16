import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response

from core.enums import FoodCategoryChoices
from core.models import Food
from . import serializers


class RandomFood(ListAPIView):
    """
    API Endpoint: GET /api/random
        Request:
        Method: GET
        Response (Success):
            Status: 200 OK
            Body: {'status': 'success', 'data': 'random food'}
        Response (Error):
            Status: 400 Bad Request
            Body: {'status': 'error', 'errors': 'error'}
    """
    serializer_class = serializers.RandomFoodSerializer

    def get(self, request, *args, **kwargs):
        foods = Food.objects.all()
        food = random.choice(list(foods))
        serializer = self.serializer_class(food)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


class FoodList(CreateAPIView):
    """
    API Endpoint: POST /api/food
        Request:
        Method: POST
        Body: {"no_of_days": <number_of_days>}
        Response (Success):
            Status: 200 OK
            Body: {"status": "success", "data": [<food_list>]}
        Response (Error):
            Status: 400 Bad Request
            Body: {"status": "error", "errors": <serializer_errors>}
    """
    serializer_class = serializers.DaysSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            count = serializer.validated_data.get('no_of_days')
            food_list = generate_food(count)
            data = serializers.GeneratedFoodSerializers(food_list, many=True)
            return Response({'status': status.HTTP_200_OK, 'data': data.data})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors})


def generate_food(count):
    foods = Food.objects.all()
    breakfast = foods.filter(category=FoodCategoryChoices.BREAKFAST)
    lunch = foods.filter(category=FoodCategoryChoices.LUNCH)
    dinner = foods.filter(category=FoodCategoryChoices.DINNER)

    lunch_list = list(lunch)
    breakfast_list = list(breakfast)
    dinner_list = list(dinner)
    food_list = []
    for i in range(count):
        random.shuffle(breakfast_list)
        random.shuffle(lunch_list)
        random.shuffle(dinner_list)

        food_dict = dict()
        breakfast = random.choice(breakfast_list)
        lunch = random.choice(lunch_list)
        dinner = random.choice(dinner_list)

        food_dict['breakfast'] = breakfast
        food_dict['lunch'] = lunch
        food_dict['dinner'] = dinner

        food_list.append(food_dict)
    return food_list
