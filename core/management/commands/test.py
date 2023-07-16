import schedule
import time
import requests
from django.conf import settings
from django.core.management import BaseCommand

from core.enums import FoodCategoryChoices
from core.models import Food

CATEGORY_CHOICE = FoodCategoryChoices.BREAKFAST


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_api_request(CATEGORY_CHOICE)
        # schedule.every(5).minutes.do(send_api_request, CATEGORY_CHOICE)
        # # schedule.every(3).seconds.do(job, 'afeez')
        # while True:
        #     schedule.run_pending()
        #     time.sleep(3)

beverages_prompt = f'Generate a list of non-alcoholic breakfast beverages commonly enjoyed in Nigeria. These beverages should be standalone options, meaning they can be enjoyed on their own without the need for additional food. Please provide a diverse range of options, including traditional Nigerian choices and other popular breakfast beverages. Ensure the list captures the unique flavors and cultural richness of Nigerian cuisine. Format each entry as "name || description" to create an organized and informative list. The goal is to create an enticing and informative compilation that readers can use to explore and enjoy a satisfying breakfast experience in Nigeria.'

cereals_prompt = f'Generate a list of breakfast cereals commonly enjoyed in Nigeria. These beverages should be standalone options, meaning they can be enjoyed on their own without the need for additional food. Please provide a diverse range of options, including traditional Nigerian choices and other popular breakfast beverages. Ensure the list captures the unique flavors and cultural richness of Nigerian cuisine. Format each entry as "name || description" to create an organized and informative list. The goal is to create an enticing and informative compilation that readers can use to explore and enjoy a satisfying breakfast experience in Nigeria'

prompt2 = f''' Generate 30 unordered list of Nigerian which does not include Alcohol of any kind that are suitable for {CATEGORY_CHOICE} using the format given below.
name || description 
To complete this task, follow these steps.
- Your suggestion should not contain anything that can intoxicate people such as Alcohol.
- The description should as well include the reason to eat it at this period.
- Research and compile list of 30 Nigerian Yoruba dishes, ensuring a diverse and wide range of options.
- ensure to put the correct Yoruba language mark on the name of each food.
- Review the structure and format of the generated data to ensure it meets the required output.
'''


def send_api_request(category):
    OPEN_API_KEY = settings.OPEN_API_KEY
    url = "https://api.openai.com/v1/completions"
    headers = {
        'Content-Type': 'Application/json',
        'Authorization': 'Bearer {}'.format(OPEN_API_KEY)
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': cereals_prompt,
        'temperature': 0.7,
        'max_tokens': 1050,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    response = requests.post(url, json=data, headers=headers)
    try:
        formatted = response.json().get('choices')[0].get('text').split('\n')[1:]
        formatted = [f for f in formatted if f != '']
        print('formatted: ', formatted)
        for item in formatted:
            name, description = item.split('||')
            print(name, description)
            name = name.lstrip().rstrip()
            if not Food.objects.filter(name=name, description=description).exists():
                Food.objects.create(name=name, description=description, category=category)
    except Exception as e:
        print(str(e))
        pass

# send_api_request(CATEGORY_CHOICE)
