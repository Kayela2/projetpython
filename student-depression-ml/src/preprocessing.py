"""Preprocessing pipeline shared by every modeling notebook and the backend."""
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import CATEGORICAL_FEATURES, NUMERIC_FEATURES, RANDOM_STATE, TEST_SIZE


def build_preprocessor() -> ColumnTransformer:
    """Numeric features are standardized (required for a distance/kernel-based
    model like SVM). Categorical features are one-hot encoded; binary columns
    (Gender) are collapsed to a single dummy, nominal ones (Department) keep
    all categories since dropping one would bias RBF kernel distances."""
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(drop="if_binary", handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
        ]
    )


def split_data(X, y):
    """Stratified train/test split to preserve the Depression class ratio
    (~8.94:1) in both subsets."""
    return train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
