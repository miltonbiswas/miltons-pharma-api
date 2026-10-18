from rest_framework import serializers
from .models import Course, Curriculum, Semester, Subject, Unit, Topic


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "code", "name", "level", "duration_years", "total_credits"]


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = [
            "id",
            "course",
            "code",
            "name",
            "version",
            "source_url",
            "regulations_summary",
            "is_active",
        ]


class SemesterSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        source="curriculum.course",
        read_only=True,
    )
    curriculum_code = serializers.CharField(
        source="curriculum.code",
        read_only=True,
    )

    class Meta:
        model = Semester
        fields = [
            "id",
            "course",
            "curriculum",
            "curriculum_code",
            "semester_number",
            "name",
            "total_credits",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "semester",
            "code",
            "name",
            "slug",
            "category",
            "total_hours",
            "lecture_hours_per_week",
            "tutorial_hours_per_week",
            "practical_hours_per_week",
            "credits",
            "is_non_university_exam",
            "internal_marks",
            "end_sem_marks",
            "total_marks",
            "description",
            "objectives",
            "recommended_books",
            "display_order",
        ]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "id",
            "subject",
            "unit_number",
            "title",
            "hours",
            "description",
            "display_order",
        ]


class TopicTeaserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            "id",
            "unit",
            "title",
            "slug",
            "topic_type",
            "requires_synthesis_or_assay",
            "teaser",
            "published_at",
            "display_order",
        ]