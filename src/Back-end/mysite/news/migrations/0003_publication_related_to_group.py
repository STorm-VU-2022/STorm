# Generated by Django 4.0.4 on 2022-06-03 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_remove_methodic_group_invitation_code_and_more'),
        ('news', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='related_to_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.methodic_group', verbose_name='Related to group'),
        ),
    ]
