from rest_framework import serializers
from . import models
from django.db import transaction

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ['name']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['name', 'address']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['name']


class ContributionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContributionType
        fields = ['name']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = ['contribution_type', 'name', 'company', 'remarks']

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commodity
        fields = ['name']

class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Situation
        fields = ['name']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Award
        fields = ['title', 'award_type', 'year']


class MediaTypeSerialiser(serializers.ModelSerializer):
    class meta:
        model = models.MediaType
        fields = ['name']


# class MediaBaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.MediaBase
#         fields = ['user', 'title', 'description', 'published_date', 'agency', 'tags', 'genres', 'media_type', 'company', 'commodities', 'situations', 'views', 'downloads']


class VideoSerializer(serializers.ModelSerializer):

    awards = AwardSerializer(many=True)
    # genres = GenreSerializer(many=True)
    # commodities = CommoditySerializer(many=True)
    # situations = SituationSerializer(many=True)
    # tags = TagSerializer(many=True)

    class Meta:
        model = models.Video
        fields = ['id','user', 'company', 'media_type', 'product_name', 'product_title', 'on_air_date', 'commodities', 'genres', 'situations', 'tags', 'agency', 'production_company', 'views', 'downloads', 'video_file', 'video_file_60', 'video_file_30', 'video_file_15', 'duration', 'youtube_url', 'thumbnail1', 'thumbnail2', 'thumbnail3', 'thumbnail4', 'awards', 'created_at', 'updated_at']

    read_only_fields = ['user', 'crated_at', 'updated_at']

    def create(self, validated_data):
        with transaction.atomic():
            awards_data = validated_data.pop('awards')
            genres_data = validated_data.pop('genres')
            commodities_data = validated_data.pop('commodities')
            situations_data = validated_data.pop('situations')
            tags_data = validated_data.pop('tags')

            video = models.Video.objects.create( user=self.context['request'].user, **validated_data)

            # lists to store the current data in many-to-many fields
            current_genres = []
            current_situations = []
            current_commodities = []
            current_tags = []

            # import ipdb; ipdb.set_trace()

            # Retrieve the current items from many-to-many field models and store them in the lists
            for genre in models.Genre.objects.all().values('name'):
                current_genres.append(genre['name'])

            for situation in models.Situation.objects.all().values('name'):
                current_situations.append(situation['name'])

            for tag in models.Tag.objects.all().values('name'):
                current_tags.append(tag['name'])

            for commodity in models.Commodity.objects.all().values('name'):
                current_commodities.append(commodity['name'])

            for award in awards_data:
                models.Award.objects.create(media=video, **award)
            
            # import ipdb; ipdb.set_trace()
            
            for commodity in commodities_data:
                # if commodity.name.lower() in current_commodities:
                video.commodities.add(commodity)       
                    # models.Commodity.objects.create(**commodity)
                    

            for genre in genres_data:
                video.genres.add(genre)


            for situation in situations_data:
                video.situations.add(situation)

            for tag in tags_data:
                video.tags.add(tag)

        return video

    def update(self, instance, validated_data):
        with transaction.atomic():
            import ipdb; ipdb.set_trace()
            awards_data = validated_data.pop('awards')
            instance.save(**validated_data)
            # for award_data in awards_data:
            #     award = award_data.pop(0)
            #     if award.['title'] != instance.award['name']
            #     award.save(**award_data)
                

        return super().update(instance, validated_data)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['company', 'media_type', 'product_name', 'product_title', 'on_air_date', 'commodities', 'genres', 'situations', 'tags', 'agency', 'production_company', 'views', 'downloads', 'image_file']
        read_only_fields = ['user']
