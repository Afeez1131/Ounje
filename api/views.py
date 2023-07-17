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
        Description: returns random Food and Description.
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
        Description: returns the Breakfast, Lunch and Dinner for the number of
        days provided in the body.
        If meal is provided, returns only food for the provided meal.
        Method: POST
        Body: {"no_of_days": <number_of_days: int>,
                "meal": <[breakfast|lunch|dinner]>}
        Response (Success):
            Status: 200 OK
            Body: {"status": "success", "data": [<food_list>]}
        Response (Error):
            Status: 400 Bad Request
            Body: {"status": "error", "errors": <serializer_errors>}
    """
    serializer_class = serializers.GetFoodSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            count = serializer.validated_data.get('no_of_days')
            meal = serializer.validated_data.get('meal')
            food_list = generate_food(count, meal)
            data = serializers.GeneratedFoodSerializers(food_list, many=True)
            return Response({'status': status.HTTP_200_OK, 'data': data.data})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors})


def generate_food(count: int, meal: str):
    foods = Food.objects.all()
    meal_list = []
    breakfast_list = []
    lunch_list = []
    dinner_list = []
    if not meal:
        breakfast = foods.filter(category=FoodCategoryChoices.BREAKFAST)
        lunch = foods.filter(category=FoodCategoryChoices.LUNCH)
        dinner = foods.filter(category=FoodCategoryChoices.DINNER)

        lunch_list = list(lunch)
        breakfast_list = list(breakfast)
        dinner_list = list(dinner)
    else:
        meal_list = list(foods.filter(category=meal))

    food_list = []
    for i in range(count):
        food_dict = dict()
        if not meal:
            random.shuffle(breakfast_list)
            random.shuffle(lunch_list)
            random.shuffle(dinner_list)

            breakfast = random.choice(breakfast_list)
            lunch = random.choice(lunch_list)
            dinner = random.choice(dinner_list)

            food_dict['breakfast'] = breakfast
            food_dict['lunch'] = lunch
            food_dict['dinner'] = dinner
        else:
            random.shuffle(meal_list)
            food_dict[meal] = random.choice(meal_list)

        food_list.append(food_dict)
    return food_list
