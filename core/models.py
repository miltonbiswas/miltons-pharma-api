from django.db import models


class Course(models.Model):
    code = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    level = models.CharField(max_length=30, default="undergraduate")
    duration_years = models.PositiveSmallIntegerField(default=4)
    total_credits = models.PositiveSmallIntegerField(default=208)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="curricula",
    )
    code = models.SlugField(max_length=50)  # e.g., 'pci-cbcs-2014' or 'nep-2020'
    name = models.CharField(max_length=150)
    version = models.CharField(max_length=100, blank=True)
    source_url = models.URLField(blank=True)
    regulations_summary = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["course", "code"],
                name="unique_course_curriculum_code",
            ),
        ]

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Semester(models.Model):
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.PROTECT,
        related_name="semesters",
        null=True,
        blank=True,
    )
    semester_number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100, blank=True)
    total_credits = models.CharField(max_length=50, blank=True)  # e.g., "27/29$/30#"

    class Meta:
        ordering = ["semester_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum", "semester_number"],
                name="unique_curriculum_semester",
            ),
        ]

    def __str__(self):
        curr_name = self.curriculum.code if self.curriculum else "Unassigned"
        return f"{curr_name} - Semester {self.semester_number}"


class Subject(models.Model):
    class Category(models.TextChoices):
        THEORY = "theory", "Theory (T)"
        PRACTICAL = "practical", "Practical (P)"
        REMEDIAL_THEORY = "remedial_theory", "Remedial Theory (RBT/RMT)"
        REMEDIAL_PRACTICAL = "remedial_practical", "Remedial Practical (RBP)"
        ELECTIVE = "elective", "Elective Theory (ET)"
        PRACTICE_SCHOOL = "practice_school", "Practice School (PS)"
        PROJECT_WORK = "project_work", "Project Work (PW)"

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="subjects",
    )
    code = models.CharField(max_length=50, blank=True)  # e.g., BP101T, BP107P
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.THEORY,
    )
    total_hours = models.PositiveSmallIntegerField(default=45)
    lecture_hours_per_week = models.PositiveSmallIntegerField(default=3)
    tutorial_hours_per_week = models.PositiveSmallIntegerField(default=1)
    practical_hours_per_week = models.PositiveSmallIntegerField(default=0)
    credits = models.PositiveSmallIntegerField(default=4)
    is_non_university_exam = models.BooleanField(default=False)
    internal_marks = models.PositiveSmallIntegerField(default=25)
    end_sem_marks = models.PositiveSmallIntegerField(default=75)
    total_marks = models.PositiveSmallIntegerField(default=100)
    description = models.TextField(blank=True, help_text="Scope of the subject")
    objectives = models.JSONField(default=list, blank=True, help_text="List of course objectives")
    recommended_books = models.JSONField(default=list, blank=True, help_text="List of recommended & reference books")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "code", "name"]
        indexes = [
            models.Index(fields=["semester", "is_active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}" if self.code else self.name


class Unit(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="units",
    )
    unit_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    hours = models.PositiveSmallIntegerField(default=10)
    description = models.TextField(blank=True, help_text="Official syllabus topics under this unit")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "unit_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "unit_number"],
                name="unique_subject_unit",
            ),
        ]

    def __str__(self):
        return f"{self.subject.code} - Unit {self.unit_number}: {self.title}"


class Topic(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    class ContentType(models.TextChoices):
        THEORY_TOPIC = "theory", "Theory Topic"
        PRACTICAL_EXPERIMENT = "practical", "Practical Experiment"
        DRUG_MONOGRAPH = "monograph", "Drug Synthesis / Monograph (*)"

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="topics",
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True)
    topic_type = models.CharField(
        max_length=20,
        choices=ContentType.choices,
        default=ContentType.THEORY_TOPIC,
    )
    requires_synthesis_or_assay = models.BooleanField(
        default=False,
        help_text="True if marked with asterisk (*) in PCI syllabus",
    )
    teaser = models.TextField(
        blank=True,
        help_text="Public short summary shown to everyone for SEO",
    )
    body_markdown = models.TextField(
        blank=True,
        help_text="Easy-to-write Markdown/Text notes from Admin Panel",
    )
    attachment_url = models.URLField(
        blank=True,
        help_text="Optional PDF/Diagram/Video link for this topic",
    )
    content = models.JSONField(
        default=list,
        blank=True,
        help_text="Structured JSON blocks for frontend rendering",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]
        indexes = [
            models.Index(fields=["unit", "status"]),
        ]

    def __str__(self):
        return self.title


class AdminUser(models.Model):
    supabase_user_id = models.UUIDField(unique=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "admin_users"
        ordering = ["email"]

    def __str__(self):
        return self.email