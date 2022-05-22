from django import views
from rest_framework import viewsets
from . import serializers
from . import models

class GenreViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class ContributionTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ContributionType.objects.all()
    serializer_class = serializers.ContributionTypeSerializer

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = models.Contributor.objects.all()
    serializer_class = serializers.ContributorSerializer


class CommodityViewSet(viewsets.ModelViewSet):
    queryset = models.Commodity.objects.all()
    serializer_class = serializers.CommoditySerializer


class SituationViewSet(viewsets.ModelViewSet):
    queryset = models.Situation.objects.all()
    serializer_class = serializers.SituationSerializer

class AwardViewSet(viewsets.ModelViewSet):
    queryset = models.Award.objects.all()
    serializer_class = serializers.AwardSerializer


class MediaTypeViewSet(viewsets.ModelViewSet):
    queryset = models.MediaType.objects.all()
    serializer_class = serializers.MediaTypeSerialiser


# class MediaBaseViewSet(viewsets.ModelViewSet):
#     queryset = models.MediaBase.objects.all()
#     serializer_class = serializers.MediaBaseSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = models.Video.objects.all().select_related('media_type', 'company', 'user').prefetch_related('tags', 'commodities', 'situations', 'genres')
    serializer_class = serializers.VideoSerializer

    
class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer