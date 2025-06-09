import os
import pandas as pd
from datetime import datetime

def export_ohlcv_to_csv(symbol: str, interval: str, df: pd.DataFrame):
    """Exports OHLCV DataFrame to a CSV file in the exports/ folder."""
    # Prepare export directory
    folder_path = os.path.join("exports", interval)
    os.makedirs(folder_path, exist_ok=True)

    # Format filename
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{symbol}_{interval}_{now}.csv"
    file_path = os.path.join(folder_path, filename)

    # Save CSV
    df.to_csv(file_path, index=False)
    print(f"💾 Exported to {file_path}")
