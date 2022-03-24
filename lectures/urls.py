from django.urls    import path
from lectures.views import LectureDetailView, LectureLikeView,LecturesView 

urlpatterns = [
    path('/<int:lecture_id>', LectureDetailView.as_view()),
    path('/<int:lecture_id>/like', LectureLikeView.as_view()),
    path('',LecturesView.as_view()),
]
