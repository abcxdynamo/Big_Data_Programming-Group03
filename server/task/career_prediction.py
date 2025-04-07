import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import config
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Database engine
engine = create_engine(config.DB_URI)


def get_training_career_data():
    """Fetch alumni data used for training the model."""
    with engine.connect() as conn:
        query = text("""
            SELECT
                sa.program_id,
                sa.cgpa,
                sa.career
            FROM students_archive sa
            WHERE sa.career IS NOT NULL
              AND sa.cgpa IS NOT NULL
              AND sa.program_id IS NOT NULL
              AND sa.career != 'others'
        """)
        return pd.read_sql(query, conn)


# def get_student_gpa_program(student_id):
#     """Fetch the current GPA and program ID of a student."""
#     with engine.connect() as conn:
#         query = text(f"""
#             SELECT TOP 1
#                 e.program_id,
#                 COALESCE(ROUND(AVG(g.final_grade), 2), 0.0) AS current_gpa
#             FROM users u
#             JOIN enrollments e ON u.id = e.student_id
#             LEFT JOIN grades g ON u.id = g.student_id
#             WHERE u.id = :student_id
#             GROUP BY e.program_id
#             HAVING COUNT(g.final_grade) > 0
#         """)
#         result = pd.read_sql(query, conn, params={"student_id": student_id})
#         return result.iloc[0] if not result.empty else None


def train_career_model(archived_data):
    """Train the RandomForest model for career prediction."""
    archived_data = archived_data.copy()
    scaler = MinMaxScaler()
    archived_data['normalized_gpa'] = scaler.fit_transform(archived_data[['cgpa']])
    
    le = LabelEncoder()
    archived_data['career_encoded'] = le.fit_transform(archived_data['career'])

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(archived_data[['program_id', 'normalized_gpa']], archived_data['career_encoded'])

    return model, scaler, le


def predict_career_path(student_id, program_id, current_gpa):
    """Main method to predict career path for a student."""
    try:
        # Get student academic info
        student = pd.Series({'program_id': program_id, 'current_gpa': current_gpa})
        if student is None:
            return ["Insufficient academic records for predictions"]

        archived_data = get_training_career_data()
        if archived_data.empty or len(archived_data) < 10:
            return ["More alumni data needed for accurate prediction"]

        model, scaler, le = train_career_model(archived_data)

        # Normalize student's GPA and predict
        normalized_gpa = scaler.transform([[student['current_gpa']]])[0][0]
        features = [[student['program_id'], normalized_gpa]]
        predicted = model.predict(features)[0]
        predicted_label = le.inverse_transform([predicted])[0]

        return (f"{predicted_label}")

    except Exception as e:
        print(f"[Career Prediction Error] {str(e)}")

# if __name__ == "__main__":
#     test_id = 1  # Replace with actual student_id
#     results = predict_career_path(test_id)
#     for line in format_suggestions(results):
#         print(line)
