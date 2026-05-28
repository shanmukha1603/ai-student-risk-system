from flask import Flask, render_template, request, redirect, session
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = "student_risk_key"

# ---------------- LOAD MODEL ----------------

model = joblib.load("student_risk_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- FEATURES ----------------

feature_names = [
    'Hours_Studied',
    'Attendance',
    'Parental_Involvement',
    'Access_to_Resources',
    'Extracurricular_Activities',
    'Sleep_Hours',
    'Previous_Scores',
    'Motivation_Level',
    'Internet_Access',
    'Tutoring_Sessions',
    'Family_Income',
    'Teacher_Quality',
    'School_Type',
    'Peer_Influence',
    'Physical_Activity',
    'Learning_Disabilities',
    'Parental_Education_Level',
    'Distance_from_Home',
    'Gender',
    'Learning_Environment',
    'Health_Status',
    'Stress_Level',
    'Social_Skills',
    'Goal_Setting',
    'Self_Confidence',
    'Class_Participation',
    'Time_Management',
    'Project_Work',
    'Attendance_Pattern',
    'Exam_Score'
]

# ---------------- WELCOME PAGE ----------------

@app.route("/")
def welcome():
    return render_template("welcome.html")

# ---------------- LOGIN PAGE ----------------

@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- STUDENT LOGIN PAGE ----------------

@app.route("/student_login_page")
def student_login_page():
    return render_template("student_login.html")

# ---------------- TEACHER LOGIN PAGE ----------------

@app.route("/teacher_login_page")
def teacher_login_page():
    return render_template("teacher_login.html")

# ---------------- STUDENT LOGIN ----------------

@app.route("/student_login")
def student_login():
    session["role"] = "student"
    return redirect("/student_form")

# ---------------- TEACHER LOGIN ----------------

@app.route("/teacher_login")
def teacher_login():
    session["role"] = "teacher"
    return redirect("/dashboard")

# ---------------- STUDENT FORM ----------------

@app.route("/student_form", methods=["GET", "POST"])
def student_form():

    if session.get("role") != "student":
        return redirect("/")

    if request.method == "POST":

        student_name = request.form.get("student_name")
        student_id = request.form.get("student_id")

        data = []

        for f in feature_names:

            value = request.form.get(f, 0)

            if f == "Gender":

                if str(value).lower() == "male":
                    value = 1

                elif str(value).lower() == "female":
                    value = 0

                else:
                    value = 0

            try:
                value = float(value)

            except:
                value = 0

            data.append(value)

        while len(data) < 30:
            data.append(0)

        data = data[:30]

        scaled_data = scaler.transform([data])

        prediction = float(model.predict(scaled_data)[0])
        prediction = round(prediction, 2)

        # ---------------- RISK ANALYSIS ----------------

        risk_scores = {}

        attendance = float(request.form.get("Attendance", 0))
        study_hours = float(request.form.get("Hours_Studied", 0))
        sleep_hours = float(request.form.get("Sleep_Hours", 0))
        previous_scores = float(request.form.get("Previous_Scores", 0))
        exam_score = float(request.form.get("Exam_Score", 0))
        distance = float(request.form.get("Distance_from_Home", 0))

        risk_scores["Attendance"] = max(0, 100 - attendance)
        risk_scores["Hours Studied"] = max(0, 100 - (study_hours * 10))
        risk_scores["Sleep Hours"] = max(0, 100 - (sleep_hours * 10))
        risk_scores["Previous Scores"] = max(0, 100 - previous_scores)
        risk_scores["Exam Score"] = max(0, 100 - exam_score)
        risk_scores["Distance From Home"] = min(100, distance * 10)

        categorical_features = [
            "Parental_Involvement",
            "Access_to_Resources",
            "Extracurricular_Activities",
            "Motivation_Level",
            "Internet_Access",
            "Family_Income",
            "Teacher_Quality",
            "School_Type",
            "Peer_Influence",
            "Physical_Activity",
            "Learning_Disabilities",
            "Parental_Education_Level",
            "Learning_Environment",
            "Health_Status",
            "Stress_Level",
            "Social_Skills",
            "Goal_Setting",
            "Self_Confidence",
            "Class_Participation",
            "Time_Management",
            "Project_Work",
            "Attendance_Pattern"
        ]

        for feature in categorical_features:

            value = float(request.form.get(feature, 1))

            if value == 0:
                risk = 85

            elif value == 1:
                risk = 50

            else:
                risk = 15

            risk_scores[feature.replace("_", " ")] = risk

        sorted_risks = sorted(
            risk_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        chart_data = []

        for feature, score in sorted_risks[:5]:

            chart_data.append({
                "feature": feature,
                "score": round(score, 2)
            })

        # ---------------- RISK LEVEL ----------------

        highest_risk = sorted_risks[0][1]

        if prediction < 40 and highest_risk < 50:

            risk_level = "Low"
            escalation = "Normal Monitoring"

        elif prediction < 70 or highest_risk < 80:

            risk_level = "Medium"
            escalation = "Teacher Attention Required"

        else:

            risk_level = "High"
            escalation = "Immediate Parent & Teacher Intervention"

        # ---------------- RECOMMENDATIONS ----------------

        recommendations = []
        intervention_plan = []
        mentoring_strategy = []

        for feature, score in sorted_risks[:5]:

            if feature == "Attendance":

                recommendations.append(
                    "Student should improve class attendance and participate regularly."
                )

                intervention_plan.append(
                    "Monitor attendance weekly and notify parents for continuous absenteeism."
                )

                mentoring_strategy.append(
                    "Assign attendance mentor for daily tracking."
                )

            elif feature == "Hours Studied":

                recommendations.append(
                    "Increase daily study hours with a structured study schedule."
                )

                intervention_plan.append(
                    "Provide supervised study planning and revision monitoring."
                )

                mentoring_strategy.append(
                    "Conduct weekly academic mentoring and study planning sessions."
                )

            elif feature == "Sleep Hours":

                recommendations.append(
                    "Maintain healthy sleep habits for improved concentration."
                )

                intervention_plan.append(
                    "Provide awareness on healthy sleep and time management."
                )

                mentoring_strategy.append(
                    "Counsellor should monitor student wellness and stress levels."
                )

            elif feature == "Previous Scores":

                recommendations.append(
                    "Focus on improving weak academic subjects."
                )

                intervention_plan.append(
                    "Arrange extra practice tests and academic support sessions."
                )

                mentoring_strategy.append(
                    "Assign subject mentor for low-performing subjects."
                )

            elif feature == "Exam Score":

                recommendations.append(
                    "Improve exam preparation techniques and revision methods."
                )

                intervention_plan.append(
                    "Conduct mock tests and performance improvement programs."
                )

                mentoring_strategy.append(
                    "Provide exam-oriented mentoring and performance tracking."
                )

            elif feature == "Motivation Level":

                recommendations.append(
                    "Participate in confidence-building and motivational activities."
                )

                intervention_plan.append(
                    "Provide motivational workshops and positive reinforcement."
                )

                mentoring_strategy.append(
                    "Teacher mentor should conduct weekly motivation sessions."
                )

            elif feature == "Parental Involvement":

                recommendations.append(
                    "Parents should engage more actively in academic progress."
                )

                intervention_plan.append(
                    "Increase parent-teacher communication frequency."
                )

                mentoring_strategy.append(
                    "Schedule monthly parent mentoring discussions."
                )

            elif feature == "Internet Access":

                recommendations.append(
                    "Ensure access to online learning resources."
                )

                intervention_plan.append(
                    "Provide digital learning support and internet facilities."
                )

                mentoring_strategy.append(
                    "Guide student toward online educational platforms."
                )

            elif feature == "Learning Disabilities":

                recommendations.append(
                    "Provide specialized learning assistance."
                )

                intervention_plan.append(
                    "Arrange personalized learning support and counselling."
                )

                mentoring_strategy.append(
                    "Assign special educator and individualized mentoring support."
                )

            elif feature == "Stress Level":

                recommendations.append(
                    "Practice stress management and emotional wellness activities."
                )

                intervention_plan.append(
                    "Provide emotional counselling and stress-relief programs."
                )

                mentoring_strategy.append(
                    "Mental wellness mentor should monitor emotional health regularly."
                )

            elif feature == "Distance From Home":

                recommendations.append(
                    "Student may require transportation or hostel support for better attendance."
                )

                intervention_plan.append(
                    "Provide transport assistance or flexible academic support programs."
                )

                mentoring_strategy.append(
                    "Monitor travel-related academic challenges through mentor interaction."
                )

            elif feature == "Access to Resources":

                recommendations.append(
                    "Student should gain better access to academic learning materials."
                )

                intervention_plan.append(
                    "Provide digital resources, library access and study materials."
                )

                mentoring_strategy.append(
                    "Guide student on effective usage of academic resources."
                )

            elif feature == "School Type":

                recommendations.append(
                    "Student may require additional institutional academic support."
                )

                intervention_plan.append(
                    "Provide personalized academic engagement programs."
                )

                mentoring_strategy.append(
                    "Assign faculty mentor for institutional adaptation support."
                )

            elif feature == "Peer Influence":

                recommendations.append(
                    "Student should maintain positive peer interactions and academic focus."
                )

                intervention_plan.append(
                    "Encourage participation in positive peer learning groups."
                )

                mentoring_strategy.append(
                    "Provide peer mentoring and behavioural guidance sessions."
                )

            else:

                recommendations.append(
                    f"Improve performance related to {feature}."
                )

                intervention_plan.append(
                    f"Provide continuous monitoring and support for {feature}."
                )

                mentoring_strategy.append(
                    f"Assign personalized mentoring support for improvement in {feature}."
                )

        recommendations = list(dict.fromkeys(recommendations))
        intervention_plan = list(dict.fromkeys(intervention_plan))
        mentoring_strategy = list(dict.fromkeys(mentoring_strategy))

        # ---------------- SAVE RECORDS ----------------

        file = "student_records.csv"

        previous_score = "No Previous Data"

        if os.path.exists(file) and os.path.getsize(file) > 0:

            df = pd.read_csv(file)

            old = df[df["Student_ID"].astype(str) == str(student_id)]

            if len(old) > 0:
                previous_score = old.iloc[-1]["Current_Risk_Score"]

        else:

            df = pd.DataFrame(columns=[
                "Student_Name",
                "Student_ID",
                "Current_Risk_Score",
                "Previous_Risk_Score",
                "Risk_Level",
                "Intervention_Plan",
                "Mentoring_Strategy"
            ])

        new_record = {
            "Student_Name": student_name,
            "Student_ID": student_id,
            "Current_Risk_Score": prediction,
            "Previous_Risk_Score": previous_score,
            "Risk_Level": risk_level,

            "Intervention_Plan":
            " | ".join(intervention_plan),

            "Mentoring_Strategy":
            " | ".join(mentoring_strategy)
        }

        df = pd.concat(
            [df, pd.DataFrame([new_record])],
            ignore_index=True
        )

        df.to_csv(file, index=False)

        return render_template(
            "result.html",
            student_name=student_name,
            student_id=student_id,
            prediction=prediction,
            risk_level=risk_level,
            escalation=escalation,
            chart_data=chart_data,
            recommendations=recommendations
        )

    return render_template(
        "student_form.html",
        features=feature_names
    )

# ---------------- DASHBOARD ----------------

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if session.get("role") != "teacher":
        return redirect("/")

    file = "student_records.csv"

    if os.path.exists(file) and os.path.getsize(file) > 0:

        df = pd.read_csv(file)

    else:

        df = pd.DataFrame(columns=[
            "Student_Name",
            "Student_ID",
            "Current_Risk_Score",
            "Previous_Risk_Score",
            "Risk_Level",
            "Intervention_Plan",
            "Mentoring_Strategy"
        ])

    if request.method == "POST":

        search_id = request.form.get("student_id")

        if search_id:

            df = df[
                df["Student_ID"].astype(str).str.contains(str(search_id))
            ]

    low = len(df[df["Risk_Level"] == "Low"])
    medium = len(df[df["Risk_Level"] == "Medium"])
    high = len(df[df["Risk_Level"] == "High"])

    chart_data = [low, medium, high]

    records = df.to_dict(orient="records")

    return render_template(
        "dashboard.html",
        records=records,
        chart_data=chart_data
    )

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
