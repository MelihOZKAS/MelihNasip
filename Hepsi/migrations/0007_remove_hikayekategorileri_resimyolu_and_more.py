# Generated by Django 4.2.5 on 2023-09-17 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Hepsi", "0006_alter_hikayekategorileri_resimyolu_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="hikayekategorileri", name="resimyolu",),
        migrations.RemoveField(model_name="masalkategorileri", name="resimyolu",),
    ]
