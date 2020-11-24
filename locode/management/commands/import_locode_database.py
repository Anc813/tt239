import zipfile
import re
import csv

from io import BytesIO, StringIO

from django.core.management.base import BaseCommand, CommandError
import requests
from django.db import transaction

from ...models import Locode, Function


class Command(BaseCommand):
    help = 'Delete existing data and fetch new LOCODE information'
    DATABASE_CSV_ZIP_URL = 'http://www.unece.org/fileadmin/DAM/cefact/locode/loc201csv.zip'
    FILENAME_RE = re.compile(r'^.+UNLOCODE CodeListPart\d+\.csv$')
    COLUMN_NAMES = [
        'ch',
        'country_code',
        'location_code',
        'name',
        'name_wo_diacritics',
        'sub_div',
        'function',
        'status',
        'date',
        'iata',
        'coordinates_str',
        'remarks',
    ]

    def save(self, locodes):
        print('Locodes found', len(locodes))
        assert len(locodes) > 0, "no codes were found"
        Locode.objects.bulk_create(locodes, batch_size=10000)
        Through = Locode.functions.through

        function_map = {item.code: item.id for item in Function.objects.all()}
        functions = []

        for locode in Locode.objects.all():  # we query database because sqlite does not returns ids in bulk_create
            for char in locode.function.replace('-', ''):
                functions.append(Through(function_id=function_map[char], locode_id=locode.id))

        print('functions found', len(functions))
        Through.objects.bulk_create(functions, batch_size=10000)

    def handle(self, *args, **options):
        response = requests.get(self.DATABASE_CSV_ZIP_URL)
        with transaction.atomic():
            Locode.objects.all().delete()

            locodes = []
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                # as of 24.11.2020 only three files are needed
                # 2020-1 UNLOCODE CodeListPart1.csv
                # 2020-1 UNLOCODE CodeListPart2.csv
                # 2020-1 UNLOCODE CodeListPart3.csv
                for file in zip_file.filelist:
                    if not self.FILENAME_RE.match(file.filename):
                        continue

                    with zip_file.open(file) as csvfile:
                        with StringIO(csvfile.read().decode('cp1252')) as io:
                            reader = csv.DictReader(io, self.COLUMN_NAMES)
                            for row in reader:
                                locode = Locode(**row)
                                locode.locode = locode.country_code + locode.location_code
                                locodes.append(locode)
            self.save(locodes)
