# Generated by Django 4.2.5 on 2023-09-19 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Hepsi", "0007_remove_hikayekategorileri_resimyolu_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hikayekategorileri",
            name="sirasi",
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name="masalkategorileri",
            name="sirasi",
            field=models.IntegerField(default=100),
        ),
    ]
