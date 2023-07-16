from rest_framework import serializers

from core.models import Food


class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'description', 'category']


class GeneratedFoodSerializers(serializers.Serializer):
    breakfast = FoodSerializers()
    lunch = FoodSerializers()
    dinner = FoodSerializers()


class DaysSerializers(serializers.Serializer):
    no_of_days = serializers.IntegerField()

    def validate_no_of_days(self, value):
        # no_of_days = attrs.get('no_of_days')
        print('in validate: ', value)
        if int(value) > 50:
            raise serializers.ValidationError('You cannot query more than 50 days')
        return value

class RandomFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'description']
