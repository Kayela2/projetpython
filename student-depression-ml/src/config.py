"""Central configuration: paths, feature lists, and constants shared by all notebooks."""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT_DIR / "dataset" / "student_lifestyle_100k.csv"
MODELS_DIR = ROOT_DIR / "models"
REPORTS_DIR = ROOT_DIR / "reports"

TARGET_COL = "Depression"
ID_COL = "Student_ID"

NUMERIC_FEATURES = [
    "Age",
    "CGPA",
    "Sleep_Duration",
    "Study_Hours",
    "Social_Media_Hours",
    "Physical_Activity",
    "Stress_Level",
]
CATEGORICAL_FEATURES = ["Gender", "Department"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

RANDOM_STATE = 42

# Kernel SVM (libsvm) does not scale to 100k rows in interactive time (O(n^2-2.8)):
# benchmarked ~15-20min for a single fit at 80k rows, which makes GridSearchCV
# (Phase 5) infeasible. We use a stratified subsample for all modeling notebooks;
# the EDA (Phase 1) already ran on the full 100k rows.
SAMPLE_SIZE = 12_000
TEST_SIZE = 0.2
