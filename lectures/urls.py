from django.urls import path
from lectures.views import FileView 
 
urlpatterns = [
    path('/upload',FileView.as_view()),
]