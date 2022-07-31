from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None,):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, ):
        """
        Creates and saves a superuser with the given email,  and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Teacher(AbstractUser):
    # ID - Django by default creates it and assigns it as PK
    username = models.CharField(max_length=100, verbose_name="user name")
    full_name = models.CharField(max_length=100, verbose_name="full name")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    profile_picture = models.ImageField(upload_to="profile_pictures/%Y/%m", blank=True, verbose_name="profile picture")
    self_description = models.TextField(blank=True, verbose_name="self description")
    follows = models.ManyToManyField("self", symmetrical=False, blank=True)
    recommends = models.ManyToManyField("self", symmetrical=False, through='Recommends', related_name='recommendations')
    profession = models.CharField(max_length=150, blank=True, default="New Teacher", verbose_name="Profession")

    # Social media links:
    facebook_link = models.CharField(max_length=200, blank=True, verbose_name="Facebook")
    twitter_link = models.CharField(max_length=200, blank=True, verbose_name="Twitter")
    instagram_link = models.CharField(max_length=200, blank=True, verbose_name="Instagram")
    linkedin_link = models.CharField(max_length=200, blank=True, verbose_name="LinkedIn")

    # Fields required for users by django:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "Teacher"  # Name of your model in single form
        verbose_name_plural = "Teachers"  # Name of your model in plural form
        ordering = ['full_name', ]


class Recommends(models.Model):
    recommender = models.ForeignKey(Teacher, related_name='recommender', verbose_name="Who recommends",
                                    on_delete=models.CASCADE)  # Teacher who recommends
    recommended = models.ForeignKey(Teacher, related_name='recommended', verbose_name="Who is recommended",
                                    on_delete=models.CASCADE)  # Teacher which was recommended
    recommendation_text = models.TextField(verbose_name=_('recommendation text'))
    recommendation_date = models.DateTimeField(auto_now_add=True, verbose_name='Created at')        # To be set only 1 time

    class Meta:
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
