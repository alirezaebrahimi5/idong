from django.urls import path

from .views import *


urlpatterns = [
    path("group/", GroupListCreateView.as_view()),
    path("group/<int:group_id>/", GroupUpdateDeleteDetailView.as_view()),
    path("group/create-link/", GroupInviteView.as_view()),
    path("group/join/", GroupJoinView.as_view()),

]