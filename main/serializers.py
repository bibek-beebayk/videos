from rest_framework import serializers
from . import models

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class ContributionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContributionType
        fields = '__all__'


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = '__all__'

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commodity
        fields = '__all__'

class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Situation
        fields = '_-all__'


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Award
        fields = '__all__'


class MediaTypeSerialiser(serializers.ModelSerializer):
    class meta:
        model = models.MediaType
        fields = '__all__'


class MediaBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MediaBase
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'
