import pandas as pd
data = pd.read_csv("student_data.csv")
# Show all column names
print(data.columns.tolist())
