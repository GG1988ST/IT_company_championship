# Generated by Django 2.1.5 on 2020-03-27 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ratecompany', '0007_company_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='emailtag',
            field=models.CharField(default=1, max_length=128, unique=True),
            preserve_default=False,
        ),
    ]