from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()


router.register('genre', api.GenreViewSet, basename='genre')
router.register('company', api.CompanyViewSet, basename='company')
router.register('tag', api.TagViewSet, basename='tag')
router.register('contribution-type', api.ContributionTypeViewSet, basename='contribution-type')
router.register('contributor', api.ContributorViewSet, basename='contributor')
router.register('commodity', api.CommodityViewSet, basename='commodity')
router.register('situation', api.SituationViewSet, basename='situation')
router.register('award', api.AwardViewSet, basename='award')
router.register('media-type', api.MediaTypeViewSet, basename='media-type')
# router.register('media-base', api.MediaBaseViewSet, basename='media-base')
router.register('video', api.VideoViewSet, basename='video')
router.register('image', api.ImageViewSet, basename='image')



urlpatterns = router.urls