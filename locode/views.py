from pathlib import Path

from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
# Create your views here.
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView, get_object_or_404, ListAPIView

from . import models
from . import serializers


@method_decorator(name='get', decorator=swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('code', openapi.IN_QUERY, 'Get information by 5 symbol length UN/LOCODEs',
                          type=openapi.TYPE_STRING, required=True, default='PLGWO'),
    ],
    operation_summary="Get single location information by UN/LOCODEs",
    responses={
        404: "No information by provided code"
    }
))
class GetLocationByCode(RetrieveAPIView):
    queryset = models.Locode.objects.all()
    serializer_class = serializers.LocodeSerializer

    def get_object(self):
        serializer = serializers.SearchByCodeInputSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        code = validated_data['code']
        return get_object_or_404(self.get_queryset(), locode__iexact=code)


@method_decorator(name='get', decorator=swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('name', openapi.IN_QUERY,
                          'Get UN/LOCODEs information by part of NameWoDiacritics field (case insensitive)',
                          type=openapi.TYPE_STRING, required=True, default='lublin'),
    ],
    operation_summary="List locations information by part of NameWoDiacritics field",
))
class SearchLocations(ListAPIView):
    queryset = models.Locode.objects.all()
    serializer_class = serializers.LocodeSerializer

    def filter_queryset(self, queryset):
        serializer = serializers.SearchLocationsInputSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        name = validated_data['name']
        queryset = queryset.filter(name_wo_diacritics__icontains=name)
        return super().filter_queryset(queryset)


@staff_member_required
def reparse(request):
    started_at = timezone.now()
    call_command('import_locode_database')
    elapsed_seconds = (timezone.now() - started_at).total_seconds()
    return HttpResponse(f"Total codes found {models.Locode.objects.all().count()}\nElapsed seconds: {elapsed_seconds}")
