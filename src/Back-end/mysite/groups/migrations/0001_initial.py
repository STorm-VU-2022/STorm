# Generated by Django 4.0.3 on 2022-05-25 12:08

from django.db import migrations, models
import django.db.models.deletion
import groups.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitation_date', models.DateTimeField(auto_now_add=True, verbose_name='Invitation date')),
            ],
            options={
                'verbose_name_plural': 'Invitations',
            },
        ),
        migrations.CreateModel(
            name='Methodic_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name="Methodic group's name")),
                ('invitation_code', models.CharField(default=groups.models.group_key_generator, editable=False, max_length=16, unique=True, verbose_name='Invitation code')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Methodic group',
                'verbose_name_plural': 'Methodic groups',
                'ordering': ['name', 'creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Participates_in',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='groups.methodic_group')),
            ],
            options={
                'verbose_name_plural': 'Participants',
            },
        ),
    ]