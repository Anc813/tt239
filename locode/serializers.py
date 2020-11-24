from rest_framework import serializers
from . import models


class SearchByCodeInputSerializer(serializers.Serializer):
    code = serializers.CharField()


class SearchLocationsInputSerializer(serializers.Serializer):
    name = serializers.CharField()


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Function
        exclude = 'id',


class LocodeSerializer(serializers.ModelSerializer):
    functions = FunctionSerializer(many=True)

    class Meta:
        exclude = 'id',
        model = models.Locode
        swagger_schema_fields = {
            "example": {
                "functions": [
                    {
                        "code": "3",
                        "name": "Road terminal"
                    }
                ],
                "ch": "",
                "locode": "PLGWO",
                "country_code": "PL",
                "location_code": "GWO",
                "name": "Glowno",
                "name_wo_diacritics": "Glowno",
                "sub_div": "10",
                "function": "--3-----",
                "status": "RQ",
                "date": "0607",
                "iata": "",
                "coordinates_str": "5158N 01942E",
                "remarks": ""
            }
        }
