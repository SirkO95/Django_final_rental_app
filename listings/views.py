from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Listing, Booking, Review, SearchHistory, ViewHistory
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer, SearchHistorySerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class IsLandlordOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'is_landlord', False)


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsLandlordOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'rooms', 'housing_type', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'views_count']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ViewHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            listing=instance
        )
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular = Listing.objects.filter(is_active=True).annotate(
            num_views=Count('viewhistory')
        ).order_by('-num_views')[:10]
        serializer = self.get_serializer(popular, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_landlord', False):
            return Booking.objects.filter(listing__owner=user)
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        listing_pk = self.kwargs.get('listing_pk')
        if listing_pk:
            return Review.objects.filter(listing_id=listing_pk)
        return Review.objects.none()

    def perform_create(self, serializer):
        listing_pk = self.kwargs.get('listing_pk')
        listing = Listing.objects.get(pk=listing_pk)
        serializer.save(tenant=self.request.user, listing=listing)


class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular = SearchHistory.objects.values('query').annotate(count=Count('id')).order_by('-count')[:10]
        return Response(popular)