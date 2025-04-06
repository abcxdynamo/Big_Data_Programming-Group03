from base.base_model import db_execute
from models import User, UserRole, Enrollment, Term, Program, TermProgramCourse, Course, Grade
from models import UserToken
from utils.common import send_email
from utils.auth import generate_jwt_token, decode_jwt_token
from utils.time import utcnow

class CourseService:
    @staticmethod
    def get_student_enrollment(student_id):
        return (Enrollment.query
                .filter_by(student_id=student_id, status=1)
                .first())

    @staticmethod
    def get_term(term_id):
        return Term.query.filter_by(id=term_id).first()

    @staticmethod
    def get_program(program_id):
        return Program.query.filter_by(id=program_id).first()

    @staticmethod
    def get_term_program_course_list(term_id, program_id, student_id):
        return (
        TermProgramCourse.query
        .join(Grade, (Grade.tp_course_id == TermProgramCourse.id) & (Grade.student_id == student_id))
        .filter(TermProgramCourse.term_id == term_id, TermProgramCourse.program_id == program_id).all()
    )
           
    @staticmethod
    def get_course(course_id):
        return Course.query.filter_by(id=course_id).first()

    @staticmethod
    def query_course_list(query=None):
        if query is None:
            query = {}
        ids = query.get('ids')
        if not ids or len(ids) == 0:
            return []
        if isinstance(ids, str):
            # ids = list(map(int, ids.split(',')))
            ids = [int(x.strip()) for x in ids.split(',')]
        elif isinstance(ids, list):
            pass
        else:
            raise TypeError('ids must be a string or a list of ints')

        return Course.query.filter(Course.id.in_(ids)).all()

    @staticmethod
    def query_grades(term_id, program_id, student_id=None, course_id=None):
        conditions = [
            "tpc.term_id=:term_id",
            "tpc.program_id=:program_id",
        ]
        filters = {
            "term_id": term_id,
            "program_id": program_id,
        }
        if student_id is not None:
            filters["student_id"] = student_id
            conditions.append("g.student_id=:student_id")
        if course_id is not None:
            filters["course_id"] = course_id
            conditions.append("tpc.course_id=:course_id")
        sql = f"""
            select 
                g.*
            from grades g
            join term_program_courses tpc on g.tp_course_id = tpc.id
            where {" and ".join(conditions)}
        """
        return db_execute(sql, filters)
    
    @staticmethod
    def query_attendance(term_id, program_id, student_id=None, course_id=None):
        conditions = [
            "tpc.term_id=:term_id",
            "tpc.program_id=:program_id",
        ]
        filters = {
            "term_id": term_id,
            "program_id": program_id,
        }
        if student_id is not None:
            filters["student_id"] = student_id
            conditions.append("a.student_id=:student_id")
        if course_id is not None:
            filters["course_id"] = course_id
            conditions.append("tpc.course_id=:course_id")
        sql = f"""
            select 
                a.*
            from attendance a
            join term_program_courses tpc on a.tp_course_id = tpc.id
            where {" and ".join(conditions)}
        """
        return db_execute(sql, filters)

    @staticmethod
    def query_instructor_courses(query=None):
        conditions = []
        if query is None:
            query = {}
        if query.get('instructor_id'):
            conditions.append("instructor_id=:instructor_id")
        if not conditions or len(conditions) == 0:
            conditions = ["1=1"]
        conditions.append("CURRENT_TIMESTAMP BETWEEN t.start_date AND t.end_date")
        sql = f"""
            select 
                tpc.id,
                tpc.term_id,
                tpc.instructor_id,
                t.year term_year,
                t.season term_season,
                t.section term_section,
                tpc.program_id,
                p.code program_code,
                p.name program_name,
                tpc.course_id,
                c.code course_code,
                c.name course_name
            from term_program_courses tpc
            join terms t on tpc.term_id=t.id
            join programs p on tpc.program_id=p.id
            join courses c on tpc.course_id=c.id
            where {" and ".join(conditions)}
        """
        return db_execute(sql, query)

    @staticmethod
    def query_student_grades(query=None):
        if query is None:
            query = {}
        conditions = []
        if query.get("instructor_id"):
            conditions.append("instructor_id=:instructor_id")
        if query.get("term_id"):
            conditions.append("term_id=:term_id")
        if query.get("program_id"):
            conditions.append("program_id=:program_id")
        if query.get("course_id"):
            conditions.append("course_id=:course_id")
        if query.get("student_id"):
            conditions.append("student_id=:student_id")
        if query.get("student_name"):
            conditions.append("student_name like %:student_name%")
        if query.get("email"):
            conditions.append("email like %:email%")
        if query.get("course_name"):
            conditions.append("course_name like %:course_name%")
        if query.get("term_name"):
            conditions.append("(term_code like %:term_name% or term_code like %:term_code%)")
        if conditions is None or len(conditions) == 0:
            conditions = ["1=1"]
        conditions.append("CURRENT_TIMESTAMP BETWEEN t.start_date AND t.end_date")
        sql = f"""
            select 
                tpc.id,
                tpc.term_id,
                t.year term_year,
                t.season term_season,
                t.section term_section,
                tpc.program_id,
                p.code program_code,
                p.name program_name,
                tpc.course_id,
                c.code course_code,
                c.name course_name,
                e.student_id,
                g.id grade_id,
                g.final_grade,
                g.final_gpa,
                g.feedback grade_feedback
            from term_program_courses tpc
            join terms t on tpc.term_id=t.id
            join programs p on tpc.program_id=p.id
            join courses c on tpc.course_id=c.id
            join enrollments e on tpc.term_id=e.term_id and tpc.program_id=e.program_id
            join grades g on e.student_id=g.student_id and tpc.id=g.tp_course_id
            join users ins on tpc.instructor_id=ins.id
            join users stu on e.student_id=stu.id
            where {" and ".join(conditions)}
            order by student_id, term_id, program_id, course_id

        """
        return db_execute(sql, query)

    @staticmethod
    def save_grade_feedback(grade_id, feedback):
        grade = Grade.query.filter_by(id=grade_id).first()
        grade.feedback = feedback
        grade.save()

    # @staticmethod
    # def get_student_enrollment_info(student_id):
    #     enrollment = (Enrollment.query
    #                   .filter_by(student_id=student_id, status=1)
    #                   .first())
    #     term_id = enrollment.term_id
    #     program_id = enrollment.program_id
    #     term = Term.query.filter_by(id=term_id).first()
    #     program = Program.query.filter_by(id=program_id).first()
    #     courses = (TermProgramCourse.query
    #      .filter_by(term_id=term_id, program_id=program_id)
    #      .all())
