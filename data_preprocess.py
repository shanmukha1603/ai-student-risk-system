import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Load dataset
data = pd.read_csv("student_data.csv")

# Clean column names
data.columns = data.columns.str.strip()

# Set target column
target_column = "Exam_Score"

# Fill missing values
numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

# Fill text/categorical columns
text_cols = data.select_dtypes(include=['object', 'string']).columns
data[text_cols] = data[text_cols].fillna("Unknown")

# Separate features and target
X = data.drop(target_column, axis=1)
y = data[target_column]

# Convert categorical/text columns to numeric using one-hot encoding
X = pd.get_dummies(X, columns=text_cols, drop_first=True)

# Scale numeric features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Save scaler
joblib.dump(scaler, "scaler.pkl")

print("Preprocessing complete!")
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
