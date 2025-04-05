import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import config

# Database configuration
# DB_URI = "mssql+pyodbc://@ROOZ\\ANUSQL/PDB1?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(config.DB_URI)

# Conestoga GPA conversion
def grade_to_gpa(grade):
    if grade >= 90: return 4.0
    elif grade >= 85: return 3.9
    elif grade >= 80: return 3.7
    elif grade >= 75: return 3.3
    elif grade >= 70: return 3.0
    elif grade >= 65: return 2.7
    elif grade >= 60: return 2.3
    elif grade >= 55: return 2.0
    elif grade >= 50: return 1.7
    else: return 0.0

def get_training_data():
    """Get historical course-level data for model training"""
    with engine.connect() as conn:
        query = text("""
        SELECT 
            tpc.program_level,
            tpc.credits,
            sga.attendance_percent,
            sga.grade AS final_grade,
            tpc.course_id
        FROM students_grades_archive sga
        JOIN term_program_courses tpc ON sga.tp_course_id = tpc.id
        WHERE sga.grade IS NOT NULL
        """)
        return pd.read_sql(query, conn)

def get_current_courses(term_id):
    """Get current term courses with partial grades"""
    with engine.connect() as conn:
        query = text(f"""
        SELECT
            u.id AS student_id,
            tpc.id AS term_course_id,
            tpc.program_level,
            tpc.credits,
            COALESCE(a.attendance_in_percent, 85.0) AS current_attendance,
            g.final_grade,
            tpc.course_id
        FROM users u
        JOIN enrollments e ON u.id = e.student_id
        JOIN term_program_courses tpc ON e.term_id = tpc.term_id
        JOIN attendance a ON u.id = a.student_id AND a.tp_course_id = tpc.id
        JOIN grades g ON u.id = g.student_id AND g.tp_course_id = tpc.id
        WHERE e.term_id = {term_id}
          AND u.role_id = 1
          AND e.status = 1
        """)
        return pd.read_sql(query, conn)

def predict_and_update_gpa():
    """Main prediction workflow"""
    with engine.connect() as conn:
        # Train model
        train_df = get_training_data()
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', HistGradientBoostingRegressor(
                max_iter=200,
                validation_fraction=0.2,
                random_state=42
            ))
        ])
        model.fit(
            train_df[['program_level', 'credits', 'attendance_percent', 'course_id']],
            train_df['final_grade']
        )

        # Process current terms
        current_terms = pd.read_sql(
            # text("SELECT id FROM terms WHERE GETDATE() BETWEEN start_date AND end_date"),
            text("SELECT id FROM terms WHERE NOW() BETWEEN start_date AND end_date"),
            conn
        )

        for term_id in current_terms['id']:
            current_courses = get_current_courses(term_id)
            predictions = []

            for student_id, courses in current_courses.groupby('student_id'):
                total_credits = 0
                weighted_gpa = 0
                sum_weighted_grade = 0
                sum_total_credit_value = 0
                
                for _, course in courses.iterrows():
                    X = pd.DataFrame([[
                            course['program_level'],
                            course['credits'],
                            course['current_attendance'],
                            course['course_id']
                    ]], columns=['program_level', 'credits', 'attendance_percent', 'course_id'])
                        
                    final_grade = model.predict(X)[0]
                    final_grade = np.clip(final_grade, 0, 100)

                    # Calculate course GPA
                    course_gpa = grade_to_gpa(final_grade)
                    weighted_gpa += course_gpa * course['credits']
                    total_credits += course['credits']
                    # Calculate weighted average components
                    weighted_grade_factor = final_grade * course['credits']
                    total_credit_value = 100 * course['credits']  # Max grade is 100
                    
                    sum_weighted_grade += weighted_grade_factor
                    sum_total_credit_value += total_credit_value

                if total_credits > 0:
                    term_gpa = round(weighted_gpa / total_credits, 2)
                    # Calculate term weighted average
                    weighted_average = round((sum_weighted_grade / sum_total_credit_value)*100,2)
                    predictions.append({
                        'student_id': int(student_id),
                        'term_id': int(term_id),
                        'predicted_gpa': float(term_gpa),
                        'predicted_average': float(weighted_average)
                    })
                    print(weighted_average)

            # Update database
            if predictions:
                SQL_MS_SQL_SERVER = """
                    MERGE INTO performance_predictions AS target
                    USING (VALUES (:student_id, :term_id, :predicted_gpa, :predicted_average)) 
                        AS source (student_id, term_id, predicted_gpa, predicted_average)
                    ON target.student_id = source.student_id 
                        AND target.term_id = source.term_id
                    WHEN MATCHED THEN
                        UPDATE SET 
                            predicted_gpa = source.predicted_gpa,
                            predicted_average = source.predicted_average,
                            update_time = GETDATE()
                    WHEN NOT MATCHED THEN
                        INSERT (student_id, term_id, predicted_gpa, predicted_average)
                        VALUES (source.student_id, source.term_id, 
                                source.predicted_gpa, source.predicted_average);
                """
                SQL_MySQL = """
                    INSERT INTO performance_predictions (student_id, term_id, predicted_gpa, predicted_average, prediction_date, create_time, update_time, is_deleted)
                    VALUES (:student_id, :term_id, :predicted_gpa, :predicted_average, NOW(), NOW(), NOW(), 0)
                    ON DUPLICATE KEY UPDATE
                        predicted_gpa = VALUES(predicted_gpa),
                        predicted_average = VALUES(predicted_average),
                        update_time = NOW();

                """
                conn.execute(
                    text(SQL_MySQL),
                    predictions
                )
                conn.commit()

# if __name__ == "__main__":
#     predict_and_update_gpa()
#     pass