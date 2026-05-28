# Mapping each feature to a recommendation
recommendation_map = {
    "Hours_Studied": "Increase study hours for better academic performance.",
    "Attendance": "Attend classes regularly to improve learning outcomes.",
    "Parental_Involvement": "Engage parents in student progress and activities.",
    "Access_to_Resources": "Ensure access to learning materials and resources.",
    "Extracurricular_Activities": "Participate in extracurriculars for overall growth.",
    "Sleep_Hours": "Maintain proper sleep schedule for better focus and concentration.",
    "Previous_Scores": "Review past exams and work on weak areas.",
    "Motivation_Level": "Set achievable goals and practice motivation techniques.",
    "Internet_Access": "Ensure reliable internet access for online learning.",
    "Tutoring_Sessions": "Attend tutoring sessions for subjects you struggle with.",
    "Family_Income": "Seek scholarships or support programs if needed.",
    "Teacher_Quality": "Communicate with teachers regularly to clarify doubts.",
    "School_Type": "Leverage available school programs and resources.",
    "Peer_Influence": "Surround yourself with positive and motivated peers.",
    "Physical_Activity": "Engage in regular physical activity to reduce stress and improve focus.",
    # Add remaining 15 features for your 30-feature dataset
}

# Define risky thresholds per feature (customize based on your dataset)
risky_thresholds = {
    "Hours_Studied": lambda x: x < 2,
    "Attendance": lambda x: x < 70,
    "Sleep_Hours": lambda x: x < 6,
    "Motivation_Level": lambda x: x <= 1,  # if encoded 0,1,2
    "Internet_Access": lambda x: x == 0,   # 0=no, 1=yes
    "Previous_Scores": lambda x: x < 50,
    "Physical_Activity": lambda x: x < 2,  # hours per week
    # Add thresholds for all features in your dataset
}

def get_student_recommendations(student_data, feature_names):
    """
    student_data: list of feature values for one student
    feature_names: list of feature names in order
    Returns a list of recommendations only for risky features
    """
    recs = []
    for i, feature in enumerate(feature_names):
        value = student_data[i]
        if feature in risky_thresholds and risky_thresholds[feature](value):
            recs.append(f"{feature}: {recommendation_map[feature]}")
    return recs
