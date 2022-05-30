from django.urls import reverse
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

class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MediaType
        fields = ['id', 'name']

class VideoThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoThumbnail
        fields = ['id','image']

        extra_kwargs = {
            'id':{'read_only':False, 'required': False}
            }

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Agency
        fields = ['id', 'name']


class VideoSerializer(serializers.ModelSerializer):

    awards = AwardSerializer(many=True)
    contributors = ContributorSerializer(many=True)
    thumbnails = VideoThumbnailSerializer(many=True)
    genres = GenreSerializer(many=True)
    commodities = CommoditySerializer(many=True)
    situations = SituationSerializer(many=True)
    tags = TagSerializer(many=True)
    company = CompanySerializer()
    media_type = MediaTypeSerializer()
    agency = AgencySerializer()
    

    class Meta:
        model = models.Video
        fields = ['id','user', 'company', 'media_type', 'product_name', 'product_title', 'on_air_date', 'commodities', 'genres', 'situations', 'tags', 'agency', 'production_company', 'views', 'downloads', 'video_file', 'video_file_60', 'video_file_30', 'video_file_15', 'duration', 'youtube_url', 'thumbnails', 'awards', 'contributors', 'created_at', 'updated_at']

   
    def create(self, validated_data):
        with transaction.atomic():
            # remove related fields from validated 
            # validated_data.pop('genres')
            # validated_data.pop('tags')
            # validated_data.pop('commodities')
            # validated_data.pop('situations')

            pop_list = ['genres', 'commodities', 'situations', 'tags', 'company', 'media_type','agency']
            for item in pop_list:
                validated_data.pop(item)

            awards_data = validated_data.pop('awards')
            contributors_data = validated_data.pop('contributors')
            thumbnails_data = validated_data.pop('thumbnails')

            # retrieve the data from request
            genres_data = self.context['request'].data.get('genres')
            commodities_data = self.context['request'].data.get('commodities')
            situations_data = self.context['request'].data.get('situations')
            tags_data = self.context['request'].data.get('tags')
            company = self.context['request'].data.get('company')
            media_type = self.context['request'].data.get('media_type')
            agency = self.context['request'].data.get('agency')

            # create video instance
            # TODO user=self.context['request'].user, to assign currently logged in user
            video = models.Video.objects.create(user=self.context['request'].user, **validated_data)
            

            # import ipdb; ipdb.set_trace()
            # create the company attribute
            if company.get('id'):
                video.company = models.Company.objects.get(id=company.get('id'))
            else:
                video.company = models.Company.objects.create(**company)

            # create the media_type attribute
            if media_type.get('id'):
                video.media_type = models.MediaType.objects.get(id=media_type.get('id'))
            else:
                video.media_type = models.MediaType.objects.create(**media_type)

            # create agency attribute
            if agency.get('id'):
                video.agency = models.Agency.objects.get(id=agency.get('id'))
            else:
                video.agency = models.Agency.objects.create(**agency)

            # create related foreignkey objects
            for award in awards_data:
                models.Award.objects.create(media=video, **award)
            
            for contributor in contributors_data:
                models.Contributor.objects.create(media=video, **contributor)

            for thumbnail in thumbnails_data:
                models.VideoThumbnail.objects.create(video=video, **thumbnail)
        

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

            video.save()

        return video


    def update(self, instance, validated_data):
        with transaction.atomic():
            awards = validated_data.pop('awards', None)
            contributors = validated_data.pop('contributors', None)
            thumbnails = validated_data.pop('thumbnails', None)

            pop_list = ['situations', 'tags', 'genres', 'commodities', 'company', 'media_type', 'agency']

            for item in pop_list:
                validated_data.pop(item)

            genres_data = self.context['request'].data.get('genres')
            commodities_data = self.context['request'].data.get('commodities')
            situations_data = self.context['request'].data.get('situations')
            tags_data = self.context['request'].data.get('tags')
            company = self.context['request'].data.get('company')
            media_type = self.context['request'].data.get('media_type')
            agency = self.context['request'].data.get('agency')
            
            instance = super().update(instance, validated_data)

            if company.get('id'):
                instance.company = models.Company.objects.get(id=company.get('id'))
            else:
                instance.company = models.Company.objects.create(**company)
                
            if media_type.get('id'):
                instance.media_type = models.MediaType.objects.get(id=media_type.get('id'))
            else:
                instance.media_type = models.MediaType.objects.create(**media_type)

            if agency.get('id'):
                instance.agency = models.Agency.objects.get(id=agency.get('id'))
            else:
                instance.agency = models.Agency.objects.create(**agency)

            # lists to store the id's of all the instances currently in the model
            awards_list = []
            contributors_list = []
            thumbnails_list = []

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

            # retrieve contributor ids from the validated data and store them in a list
            for thumbnail in thumbnails:
                if 'id' in thumbnail:
                    thumbnails_list.append(thumbnail['id'])

            # delete the existing thumbnails related to the video from the database that are not passed in the validated_data
            all_thumbnails = models.VideoThumbnail.objects.filter(video=instance)
            for thumbnail in all_thumbnails:
                if thumbnail.id not in thumbnails_list:
                    thumbnail.delete()

            # update the thumbnails, create new one if does not exist
            for thumbnail in thumbnails:
                if 'id' in thumbnail:
                    thumbnail_instance = models.VideoThumbnail.objects.get(id=thumbnail['id'])
                    super().update(thumbnail_instance, thumbnail)
                else:
                    models.VideoThumbnail.objects.create(video=instance, **thumbnail)

            # updating the related many-to-many fields
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
    company = CompanySerializer()
    media_type = MediaTypeSerializer

    class Meta:
        model = models.Image
        fields = ['id', 'user', 'company', 'media_type', 'product_name', 'product_title', 'on_air_date', 'commodities', 'genres', 'situations', 'tags', 'agency', 'production_company', 'views', 'downloads', 'image_file', 'awards', 'contributors']


        def create(self, validated_data):
            with transaction.atomic():
                # remove related fields from validated
                pop_list = ['genres', 'tags', 'commodities', 'situations', 'company', 'media_type']
                for item in pop_list:
                    validated_data.pop(item)

                awards_data = validated_data.pop('awards')
                contributors_data = validated_data.pop('contributors')

                # retrieve the data from request
                genres_data = self.context['request'].data.get('genres')
                commodities_data = self.context['request'].data.get('commodities')
                situations_data = self.context['request'].data.get('situations')
                tags_data = self.context['request'].data.get('tags')
                company = self.context['request'].data.get('company')
                media_type = self.context['request'].data.get('media_type')

                # craeate video instance
                image = models.Image.objects.create(user=self.context['request'].user, **validated_data)

                if company.get('id'):
                    image.company = models.Image.objects.get(id=company.get('id'))
                else:
                    image.company = models.Image.objects.create(**company)

                if media_type.get('id'):
                    image.media_type = models.MediaType.objects.get(id=media_type.get('id'))
                else:
                    image.media_type = models.MediaType.objects.create(**media_type)

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

                pop_list= ['situations', 'tags', 'commodities', 'genres', 'company', 'media_type']
                for item in pop_list:
                    validated_data.pop(item)

                genres_data = self.context['request'].data.get('genres')
                commodities_data = self.context['request'].data.get('commodities')
                situations_data = self.context['request'].data.get('situations')
                tags_data = self.context['request'].data.get('tags')
                company = self.context.get('request').data.get('company')
                media_type = self.context.get('request').data.get('media_type')
                
                instance = super().update(instance, validated_data)

                # if company.get('id'):
                #     instance.company = models.Company.objects.get(id=company.get('id'))
                # else:
                #     instance.company = models.Company.objects.create()

                instance.company, created = models.Company.objects.get_or_create(**company, defaults={"id": company.get('id')})

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
