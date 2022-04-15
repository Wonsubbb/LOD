from rest_framework import serializers
from .validate import validate_sido, validate_gugun
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class TrafficInfoSerializer(serializers.Serializer):
    searchYear = serializers.IntegerField(max_value=datetime.now().year, min_value=2012)
    siDo = serializers.IntegerField(validators=[validate_sido])
    guGun = serializers.IntegerField(validators=[validate_gugun])
    numOfRows = serializers.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(9999)])
    pageNo = serializers.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(9999)])
    select = serializers.IntegerField(max_value=2, min_value=1)




