from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Course, Curriculum, Semester, Subject, Unit, Topic


class Command(BaseCommand):
    help = "Seeds the complete PCI B.Pharm (CBCS 2014/2016) Syllabus from PDF"

    def handle(self, *args, **options):
        course, _ = Course.objects.update_or_create(
            code="b-pharm",
            defaults={
                "name": "Bachelor of Pharmacy",
                "level": "undergraduate",
                "duration_years": 4,
                "total_credits": 208,
                "is_active": True,
            },
        )

        curriculum, _ = Curriculum.objects.update_or_create(
            course=course,
            code="pci-cbcs",
            defaults={
                "name": "PCI Revised Regulations (CBCS)",
                "version": "2016-17 (2014 Regulations)",
                "regulations_summary": "8 Semesters, 208 Minimum Credits, 80% Minimum Attendance, 50% Passing Marks.",
                "is_active": True,
            },
        )

        # Also create placeholder for NEP-2020 so multi-curriculum is ready
        Curriculum.objects.get_or_create(
            course=course,
            code="nep-2020",
            defaults={
                "name": "PCI NEP 2020 Curriculum",
                "version": "2020",
                "is_active": True,
            },
        )

        semesters_data = {
            1: ("Semester I", "27/29$/30#", [
                ("BP101T", "Human Anatomy and Physiology I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP102T", "Pharmaceutical Analysis I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP103T", "Pharmaceutics I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP104T", "Pharmaceutical Inorganic Chemistry - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP105T", "Communication Skills - Theory", "theory", 30, 2, 0, 0, 2, True, 15, 35, 50),
                ("BP106RBT", "Remedial Biology - Theory", "remedial_theory", 30, 2, 0, 0, 2, True, 15, 35, 50),
                ("BP106RMT", "Remedial Mathematics - Theory", "remedial_theory", 30, 2, 0, 0, 2, True, 15, 35, 50),
                ("BP107P", "Human Anatomy and Physiology - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP108P", "Pharmaceutical Analysis I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP109P", "Pharmaceutics I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP110P", "Pharmaceutical Inorganic Chemistry - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP111P", "Communication Skills - Practical", "practical", 30, 0, 0, 2, 1, True, 10, 15, 25),
                ("BP112RBP", "Remedial Biology - Practical", "remedial_practical", 30, 0, 0, 2, 1, True, 10, 15, 25),
            ]),
            2: ("Semester II", "29", [
                ("BP201T", "Human Anatomy and Physiology II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP202T", "Pharmaceutical Organic Chemistry I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP203T", "Biochemistry - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP204T", "Pathophysiology - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP205T", "Computer Applications in Pharmacy - Theory", "theory", 30, 3, 0, 0, 3, True, 25, 50, 75),
                ("BP206T", "Environmental Sciences - Theory", "theory", 30, 3, 0, 0, 3, True, 25, 50, 75),
                ("BP207P", "Human Anatomy and Physiology II - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP208P", "Pharmaceutical Organic Chemistry I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP209P", "Biochemistry - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP210P", "Computer Applications in Pharmacy - Practical", "practical", 30, 0, 0, 2, 1, True, 10, 15, 25),
            ]),
            3: ("Semester III", "24", [
                ("BP301T", "Pharmaceutical Organic Chemistry II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP302T", "Physical Pharmaceutics I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP303T", "Pharmaceutical Microbiology - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP304T", "Pharmaceutical Engineering - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP305P", "Pharmaceutical Organic Chemistry II - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP306P", "Physical Pharmaceutics I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP307P", "Pharmaceutical Microbiology - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP308P", "Pharmaceutical Engineering - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
            ]),
            4: ("Semester IV", "28", [
                ("BP401T", "Pharmaceutical Organic Chemistry III - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP402T", "Medicinal Chemistry I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP403T", "Physical Pharmaceutics II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP404T", "Pharmacology I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP405T", "Pharmacognosy and Phytochemistry I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP406P", "Medicinal Chemistry I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP407P", "Physical Pharmaceutics II - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP408P", "Pharmacology I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP409P", "Pharmacognosy and Phytochemistry I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
            ]),
            5: ("Semester V", "26", [
                ("BP501T", "Medicinal Chemistry II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP502T", "Industrial Pharmacy I - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP503T", "Pharmacology II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP504T", "Pharmacognosy and Phytochemistry II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP505T", "Pharmaceutical Jurisprudence - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP506P", "Industrial Pharmacy I - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP507P", "Pharmacology II - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP508P", "Pharmacognosy and Phytochemistry II - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
            ]),
            6: ("Semester VI", "30", [
                ("BP601T", "Medicinal Chemistry III - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP602T", "Pharmacology III - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP603T", "Herbal Drug Technology - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP604T", "Biopharmaceutics and Pharmacokinetics - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP605T", "Pharmaceutical Biotechnology - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP606T", "Pharmaceutical Quality Assurance - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP607P", "Medicinal Chemistry III - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP608P", "Pharmacology III - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP609P", "Herbal Drug Technology - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
            ]),
            7: ("Semester VII", "24", [
                ("BP701T", "Instrumental Methods of Analysis - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP702T", "Industrial Pharmacy II - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP703T", "Pharmacy Practice - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP704T", "Novel Drug Delivery Systems - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP705P", "Instrumental Methods of Analysis - Practical", "practical", 60, 0, 0, 4, 2, False, 15, 35, 50),
                ("BP706PS", "Practice School", "practice_school", 150, 0, 0, 12, 6, True, 25, 125, 150),
            ]),
            8: ("Semester VIII", "22", [
                ("BP801T", "Biostatistics and Research Methodology - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP802T", "Social and Preventive Pharmacy - Theory", "theory", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP803ET", "Pharma Marketing Management - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP804ET", "Pharmaceutical Regulatory Science - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP805ET", "Pharmacovigilance - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP806ET", "Quality Control and Standardization of Herbals - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP807ET", "Computer Aided Drug Design - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP808ET", "Cell and Molecular Biology - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP809ET", "Cosmetic Science - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP810ET", "Pharmacological Screening Methods - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP811ET", "Advanced Instrumentation Techniques - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP812ET", "Dietary Supplements and Nutraceuticals - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP813ET", "Pharmaceutical Product Development - Theory", "elective", 45, 3, 1, 0, 4, False, 25, 75, 100),
                ("BP813PW", "Project Work", "project_work", 150, 0, 0, 12, 6, False, 0, 150, 150),
            ]),
        }

        for sem_num, (sem_name, credits_str, subjects) in semesters_data.items():
            semester, _ = Semester.objects.update_or_create(
                curriculum=curriculum,
                semester_number=sem_num,
                defaults={"name": sem_name, "total_credits": credits_str},
            )
            for idx, (code, name, cat, hrs, l_hr, t_hr, p_hr, cred, nue, int_m, end_m, tot_m) in enumerate(subjects, start=1):
                subj, _ = Subject.objects.update_or_create(
                    slug=slugify(f"{code}-{name}"),
                    defaults={
                        "semester": semester,
                        "code": code,
                        "name": name,
                        "category": cat,
                        "total_hours": hrs,
                        "lecture_hours_per_week": l_hr,
                        "tutorial_hours_per_week": t_hr,
                        "practical_hours_per_week": p_hr,
                        "credits": cred,
                        "is_non_university_exam": nue,
                        "internal_marks": int_m,
                        "end_sem_marks": end_m,
                        "total_marks": tot_m,
                        "display_order": idx,
                        "is_active": True,
                    },
                )
                # Ensure default units exist for Theory/Elective (5 Units) or Practical (1 Lab Module)
                if cat in ("theory", "elective", "remedial_theory"):
                    max_units = 3 if code == "BP206T" else 5
                    for u_num in range(1, max_units + 1):
                        Unit.objects.get_or_create(
                            subject=subj,
                            unit_number=u_num,
                            defaults={
                                "title": f"Unit {u_num}",
                                "hours": 10 if u_num <= 3 else 8,
                                "display_order": u_num,
                            },
                        )
                elif cat in ("practical", "remedial_practical"):
                    Unit.objects.get_or_create(
                        subject=subj,
                        unit_number=1,
                        defaults={
                            "title": "Laboratory Experiments",
                            "hours": hrs,
                            "display_order": 1,
                        },
                    )

        self.stdout.write(self.style.SUCCESS("Successfully seeded all 8 Semesters and 75+ PCI B.Pharm Subjects!"))