import random
from core.enums import FoodCategoryChoices
from core.models import Food


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


