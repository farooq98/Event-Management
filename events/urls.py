from django.urls import path

from .views import (
    EventListAPIView,
    EventDetailAPIView,
    CreateEventAPIView,
    AttendeesAPIView,
)

app_name = "events"
urlpatterns = [
    path("", view=EventListAPIView.as_view(), name="events_list"),
    path("<int:id>/", view=EventDetailAPIView.as_view(), name="event_details"),
    path("create/", view=CreateEventAPIView.as_view(), name="create_event"),
    path("attendees/<int:id>/", view=AttendeesAPIView.as_view(), name="create_attendees"),
]
