# Generated by Django 4.0.4 on 2022-06-09 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_publication_related_to_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name'], 'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
        migrations.RemoveField(
            model_name='subject',
            name='type',
        ),
    ]
