from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from . import models
from django.db import models as db_models

# Register your models here.


@admin.register(models.Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'award_type', 'year', 'media']
    list_filter = ['award_type', 'year']

@admin.register(models.Commodity)
class CommodityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']

# class ContributionTypeInline(admin.TabularInline):
#     model = models.ContributionType
#     extras = 1

class ContributorInline(admin.TabularInline):
    model = models.Contributor
    extra = 1

class AwardInline(admin.TabularInline):
    model = models.Award
    extra = 1

@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [ContributorInline, AwardInline]
    list_display = ['id', 'product_title', 'duration', 'views', 'downloads']
    list_filter = ['genres', 'media_type', 'tags', 'company', 'commodities', 'situations']
    list_per_page = 50
    # formfield_overrides = {
    #     db_models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # } 

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        # import pdb; pdb.set_trace()
        return super().save_model(request, obj, form, change)

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    inlines = [ContributorInline, AwardInline]
    list_display = ['id', 'product_title']
    list_filter = ['media_type', 'tags', 'company', 'commodities', 'situations']
    list_per_page = 50
    # formfield_overrides = {
    #     db_models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # } 

@admin.register(models.Contributor)
class ContributorAdmin(admin.ModelAdmin):
    # inlines = [ContributionTypeInline]
    list_display = ['id', 'name', 'company', 'contribution_type', 'media']
    list_filter = ['contribution_type']

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Situation)
class SitiationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(models.ContributionType)
class ContributionTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(models.MediaType)
class MediaTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


