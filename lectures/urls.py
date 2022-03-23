from django.urls    import path
from lectures.views import LectureDetailView, LectureLikeView, LectureCreatorView, LectureStudentView, LecturesView

urlpatterns = [
    path('/<int:lecture_id>', LectureDetailView.as_view()),
    path('/<int:lecture_id>/like', LectureLikeView.as_view()),
    path('/creator', LectureCreatorView.as_view()),
    path('/student', LectureStudentView.as_view()),
    path('/likes', LectureLikeView.as_view()),
    path('',LecturesView.as_view()),
]
