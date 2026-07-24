"""Dataset loading and stratified subsampling."""
import pandas as pd
from sklearn.model_selection import train_test_split

from .config import DATASET_PATH, FEATURES, TARGET_COL, SAMPLE_SIZE, RANDOM_STATE


def load_dataset() -> pd.DataFrame:
    """Load the full raw dataset (100k rows) from disk."""
    return pd.read_csv(DATASET_PATH)


def get_modeling_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Stratified subsample used for all SVM notebooks, preserving the
    Depression class ratio observed in the full dataset (see config.SAMPLE_SIZE)."""
    if SAMPLE_SIZE >= len(df):
        return df
    sample, _ = train_test_split(
        df,
        train_size=SAMPLE_SIZE,
        random_state=RANDOM_STATE,
        stratify=df[TARGET_COL],
    )
    return sample.reset_index(drop=True)


def get_X_y(df: pd.DataFrame):
    """Split a dataframe into feature matrix X and target vector y."""
    X = df[FEATURES].copy()
    y = df[TARGET_COL].astype(int)
    return X, y
