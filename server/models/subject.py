from base.base_model import BaseModel, db

class Subject(BaseModel):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    # Relationships
    grades = db.relationship('Grade', backref='subject', lazy=True)
    attendance = db.relationship('Attendance', backref='subject', lazy=True)

