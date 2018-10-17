# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_city_province_town'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='provin_cecode',
            new_name='province_code',
        ),
    ]
