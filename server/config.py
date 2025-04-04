# server info
from base.base_model import db
from models import User, Term, Program, Course, TermProgramCourse, Enrollment, Grade
from models import UserRole

SERVER_PORT = 5001
REGISTER_SERVER_NAME = "performa"

SECRET_KEY = "ABCX_PERFORMA"

DB_HOST = '34.130.133.219'
DB_PORT = 3306
DB_USER = 'performa'
DB_PASSWORD = 'QWER1234'
DB_NAME = 'performa'
DB_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# don't submit next line when set to True
FIRST_RUN = False


def init_database(_app):
    with _app.app_context():
        db.drop_all()
        db.create_all()
        UserRole.save_all(
            UserRole(id=1, name="STUDENT"),
            UserRole(id=2, name="INSTRUCTOR"),
            UserRole(id=3, name="ADMIN"),
        )

        User.save_all(
            User(id=1, email="admin@conestogac.on.ca", first_name="Admin", last_name="", role_id=3),
            User(id=2, email="cc@conestogac.on.ca", first_name="Ce", last_name="Chen", role_id=1),
            User(id=3, email="mila@conestogac.on.ca", first_name="Mila", last_name="Yang", role_id=1),
            User(id=4, email="hubin@conestogac.on.ca", first_name="Bin", last_name="Hu", role_id=1),
            User(id=5, email="anuroopa@conestogac.on.ca", first_name="Anuroopa", last_name="Balachandran", role_id=1),
            User(id=6, email="alex@conestogac.on.ca", first_name="Alex", last_name="", role_id=2),
            User(id=7, email="eric@conestogac.on.ca", first_name="Eric", last_name="", role_id=2),
            User(id=8, email="jomis@conestogac.on.ca", first_name="Jomis", last_name="", role_id=2),
            User(id=9, email="amrita@conestogac.on.ca", first_name="Amrita", last_name="", role_id=2),
            User(id=10, email="ahmed@conestogac.on.ca", first_name="Ahmed", last_name="", role_id=2),
        )

        Term.save_all(
            Term(id=1, year=2025, season="Winter", section=1, start_date='2025-01-01', end_date='2025-04-30'),
        )

        Program.save_all(
            Program(id=1, code="1448", name="Big Data Solution Architecture", co_op=True)
        )

        Course.save_all(
            Course(id=1, code="PROG8401", name="Relational Database Design"),
            Course(id=2, code="PROG8411", name="NoSQL Database Implementation"),
            Course(id=3, code="PROG8421", name="Programming for Big Data"),
            Course(id=4, code="PROG8441", name="Software Quality"),
            Course(id=5, code="PROG8461", name="Web Analytics and Business Intelligence Tools"),
        )

        TermProgramCourse.save_all(
            TermProgramCourse(id=1, term_id=1, program_id=1, course_id=1, instructor_id=6),
            TermProgramCourse(id=2, term_id=1, program_id=1, course_id=2, instructor_id=7),
            TermProgramCourse(id=3, term_id=1, program_id=1, course_id=3, instructor_id=8),
            TermProgramCourse(id=4, term_id=1, program_id=1, course_id=4, instructor_id=9),
            TermProgramCourse(id=5, term_id=1, program_id=1, course_id=5, instructor_id=10),
        )

        Enrollment.save_all(
            Enrollment(student_id=2, term_id=1, program_id=1),
            Enrollment(student_id=3, term_id=1, program_id=1),
            Enrollment(student_id=4, term_id=1, program_id=1),
            Enrollment(student_id=5, term_id=1, program_id=1),
        )

        Grade.save_all(
            Grade(student_id=2, term_id=1, program_id=1, course_id=1, final_grade=10.0),
            Grade(student_id=2, term_id=1, program_id=1, course_id=2, final_grade=11.0),
            Grade(student_id=2, term_id=1, program_id=1, course_id=3, final_grade=12.0),
            Grade(student_id=2, term_id=1, program_id=1, course_id=4, final_grade=13.0),
            Grade(student_id=2, term_id=1, program_id=1, course_id=5, final_grade=14.0),
            Grade(student_id=3, term_id=1, program_id=1, course_id=1, final_grade=30.0),
            Grade(student_id=3, term_id=1, program_id=1, course_id=2, final_grade=31.0),
            Grade(student_id=3, term_id=1, program_id=1, course_id=3, final_grade=32.0),
            Grade(student_id=3, term_id=1, program_id=1, course_id=4, final_grade=33.0),
            Grade(student_id=3, term_id=1, program_id=1, course_id=5, final_grade=34.0),
            Grade(student_id=4, term_id=1, program_id=1, course_id=1, final_grade=20.0),
            Grade(student_id=4, term_id=1, program_id=1, course_id=2, final_grade=21.0),
            Grade(student_id=4, term_id=1, program_id=1, course_id=3, final_grade=22.0),
            Grade(student_id=4, term_id=1, program_id=1, course_id=4, final_grade=23.0),
            Grade(student_id=4, term_id=1, program_id=1, course_id=5, final_grade=24.0),
            Grade(student_id=5, term_id=1, program_id=1, course_id=1, final_grade=40.0),
            Grade(student_id=5, term_id=1, program_id=1, course_id=2, final_grade=41.0),
            Grade(student_id=5, term_id=1, program_id=1, course_id=3, final_grade=42.0),
            Grade(student_id=5, term_id=1, program_id=1, course_id=4, final_grade=43.0),
            Grade(student_id=5, term_id=1, program_id=1, course_id=5, final_grade=44.0),
        )
    pass
