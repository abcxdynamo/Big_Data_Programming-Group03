# from base.base_model import BaseModel, db

# # ---------------------------
# # Academic Data
# # ---------------------------
# class Course(BaseModel):
#     __tablename__ = 'courses'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     code = db.Column(db.String(20), unique=True)
    
#     # Relationships
#     subjects = db.relationship('Subject', backref='course', lazy=True)
#     enrollments = db.relationship('Enrollment', backref='course', lazy=True)

# class Subject(BaseModel):
#     __tablename__ = 'subjects'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
#     # Relationships
#     grades = db.relationship('Grade', backref='subject', lazy=True)
#     attendance = db.relationship('Attendance', backref='subject', lazy=True)

# # ---------------------------
# # Student Progress Tracking
# # ---------------------------
# class Grade(BaseModel):
#     __tablename__ = 'grades'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
#     score = db.Column(db.Float, nullable=False)
#     term = db.Column(db.String(20))  # e.g., "Fall 2023"

# class Attendance(BaseModel):
#     __tablename__ = 'attendance'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     status = db.Column(db.String(10))  # Present/Absent

# # ---------------------------
# # Analytics & Predictions
# # ---------------------------
# class PerformanceMetrics(BaseModel):
#     __tablename__ = 'performance_metrics'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     gpa = db.Column(db.Float)
#     attendance_rate = db.Column(db.Float)
#     last_updated = db.Column(db.DateTime)

# class CoopEligibility(BaseModel):
#     __tablename__ = 'coop_eligibility'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     is_eligible = db.Column(db.Boolean)
#     predicted_success_rate = db.Column(db.Float)
#     eligibility_criteria = db.Column(db.JSON)  # e.g., {"min_gpa": 3.0, "min_attendance": 80}

# class CareerRecommendation(BaseModel):
#     __tablename__ = 'career_recommendations'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     career_title = db.Column(db.String(100))
#     confidence_score = db.Column(db.Float)
#     basis = db.Column(db.String(200))  # e.g., "Strong performance in Data Structures"

# # ---------------------------
# # Support Tables
# # ---------------------------
# class Media(BaseModel):
#     __tablename__ = 'media'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     file_path = db.Column(db.String(200))
#     file_type = db.Column(db.String(20))  # Profile, Report, etc.

# class Enrollment(BaseModel):
#     __tablename__ = 'enrollments'
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
#     status = db.Column(db.String(20))  # Enrolled/Completed