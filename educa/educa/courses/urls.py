from django.urls import path
from .views import ManageCourseListView, CourseCreateView, CourseDeleteView, CourseUpdateView

urlpatterns = [
    path('mine/', ManageCourseListView.as_view(), name="manage_course_list"),
    path('create/', CourseCreateView.as_view(), name="course_create"),
    path("<pk>/edit/", CourseUpdateView.as_view(), name="course_update"),
    path("<pk>/delete/", CourseDeleteView.as_view(), name="course_detele")
]