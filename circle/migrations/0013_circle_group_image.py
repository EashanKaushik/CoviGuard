# Generated by Django 4.0.2 on 2022-04-05 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("circle", "0012_circlepolicycompliance_compliance"),
    ]

    operations = [
        migrations.AddField(
            model_name="circle",
            name="group_image",
            field=models.FileField(blank=True, null=True, upload_to="media/"),
        ),
    ]
