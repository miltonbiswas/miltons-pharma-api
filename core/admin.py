from django.contrib import admin
from .models import AdminUser, Course, Curriculum, Semester, Subject, Topic, Unit


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "level", "duration_years", "is_active")
    list_filter = ("is_active", "level")
    search_fields = ("name", "code")


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "course", "version", "is_active")
    list_filter = ("course", "is_active")
    search_fields = ("name", "code", "version")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("semester_number", "name", "curriculum")
    list_filter = ("curriculum",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "semester", "display_order", "is_active")
    list_filter = ("is_active", "semester__curriculum")
    search_fields = ("name", "code", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("unit_number", "title", "subject", "display_order")
    list_filter = ("subject__semester__curriculum", "subject")
    search_fields = ("title",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "unit", "status", "published_at", "display_order")
    list_filter = ("status", "unit__subject__semester__curriculum")
    search_fields = ("title", "slug", "teaser")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ("email", "supabase_user_id", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email", "supabase_user_id")