from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, SearchHistoryViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'search-history', SearchHistoryViewSet, basename='searchhistory')

urlpatterns = [
    path('', include(router.urls)),

    # Відгуки
    path('listings/<int:listing_pk>/reviews/',
         ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='review-list'),
    path('listings/<int:listing_pk>/reviews/<int:pk>/',
         ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='review-detail'),
]