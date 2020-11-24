# Generated by Django 3.1.3 on 2020-11-24 20:23
from django.contrib.auth.models import User
from django.db import migrations, models


def migrate(apps, _):
    User.objects.create_superuser('admin', password='admin')

    Function = apps.get_model('locode', 'Function')
    for code, name in [
        ['0', "Unknown"],
        ['1', "Port"],
        ['2', "Rail terminal"],
        ['3', "Road terminal"],
        ['4', "Airport"],
        ['5', "Postal exchange office"],
        ['6', "Reserved for multimodal functions, ICDs etc"],
        ['7', "Reserved for fixed transport functions (e.g. oil platform)"],
        ['B', "Border crossing"],
    ]:
        Function.objects.create(name=name, code=code)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(
                    choices=[('0', 'Unknown'), ('1', 'Port'), ('2', 'Rail terminal'), ('3', 'Road terminal'),
                             ('4', 'Airport'), ('5', 'Postal exchange office'),
                             ('6', 'Reserved for multimodal functions, ICDs etc'),
                             ('7', 'Reserved for fixed transport functions (e.g. oil platform)'),
                             ('B', 'Border crossing')], max_length=1)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Locode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ch', models.CharField(blank=True, max_length=1)),
                ('locode', models.CharField(max_length=5)),
                ('country_code', models.CharField(max_length=2)),
                ('location_code', models.CharField(max_length=3)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('name_wo_diacritics', models.CharField(blank=True, max_length=128)),
                ('sub_div', models.CharField(blank=True, max_length=128)),
                ('function', models.CharField(max_length=10)),
                ('status', models.CharField(blank=True, max_length=128)),
                ('date', models.CharField(blank=True, max_length=128)),
                ('iata', models.CharField(blank=True, max_length=128)),
                ('coordinates_str', models.CharField(blank=True, max_length=128)),
                ('remarks', models.CharField(blank=True, max_length=128)),
                ('functions', models.ManyToManyField(blank=True, to='locode.Function')),
            ],
        ),
        migrations.RunPython(migrate, migrations.RunPython.noop)
    ]
