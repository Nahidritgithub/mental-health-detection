# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ====== CONFIG ======
DATA_PATH = "combined_data_2_cleaned.xlsx"   # your dataset file
MODEL_PATH = "model.joblib"   # output model file

# ====== LOAD DATA ======
df = pd.read_excel(DATA_PATH)

# auto-detect columns
statement_col = df.select_dtypes(include="object").columns[0]
status_col = df.columns[1] 
#if df.columns[1] == statement_col else df.columns[1]

print(f"Detected statement column: {statement_col}")
print(f"Detected status column: {status_col}")

# ====== CLEAN DATA ======
df = df[[statement_col, status_col]].dropna()
df.columns = ["statement", "status"]

# ====== SPLIT ======
X_train, X_test, y_train, y_test = train_test_split(
    df["statement"], df["status"], test_size=0.2, random_state=42, stratify=df["status"]
)

# ====== MODEL PIPELINE ======
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=20000)),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# ====== TRAIN ======
print("Training model...")
model.fit(X_train, y_train)

# ====== EVALUATE ======
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ====== SAVE MODEL ======
joblib.dump(model, MODEL_PATH)
print(f"\n✅ Model saved successfully as {MODEL_PATH}")