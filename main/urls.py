from rest_framework.routers import DefaultRouter
from . import api
from django.urls import path

router = DefaultRouter()


# router.register('genres', api.GenreViewSet, basename='genre')
# router.register('companies', api.CompanyViewSet, basename='company')
# router.register('tags', api.TagViewSet, basename='tag')
# router.register('contribution-types', api.ContributionTypeViewSet, basename='contribution-type')
# router.register('contributors', api.ContributorViewSet, basename='contributor')
# router.register('commodities', api.CommodityViewSet, basename='commodity')
# router.register('situations', api.SituationViewSet, basename='situation')
# router.register('awards', api.AwardViewSet, basename='award')
# router.register('media-types', api.MediaTypeViewSet, basename='media-type')
# router.register('media-base', api.MediaBaseViewSet, basename='media-base')
router.register('my-videos', api.VideoViewSet, basename='my-video')
router.register('my-images', api.ImageViewSet, basename='my-image')

urlpatterns = [
    path('videos/', api.VideoListView.as_view(), name = 'all-videos'),
    path('videos/<int:pk>/', api.VideoDetailView.as_view(), name = 'video-details'),

]

urlpatterns += router.urls