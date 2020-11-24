from django.db import models


class Function(models.Model):
    class TypeChoices(models.TextChoices):
        str_0 = '0', "Unknown"
        str_1 = '1', "Port"
        str_2 = '2', "Rail terminal"
        str_3 = '3', "Road terminal"
        str_4 = '4', "Airport"
        str_5 = '5', "Postal exchange office"
        str_6 = '6', "Reserved for multimodal functions, ICDs etc"
        str_7 = '7', "Reserved for fixed transport functions (e.g. oil platform)"
        str_B = 'B', "Border crossing"

    code = models.CharField(max_length=1, choices=TypeChoices.choices)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Locode(models.Model):
    # DOCUMENTATION https://service.unece.org/trade/locode/Service/LocodeColumn.htm#Function

    ch = models.CharField(max_length=1, blank=True)
    locode = models.CharField(max_length=5)
    country_code = models.CharField(max_length=2)
    location_code = models.CharField(max_length=3)
    name = models.CharField(max_length=128, blank=True)
    name_wo_diacritics = models.CharField(max_length=128, blank=True)
    sub_div = models.CharField(max_length=128, blank=True)
    function = models.CharField(max_length=10)
    functions = models.ManyToManyField(Function, blank=True)
    status = models.CharField(max_length=128, blank=True)
    date = models.CharField(max_length=128, blank=True)
    iata = models.CharField(max_length=128, blank=True)
    coordinates_str = models.CharField(max_length=128, blank=True)
    remarks = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.locode

