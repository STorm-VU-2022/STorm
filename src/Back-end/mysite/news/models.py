from django.db import models
from users.models import Teacher
from django.utils.translation import gettext_lazy as _
from .validators import validate_file_size_25mb
from groups.models import Methodic_group


class Publication(models.Model):
    # ID - Django by default creates it and assigns it as PK
    title = models.CharField(max_length=100, verbose_name='Title')
    language = models.CharField(max_length=20, verbose_name='Language')
    student_year = models.IntegerField(blank=False, verbose_name='Student Year')
    is_public = models.BooleanField(default=True, verbose_name='Is Public?')
    short_description = models.TextField(max_length=140, verbose_name='Short Description')
    description = models.TextField(blank=True, verbose_name='Description')     # change to True if it is possible to post materials only
    media = models.FileField(blank=True, upload_to='publication_materials/%Y/%m/%d', verbose_name=_('Media contents of file (up to 25MB)'), validators=[validate_file_size_25mb])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')        # To be set only 1 time
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Edited at')             # Automatically updates on change
    photo = models.ImageField(blank=True, upload_to='publication_photos/%Y/%m/%d', verbose_name=_('Publication Photo'))      # Will save picture based on upload date, automatically creates folder
    # = = = = = Many-To_one relationships = = = = =
    creator_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='creator_id', verbose_name='Creator')
    related_to_group = models.ForeignKey(Methodic_group, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Related to group")
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    """ If class "Subject" was described before (above class "Publication"), it would be ok to write
            it without quotes 
        PROTECT ensures, that we won't delete Subject that has some publications
            null=True allows us to create Subject for now, otherwise it is required     """
    # = = = = = M2M relationships = = = = =
    likes = models.ManyToManyField(Teacher, blank=True)
    downloads = models.ManyToManyField(Teacher, through='Downloads', related_name='teacher_downloads')
    comments = models.ManyToManyField(Teacher, through='Comments', related_name='commentaries')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Publication"        # Name of your model in single form
        verbose_name_plural = "Publications"        # Name of your model in plural form
        ordering = ['-created_at', 'title', ]         # -created_at prints the newest publications at the top


class Downloads(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='who_downloaded')      # No need to have records with missing teachers
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='what_downloaded')
    date_downloaded = models.DateTimeField(auto_now=True, verbose_name='Downloaded at')      # Automatically updates on change


class Comments(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='author_of_comment')  # No need to have records with missing teachers
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='commented_publication')
    comment = models.TextField(verbose_name='Comment')
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name='Commented at')     # To be set only 1 time


class Subject(models.Model):
    # ID - Django by default creates it and assigns it as PK
    name = models.CharField(max_length=30, unique=True, verbose_name="Name of subject")     # Math, History, Lithuanian language

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subject"        # Name of your model in single form
        verbose_name_plural = "Subjects"        # Name of your model in plural form
        ordering = ['name', ]
