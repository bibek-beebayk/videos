from rest_framework import serializers

from libs.functions import create_or_update_objects
from . import models
from django.db import transaction

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        depth = 1
        fields = ['id', 'name']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['id', 'name', 'address']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name']

class ContributionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContributionType
        fields = ['id', 'name']


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = ['id', 'contribution_type', 'name', 'company', 'remarks']

        extra_kwargs = {
            'id':{'read_only':False, 'required': False}
            }


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commodity
        fields = ['id', 'name']



class SituationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Situation
        fields = ['id', 'name']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Award
        fields = ['id','title', 'award_type', 'year']

        extra_kwargs = {
            'id':{'read_only':False, 'required': False}
            }


class MediaTypeSerialiser(serializers.ModelSerializer):
    class meta:
        model = models.MediaType
        fields = ['id', 'name']


class VideoSerializer(serializers.ModelSerializer):

    awards = AwardSerializer(many=True)
    contributors = ContributorSerializer(many=True)
    genres = GenreSerializer(many=True)
    commodities = CommoditySerializer(many=True)
    situations = SituationSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Video
        fields = ['id','user', 'company', 'media_type', 'product_name', 'product_title', 'on_air_date', 'commodities', 'genres', 'situations', 'tags', 'agency', 'production_company', 'views', 'downloads', 'video_file', 'video_file_60', 'video_file_30', 'video_file_15', 'duration', 'youtube_url', 'thumbnail1', 'thumbnail2', 'thumbnail3', 'thumbnail4', 'awards', 'contributors', 'created_at', 'updated_at']

   
    def create(self, validated_data):
        with transaction.atomic():
            # remove related fields from validated 
            validated_data.pop('genres')
            validated_data.pop('tags')
            validated_data.pop('commodities')
            validated_data.pop('situations')

            awards_data = validated_data.pop('awards')
            contributors_data = validated_data.pop('contributors')

            # retrieve the data from request
            genres_data = self.context['request'].data.get('genres')
            commodities_data = self.context['request'].data.get('commodities')
            situations_data = self.context['request'].data.get('situations')
            tags_data = self.context['request'].data.get('tags')

            # craeate video instance
            video = models.Video.objects.create(user=self.context['request'].user, **validated_data)

            # create related foreignkey objects
            for award in awards_data:
                models.Award.objects.create(media=video, **award)
            
            for contributor in contributors_data:
                models.Contributor.objects.create(media=video, **contributor)

            # create data for many to many related fields
            genres = create_or_update_objects(genres_data, models.Genre)
            commodities = create_or_update_objects(commodities_data, models.Commodity)
            situations = create_or_update_objects(situations_data, models.Situation
            )
            tags = create_or_update_objects(tags_data, models.Tag)
            video.genres.set(genres)
            video.commodities.set(commodities)
            video.situations.set(situations)
            video.tags.set(tags)

        return video


    def update(self, instance, validated_data):
        with transaction.atomic():

            awards = validated_data.pop('awards', None)
            contributors = validated_data.pop('contributors', None)
            validated_data.pop('situations')
            validated_data.pop('tags')
            validated_data.pop('commodities')
            validated_data.pop('genres')

            genres_data = self.context['request'].data.get('genres')
            commodities_data = self.context['request'].data.get('commodities')
            situations_data = self.context['request'].data.get('situations')
            tags_data = self.context['request'].data.get('tags')
            
            instance = super().update(instance, validated_data)

            # lists to store the id's of all the instances currently in the model
            awards_list = []
            contributors_list = []

            # retrieve the ids of awards from the validated data and store them in the list
            for award in awards:
                if 'id' in award:
                    awards_list.append(award['id'])

            # delete existing awards from the database that are not passed in the validated_data
            all_awards = models.Award.objects.filter(media=instance)
            for award in all_awards:
                if award.id not in awards_list:
                    award.delete()

            # Update the awards associated with a video, create new one if does not exist
            for award in awards:
                if 'id' in award:
                    award_instance = models.Award.objects.get(id=award['id'])
                    super().update(award_instance, award)
                else:
                    models.Award.objects.create(media=instance, **award)

            # retrieve contributor ids from the validated data and store them in a list
            for contributor in contributors:
                if 'id' in contributor:
                    contributors_list.append(contributor['id'])

            # delete the existing contributors related to the image  from the database that are not passed in the validated data
            all_contributors = models.Contributor.objects.filter(media=instance)
            for contributor in all_contributors:
                if contributor.id not in contributors_list:
                    contributor.delete()

            # Update the contributors, create new one if does not exist
            for contributor in contributors:
                if 'id' in contributor:
                    contributor_instance = models.Contributor.objects.get(id=contributor['id'])
                    super().update(contributor_instance, contributor)
                else:
                    models.Contributor.objects.create(media=instance, **contributor)

            genres = create_or_update_objects(genres_data, models.Genre)
            commodities = create_or_update_objects(commodities_data, models.Commodity)
            situations = create_or_update_objects(situations_data, models.Situation
            )
            tags = create_or_update_objects(tags_data, models.Tag)
            instance.genres.set(genres)
            instance.commodities.set(commodities)
            instance.situations.set(situations)
            instance.tags.set(tags)

            return instance


 

