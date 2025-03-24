from base.base_model import BaseModel, db

# ---------------------------
# Academic Data
# ---------------------------
class Course(BaseModel):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    
    # Relationships
    subjects = db.relationship('Subject', backref='course', lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)