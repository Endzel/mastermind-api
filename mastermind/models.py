from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from mastermind.choices import colours, feedbacks


# Create user token automatically
@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CustomUserManager(BaseUserManager):
    def create(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You must include an email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Super users must have is_staff flag activated')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super users must have is_superuser flag activated')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    alias = models.CharField(null=True, blank=True, max_length=140, verbose_name=_('Alias'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email

    def get_codemaker_games(self):
        return Game.objects.filter(codemaker=self)

    def get_codebreaker_games(self):
        return Game.objects.filter(codebreaker=self)


class Game(models.Model):

    limit_guesses = models.PositiveSmallIntegerField(default=15, null=True, blank=True, verbose_name=_('Limit guesses'))
    tries = models.PositiveSmallIntegerField(default=0, verbose_name=_('Total tries'))
    completed = models.BooleanField(default=False)

    # Relations
    secret_code = models.ForeignKey('Code', on_delete=models.CASCADE, related_name='secret_code_game', verbose_name=_('Secret code'))
    codemaker = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='codemaker_game', verbose_name=_('Code Maker'))
    codebreaker = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='codebreaker_game', verbose_name=_('Code Breaker'))

    def __str__(self):
        return str(self.id)

    def get_all_plays(self):
        return Play.objects.filter(game=self)


class Play(models.Model):

    # Relations
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='game_play', verbose_name=_('Related game'))
    feedback = models.ForeignKey('Feedback', on_delete=models.CASCADE, related_name='feedback_play', verbose_name=_('Feedback received'))
    code = models.ForeignKey('Code', on_delete=models.CASCADE, related_name='played_code', verbose_name=_('Secret code'))
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_play', verbose_name=_('Player'))

    def __str__(self):
        return str(self.id)


class Code(models.Model):

    # Positional codes
    first = models.CharField(choices=colours, blank=True, max_length=140, verbose_name=_('First'))
    second = models.CharField(choices=colours, blank=True, max_length=140, verbose_name=_('Second'))
    third = models.CharField(choices=colours, blank=True, max_length=140, verbose_name=_('Third'))
    fourth = models.CharField(choices=colours, blank=True, max_length=140, verbose_name=_('Fourth'))

    def __str__(self):
        return self.first + ' ' + self.second + ' ' + self.third + ' ' + self.fourth


class Feedback(models.Model):

    first = models.CharField(choices=feedbacks, default='wrong', max_length=140, verbose_name=_('First feedback'))
    second = models.CharField(choices=feedbacks, default='wrong', max_length=140, verbose_name=_('Second feedback'))
    third = models.CharField(choices=feedbacks, default='wrong', max_length=140, verbose_name=_('Third feedback'))
    fourth = models.CharField(choices=feedbacks, default='wrong', max_length=140, verbose_name=_('Fourth feedback'))

    def __str__(self):
        return self.first + ' ' + self.second + ' ' + self.third + ' ' + self.fourth

    def is_all_black(self):
        if self.first == "black" and self.second == "black" and self.third == "black" and self.fourth == "black":
            return True
        return False
