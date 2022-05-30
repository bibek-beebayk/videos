from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()


router.register('genres', api.GenreViewSet, basename='genre')
router.register('companies', api.CompanyViewSet, basename='company')
router.register('tags', api.TagViewSet, basename='tag')
router.register('contribution-types', api.ContributionTypeViewSet, basename='contribution-type')
router.register('contributors', api.ContributorViewSet, basename='contributor')
router.register('commodities', api.CommodityViewSet, basename='commodity')
router.register('situations', api.SituationViewSet, basename='situation')
router.register('awards', api.AwardViewSet, basename='award')
router.register('media-types', api.MediaTypeViewSet, basename='media-type')
# router.register('media-base', api.MediaBaseViewSet, basename='media-base')
router.register('videos', api.VideoViewSet, basename='video')
router.register('images', api.ImageViewSet, basename='image')



urlpatterns = router.urls