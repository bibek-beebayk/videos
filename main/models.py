import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from libs.helpers import get_year_choices, get_current_year
from django.urls import reverse

# Create your models here.
User = get_user_model()

MEDIA_TYPE_VIDEO = 'V'
MEDIA_TYPE_IMAGE = 'I'

MEDIA_TYPE_CHOICES = [
    (MEDIA_TYPE_VIDEO, 'Video'),
    (MEDIA_TYPE_IMAGE, 'Image')
]

'''Start of Genre Model'''
class Genre(models.Model):

    name = models.CharField(max_length=256, unique=True, db_index=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name

'''End of Genre Model'''


'''Start of Company Model'''
class Company(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    address = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = _("Companies")

    def __str__(self):
        return self.name
'''End of Company Model'''


'''Start of Tag Model'''
class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('')

'''End of Tag Model'''

'''Start of ContributionType Model'''
class ContributionType(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True, verbose_name=_("Contribution Type"))
    # contributor = models.ForeignKey('Contributor', rela•••••ted_name='contributions', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

'''End of ContributionType Model'''


'''Start of Contributor Model'''
class Contributor(models.Model):
    contribution_type = models.ForeignKey(ContributionType, related_name='contributors', on_delete=models.SET_NULL, null=True, verbose_name=_("Contribution Type"))
    name = models.CharField(max_length=256)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='contributors', null=True)
    remarks = models.CharField(max_length=1024, blank=True, null=True)
    media = models.ForeignKey('MediaBase', on_delete=models.SET_NULL, null=True, related_name='contributors')


    def __str__(self):
        return self.name

'''End of Contributor Model'''


'''Start of Commodity Model'''
class Commodity(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)
    # related_media = models.ManyToManyField( 'MediaBase', verbose_name=_("Media"))

    class Meta:
        verbose_name_plural = _("Commodities")
    def __str__(self):
        return self.name

'''End of Commodity Model'''


'''Start of Situation Model'''
class Situation(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name
'''End of Situation Model'''

'''Start of Award Model'''
class Award(models.Model):
    ADVERTISING_AWARD = 'AD'
    MOVIE_DRAMA_AWARD = 'MO'
    MV_AWARD = 'MV'
    OTHER_AWARD = 'OT'

    AWARD_TYPES = [
        (ADVERTISING_AWARD, 'Advertising Award'),
        (MOVIE_DRAMA_AWARD, 'Movie/Drama Award'),
        (MV_AWARD, 'MV Award'),
        (OTHER_AWARD, 'Other Award')
    ]

    title = models.CharField(_("Award Title"), max_length=256)
    award_type = models.CharField(_("Award Type"), max_length=2, choices=AWARD_TYPES)
    year = models.IntegerField(_("Year"), choices=get_year_choices(), default=get_current_year(), blank=True)
    media = models.ForeignKey('MediaBase', on_delete=models.SET_NULL, null=True, related_name='awards')

    class Meta:
        unique_together = [['title', 'year']]


    def __str__(self):
        return self.title

'''End of Award Model'''


'''Start of Mediatype Model'''
class MediaType(models.Model):
    name = models.CharField(max_length=256, unique=True, db_index=True)


    def __str__(self) -> str:
        return self.name


'''End of MediaType model'''

'''Start of Agency Model'''
class Agency(models.Model):
    name = models.CharField(max_length=256, unique=True, )
'''End of Agency Model'''


'''Start of MediaBase Model'''
class MediaBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))

    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True,related_name='media', verbose_name=_("Company"))

    media_type = models.ForeignKey(MediaType, on_delete=models.PROTECT, related_name='media', verbose_name=_("Media Type"))

    product_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Product Name"))

    product_title = models.CharField(max_length=256, verbose_name=_("Product Title"))

    on_air_date = models.DateField(_("Published Date"), default=timezone.now)

    commodities = models.ManyToManyField(Commodity, related_name='media', verbose_name=_("Commodities"))

    genres = models.ManyToManyField(Genre, related_name='media', verbose_name=_("Genres"))

    situations = models.ManyToManyField(Situation, related_name='media', verbose_name=_("Situations"))

    tags = models.ManyToManyField(Tag, related_name='media', blank=True, verbose_name=_("Tags"))

    # description = models.TextField(_("Description"), null=True, blank=True)

    agency = models.CharField(max_length=256, verbose_name=_("Agency"), null=True, blank=True)

    production_company = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Production Company"))

    views = models.PositiveIntegerField(default=0, blank=True, verbose_name=_("Views"))

    downloads = models.IntegerField(null=True, blank=True, default=0, verbose_name=_("Downloads"))

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # sprite_url = models.URLField(_("VTT URL"), max_length=1024, null=True, blank=True)
    # # detail_type
    # # thumbnail_links
    # # recommended_order

    def __str__(self):
        return self.product_title

'''End of MediaBase Model'''


'''Start of Video Model'''
class Video(MediaBase):
    video_file = models.FileField(_("Full Video"), upload_to='videos', validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])], null=True, blank=True)
    
    video_file_60 = models.FileField(_("60 Seconds Preview"), upload_to='videos/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])])

    video_file_30 = models.FileField(_("30 Seconds Preview"), upload_to='videos/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])])

    video_file_15 = models.FileField(_("15 Seconds Preview"), upload_to='videos/', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov'])])   

    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Duration"))

    # stream_url = models.URLField(_("Stream URL"), max_length=1024, null=True, blank=True)

    youtube_url = models.URLField(_("Youtube URL"), blank=True, null=True)

    # vtt_url = models.URLField(_("VTT URL"), max_length=1024, null=True, blank=True)

    thumbnail1 = models.ImageField(upload_to='video/thumbnails/', blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to='video/thumbnails/', blank=True, null=True)
    thumbnail3 = models.ImageField(upload_to='video/thumbnails/', blank=True, null=True)
    thumbnail4 = models.ImageField(upload_to='video/thumbnails/', blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.user:
    #         self.user = self.context['request'].user

'''End of Video Model'''


'''Start of Image Model'''
class Image(MediaBase):
    image_file = models.ImageField(upload_to='content/images/')

'''End of Image Model'''