class ImageSerializer(serializers.ModelSerializer):
    awards = AwardSerializer(many=True)
    contributors = ContributorSerializer(many=True)
    genres = GenreSerializer(many=True)
    commodities = CommoditySerializer(many=True)
    situations = SituationSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Image
        fields = ['id', 'user', 'company', 'media_type', 'product_name', 'product_title', 'on_air_date', 'commodities', 'genres', 'situations', 'tags', 'agency', 'production_company', 'views', 'downloads', 'image_file', 'awards', 'contributors']


        def create(self, validated_data):
            with transaction.atomic():
                # remove related fields from validated
                pop_list = ['genres', 'tags', 'commodities', 'situations']
                for item in pop_list:
                    validated_data.pop(item)

                awards_data = validated_data.pop('awards')
                contributors_data = validated_data.pop('contributors')

                # retrieve the data from request
                genres_data = self.context['request'].data.get('genres')
                commodities_data = self.context['request'].data.get('commodities')
                situations_data = self.context['request'].data.get('situations')
                tags_data = self.context['request'].data.get('tags')

                # craeate video instance
                image = models.Image.objects.create(user=self.context['request'].user, **validated_data)

                # create related foreignkey objects
                for award in awards_data:
                    models.Award.objects.create(media=image, **award)
                
                for contributor in contributors_data:
                    models.Contributor.objects.create(media=image, **contributor)

                # create data for many to many related fields
                genres = create_or_update_objects(genres_data, models.Genre)
                commodities = create_or_update_objects(commodities_data, models.Commodity)
                situations = create_or_update_objects(situations_data, models.Situation
                )
                tags = create_or_update_objects(tags_data, models.Tag)
                image.genres.set(genres)
                image.commodities.set(commodities)
                image.situations.set(situations)
                image.tags.set(tags)

            return image


        def update(self, instance, validated_data):
            with transaction.atomic():

                awards = validated_data.pop('awards', None)
                contributors = validated_data.pop('contributors', None)

                pop_list= ['situations', 'tags', 'commodities', 'genres']
                for item in pop_list:
                    validated_data.pop(item)

                genres_data = self.context['request'].data.get('genres')
                commodities_data = self.context['request'].data.get('commodities')
                situations_data = self.context['request'].data.get('situations')
                tags_data = self.context['request'].data.get('tags')

                
                instance = super().update(instance, validated_data)

                # lists to store the id's of all the instances currently in the model
                awards_list = []
                contributors_list = []

                # retrieve the ids of awards from the validated data auser=self.context['request'].usernd store them in the list
                for award in awards:
                    if 'id' in award:
                        awards_list.append(award['id'])

                # delete existing awards from the database that are not passed in the validated_data
                all_awards = models.Award.objects.filter(media=instance)
                for award in all_awards:
                    if award.id not in awards_list:
                        award.delete()

                # Update the awards associated with a video, create new one if does not exist
                for award in awards:
                    if 'id' in award:
                        award_instance = models.Award.objects.get(id=award['id'])
                        super().update(award_instance, award)
                    else:
                        models.Award.objects.create(media=instance, **award)

                # update_objects(self, awards, models.Award, instance, media=instance.media)

                # retrieve contributor ids from the validated data and store them in a list
                for contributor in contributors:
                    if 'id' in contributor:
                        contributors_list.append(contributor['id'])

                # delete the existing contributors from the database that are not passed in the validated data
                all_contributors = models.Contributor.objects.filter(media=instance)
                for contributor in all_contributors:
                    if contributor.id not in contributors_list:
                        contributor.delete()

                # Update the contributors, create new one if does not exist
                for contributor in contributors:
                    if 'id' in contributor:
                        contributor_instance = models.Contributor.objects.get(id=contributor['id'])
                        super().update(contributor_instance, contributor)
                    else:
                        models.Contributor.objects.create(media=instance, **contributor)

                genres = create_or_update_objects(genres_data, models.Genre)
                commodities = create_or_update_objects(commodities_data, models.Commodity)
                situations = create_or_update_objects(situations_data, models.Situation
                )
                tags = create_or_update_objects(tags_data, models.Tag)
                instance.genres.set(genres)
                instance.commodities.set(commodities)
                instance.situations.set(situations)
                instance.tags.set(tags)

                return instance
