# Generated by Django 2.1.5 on 2019-02-21 20:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20190221_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seeker',
            name='PrefType',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Main.JobChoices'),
        ),
    ]