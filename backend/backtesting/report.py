import pandas as pd


def compute_drawdown(equity_curve: pd.Series) -> pd.Series:
    cum_max = equity_curve.cummax()
    drawdown = (equity_curve - cum_max) / cum_max
    return drawdown


def export_report(equity_df: pd.DataFrame, path: str):
    """Save equity curve and drawdown to CSV."""
    equity_df = equity_df.copy()
    equity_df['drawdown'] = compute_drawdown(equity_df['equity'])
    equity_df.to_csv(path, index=False)
    print(f"📈 Report exported to {path}")
