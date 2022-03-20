from django.urls import path
from lectures.views import LecturesView 
 
urlpatterns = [
    path('/upload',LecturesView.as_view()),
]