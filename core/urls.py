from django.urls import path
from .views import (
    AdminMeView,
    CourseListView,
    CurriculumListView,
    CurriculumSemesterListView,
    SemesterListView,
    SubjectListView,
    TopicContentView,
    TopicListView,
    UnitListView,
    health_check,
    admin_login_api,  # <-- Import admin login API view
)

urlpatterns = [
    path("health/", health_check, name="health"),
    path("admin/login/", admin_login_api, name="admin-login-api"),  # <-- Added route here
    path("courses", CourseListView.as_view(), name="course-list"),
    path(
        "courses/<int:course_id>/curricula",
        CurriculumListView.as_view(),
        name="curriculum-list",
    ),
    path(
        "courses/<int:course_id>/semesters",
        SemesterListView.as_view(),
        name="semester-list",
    ),
    path(
        "curricula/<int:curriculum_id>/semesters",
        CurriculumSemesterListView.as_view(),
        name="curriculum-semester-list",
    ),
    path(
        "semesters/<int:semester_id>/subjects",
        SubjectListView.as_view(),
        name="subject-list",
    ),
    path(
        "subjects/<int:subject_id>/units",
        UnitListView.as_view(),
        name="unit-list",
    ),
    path(
        "units/<int:unit_id>/topics",
        TopicListView.as_view(),
        name="topic-list",
    ),
    path("admin/me", AdminMeView.as_view(), name="admin-me"),
    path(
        "topics/<slug:slug>/content",
        TopicContentView.as_view(),
        name="topic-content",
    ),
]