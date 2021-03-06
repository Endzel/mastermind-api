# Generated by Django 2.1.1 on 2018-10-26 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mastermind', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(blank=True, choices=[('red', 'RED'), ('blue', 'BLUE'), ('green', 'GREEN'), ('yellow', 'YELLOW'), ('purple', 'PURPLE'), ('brown', 'BROWN')], max_length=140, verbose_name='First')),
                ('second', models.CharField(blank=True, choices=[('red', 'RED'), ('blue', 'BLUE'), ('green', 'GREEN'), ('yellow', 'YELLOW'), ('purple', 'PURPLE'), ('brown', 'BROWN')], max_length=140, verbose_name='Second')),
                ('third', models.CharField(blank=True, choices=[('red', 'RED'), ('blue', 'BLUE'), ('green', 'GREEN'), ('yellow', 'YELLOW'), ('purple', 'PURPLE'), ('brown', 'BROWN')], max_length=140, verbose_name='Third')),
                ('fourth', models.CharField(blank=True, choices=[('red', 'RED'), ('blue', 'BLUE'), ('green', 'GREEN'), ('yellow', 'YELLOW'), ('purple', 'PURPLE'), ('brown', 'BROWN')], max_length=140, verbose_name='Fourth')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_feedback', models.CharField(choices=[('wrong', 'Wrong'), ('white', 'White'), ('black', 'Black')], default='wrong', max_length=140, verbose_name='First feedback')),
                ('second_feedback', models.CharField(choices=[('wrong', 'Wrong'), ('white', 'White'), ('black', 'Black')], default='wrong', max_length=140, verbose_name='Second feedback')),
                ('third_feedback', models.CharField(choices=[('wrong', 'Wrong'), ('white', 'White'), ('black', 'Black')], default='wrong', max_length=140, verbose_name='Third feedback')),
                ('fourth_feedback', models.CharField(choices=[('wrong', 'Wrong'), ('white', 'White'), ('black', 'Black')], default='wrong', max_length=140, verbose_name='Fourth feedback')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit_guesses', models.PositiveSmallIntegerField(blank=True, default=15, null=True, verbose_name='Limit guesses')),
                ('tries', models.PositiveSmallIntegerField(default=0, verbose_name='Total tries')),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='played_code', to='mastermind.Code', verbose_name='Secret code')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_play', to='mastermind.Feedback', verbose_name='Feedback received')),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='customuser',
            name='alias',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='Alias'),
        ),
        migrations.AddField(
            model_name='play',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_play', to=settings.AUTH_USER_MODEL, verbose_name='Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='codebreaker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='codebreaker_game', to=settings.AUTH_USER_MODEL, verbose_name='Code Breaker'),
        ),
        migrations.AddField(
            model_name='game',
            name='codemaker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='codemaker_game', to=settings.AUTH_USER_MODEL, verbose_name='Code Maker'),
        ),
        migrations.AddField(
            model_name='game',
            name='secret_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secret_code_game', to='mastermind.Code', verbose_name='Secret code'),
        ),
    ]
