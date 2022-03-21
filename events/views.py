from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.contrib.auth import get_user_model

from core.permissions import IsOwner

from .serializers import EventSerializer, UserSerializer
from .models import Event

User = get_user_model()

class CustomPagination(PageNumberPagination):
    
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class EventListAPIView(ListAPIView):
    
    permission_classes = ()
    serializer_class = EventSerializer
    pagination_class = CustomPagination
    queryset = Event.objects.all().order_by('id')
    

class CreateEventAPIView(EventListAPIView, ListCreateAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class EventDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Event.objects.all().order_by('id')
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class AttendeesAPIView(ListAPIView):

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPagination
    queryset = User.objects.all().order_by('id')

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            events_attended__id=self.request.resolver_match.kwargs.get('id')
        ).order_by('id')
        return super().get_queryset()

    def post(self, request, *args, **kwargs):

        try:
            event = Event.objects.get(pk=kwargs.get('id'))
            event.attendees.add(request.user)
            return Response({
                "status": True, 
                "message": "{username} will attend the event".format(
                    username=request.user.username
                ),
            }, status=status.HTTP_201_CREATED)

        except Event.DoesNotExist:
            return Response({
                "status": False, 
                "message": "Event does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)
        