from rest_framework import serializers

from core.models import Food


class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'description', 'category']


class GeneratedFoodSerializers(serializers.Serializer):
    breakfast = FoodSerializers(allow_null=True)
    lunch = FoodSerializers(allow_null=True)
    dinner = FoodSerializers(allow_null=True)

    def to_representation(self, instance):
        data = super(GeneratedFoodSerializers, self).to_representation(instance)
        data['breakfast'] = data['breakfast'] or {}
        data['lunch'] = data['lunch'] or {}
        data['dinner'] = data['dinner'] or {}
        return data


class GetFoodSerializers(serializers.Serializer):
    no_of_days = serializers.IntegerField()
    meal = serializers.CharField(allow_blank=True)

    def validate_no_of_days(self, value):
        # no_of_days = attrs.get('no_of_days')
        if int(value) > 50:
            raise serializers.ValidationError('You cannot query more than 50 days')
        return value

    def validate_meal(self, value):
        if value and value.lower() not in ['breakfast', 'lunch', 'dinner']:
            raise serializers.ValidationError('Not a valid meal type. should be one of "Breakfast", "Lunch", "Dinner"')
        return value


class RandomFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name', 'description']
