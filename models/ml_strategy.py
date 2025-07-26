import pandas as pd
from sklearn.linear_model import LogisticRegression

class MLStrategy:
    """Simple ML-based strategy using logistic regression."""

    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X: pd.DataFrame, y: pd.Series):
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> pd.Series:
        preds = self.model.predict(X)
        return pd.Series(preds, index=X.index)
