from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate

from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from .authentication import SupabaseTokenAuthentication
from .models import Course, Curriculum, Semester, Subject, Topic, Unit
from .permissions import IsActiveAdmin
from .serializers import (
    CourseSerializer,
    CurriculumSerializer,
    SemesterSerializer,
    SubjectSerializer,
    TopicTeaserSerializer,
    UnitSerializer,
)

@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None and user.is_staff:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'ok': True,
            'token': token.key,
            'email': user.email,
            'role': 'admin'
        })
    return Response({
        'error': 'Invalid credentials or insufficient permissions'
    }, status=400)

@require_GET
def health_check(request):
    return JsonResponse({
        "ok": True,
        "service": "Milton's Pharma API",
        "status": "running",
    })


class ContentPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100


class PublicListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = ContentPagination


class CourseListView(PublicListView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.filter(is_active=True).order_by("name")


class CurriculumListView(PublicListView):
    serializer_class = CurriculumSerializer

    def get_queryset(self):
        return Curriculum.objects.filter(
            course_id=self.kwargs["course_id"],
            course__is_active=True,
            is_active=True,
        ).order_by("name")


class SemesterListView(PublicListView):
    serializer_class = SemesterSerializer

    def get_queryset(self):
        queryset = Semester.objects.select_related(
            "curriculum", "curriculum__course"
        ).filter(
            curriculum__course_id=self.kwargs["course_id"],
            curriculum__course__is_active=True,
            curriculum__is_active=True,
        )

        curriculum_id = self.request.query_params.get("curriculum_id")
        curriculum_code = self.request.query_params.get("curriculum")

        if curriculum_id:
            queryset = queryset.filter(curriculum_id=curriculum_id)
        elif curriculum_code:
            queryset = queryset.filter(curriculum__code=curriculum_code)

        return queryset.order_by("semester_number", "id")


class CurriculumSemesterListView(PublicListView):
    serializer_class = SemesterSerializer

    def get_queryset(self):
        return Semester.objects.select_related(
            "curriculum", "curriculum__course"
        ).filter(
            curriculum_id=self.kwargs["curriculum_id"],
            curriculum__is_active=True,
            curriculum__course__is_active=True,
        ).order_by("semester_number")


class SubjectListView(PublicListView):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return Subject.objects.filter(
            semester_id=self.kwargs["semester_id"],
            semester__curriculum__is_active=True,
            semester__curriculum__course__is_active=True,
            is_active=True,
        ).order_by("display_order", "name")


class UnitListView(PublicListView):
    serializer_class = UnitSerializer

    def get_queryset(self):
        return Unit.objects.filter(
            subject_id=self.kwargs["subject_id"],
            subject__is_active=True,
            subject__semester__curriculum__is_active=True,
            subject__semester__curriculum__course__is_active=True,
        ).order_by("display_order", "unit_number")


class TopicListView(PublicListView):
    serializer_class = TopicTeaserSerializer

    def get_queryset(self):
        return Topic.objects.filter(
            unit_id=self.kwargs["unit_id"],
            status=Topic.Status.PUBLISHED,
            unit__subject__is_active=True,
            unit__subject__semester__curriculum__is_active=True,
            unit__subject__semester__curriculum__course__is_active=True,
        ).order_by("display_order", "title")


class AdminMeView(APIView):
    authentication_classes = [SupabaseTokenAuthentication]
    permission_classes = [IsActiveAdmin]

    def get(self, request):
        return Response({
            "ok": True,
            "role": "admin",
            "user": {
                "id": request.user.id,
                "email": request.user.email,
            },
        })


class TopicContentView(RetrieveAPIView):
    authentication_classes = [SupabaseTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = None
    lookup_field = "slug"

    def get_queryset(self):
        return Topic.objects.filter(
            status=Topic.Status.PUBLISHED,
            unit__subject__is_active=True,
            unit__subject__semester__curriculum__is_active=True,
            unit__subject__semester__curriculum__course__is_active=True,
        )

    def retrieve(self, request, *args, **kwargs):
        topic = self.get_object()
        return Response({
            "id": topic.id,
            "title": topic.title,
            "slug": topic.slug,
            "teaser": topic.teaser,
            "body_markdown": topic.body_markdown,
            "attachment_url": topic.attachment_url,
            "content": topic.content,
            "published_at": topic.published_at,
        })