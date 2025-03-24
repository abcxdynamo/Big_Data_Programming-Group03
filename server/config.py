# server info
from datetime import datetime
import models
from base.base_model import db
from models.user import User
from models.user_role import UserRole
from models.course import Course
from models.subject import Subject
from models.grade import Grade
from models.attendance import Attendance
from models.enrollment import Enrollment
import pydoc

SERVER_PORT = 5001
REGISTER_SERVER_NAME = "performa"

SECRET_KEY = "ABCX_PERFORMA"

DB_URI = "mssql+pyodbc://@ROOZ\\ANUSQL/performa1?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# don't submit next line when set to True
FIRST_RUN = False


def init_database(_app):
    with _app.app_context():
        db.drop_all()
        db.create_all()
        UserRole.save_all(
            UserRole(id=1, name="STUDENT"),
            UserRole(id=2, name="PROFESSOR"),
            UserRole(id=3, name="ADMIN"),
        )

        User.save_all(
            User(email="cchen7166@conestogac.on.ca", first_name="Ce", last_name="Chen", role_id=1),
            User(email="mila@conestogac.on.ca", first_name="Xiaoman", last_name="Yang", role_id=1),
            User(email="hubin@conestogac.on.ca", first_name="Bin", last_name="Hu", role_id=1),
            User(email="abala@conestogac.on.ca", first_name="Anuroopa", last_name="Balachandran", role_id=1),
            User(email="cchen71666@conestogac.on.ca", first_name="Jomis", last_name="X", role_id=2),
            User(email="cchen716666@conestogac.on.ca", first_name="Admin", last_name="X", role_id=3),
        )
        
        # 3. Create Courses
        Course.save_all(
            Course(name="Computer Science", code="CS101"),
            Course(name="Mathematics", code="MATH101"),
            Course(name="Business Administration", code="BUS201")
        )

        # ======================
        # 4. Create Subjects
        # ======================
        cs_course = Course.query.filter_by(code="CS101").first()
        Subject.save_all(
            Subject(name="Algorithms", course_id=cs_course.id),
            Subject(name="Database Systems", course_id=cs_course.id),
            Subject(name="Operating Systems", course_id=cs_course.id)
        )

        # ======================
        # 5. Create Enrollments
        # ======================
        students = User.query.filter_by(role_id=1).all()
        for student in students:
            db.session.add(Enrollment(
                student_id=student.id,
                course_id=cs_course.id,
                status="Enrolled"
            ))

        # ======================
        # 6. Create Grades
        # ======================
        algorithms = Subject.query.filter_by(name="Algorithms").first()
        Grade.save_all(
            Grade(student_id=students[0].id, subject_id=algorithms.id, score=85.0, term="Fall 2023"),
            Grade(student_id=students[1].id, subject_id=algorithms.id, score=78.5, term="Fall 2023"),
            Grade(student_id=students[2].id, subject_id=algorithms.id, score=92.0, term="Fall 2023")
        )

        # ======================
        # 7. Create Attendance
        # ======================
        Attendance.save_all(
            Attendance(student_id=students[0].id, subject_id=algorithms.id, date=datetime(2023, 9, 10), status="Present"),
            Attendance(student_id=students[1].id, subject_id=algorithms.id, date=datetime(2023, 9, 10), status="Absent"),
            Attendance(student_id=students[2].id, subject_id=algorithms.id, date=datetime(2023, 9, 10), status="Present")
        )

        # ======================
        # 8. Create Media
        # ======================
        # Media.save_all(
        #     Media(user_id=students[0].id, file_path="", file_type="profile"),
        #     Media(user_id=students[1].id, file_path="", file_type="profile")
        # )

        # # ======================
        # # 9. Performance Metrics
        # # ======================
        # for student in students:
        #     PerformanceMetrics.save_all(
        #         student_id=student.id,
        #         gpa=3.8,
        #         attendance_rate=95.0
        #     )

        # # ======================
        # # 10. Co-op Eligibility
        # # ======================
        # CoopEligibility.save_all(
        #     student_id=students[0].id,
        #     is_eligible=True,
        #     predicted_success_rate=0.85,
        #     eligibility_criteria={"min_gpa": 3.5, "min_attendance": 90}
        # )

        # # ======================
        # # 11. Career Recommendations
        # # ======================
        # CareerRecommendation.save_all(
        #     student_id=students[0].id,
        #     career_title="Software Engineer",
        #     confidence_score=0.92,
        #     basis="Exceptional performance in Algorithms and Database Systems"
        # )
        
    pass
