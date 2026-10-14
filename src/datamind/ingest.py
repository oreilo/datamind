from pathlib import Path
import pandas as pd
from .config import MAX_ROWS
EXTENSIONS = {".csv", ".xlsx", ".xlsm", ".json", ".parquet"}
def read_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() not in EXTENSIONS: raise ValueError("Unsupported file type")
    suffix = path.suffix.lower()
    if suffix == ".csv": df = pd.read_csv(path, nrows=MAX_ROWS+1)
    elif suffix in {".xlsx", ".xlsm"}: df = pd.read_excel(path, engine="openpyxl")
    elif suffix == ".json": df = pd.read_json(path)
    else: df = pd.read_parquet(path)
    if len(df) > MAX_ROWS: raise ValueError(f"Dataset exceeds {MAX_ROWS} rows")
    if len(df.columns) > 500: raise ValueError("Dataset exceeds 500 columns")
    df.columns = [str(c) for c in df.columns]
    if len(set(df.columns)) != len(df.columns): raise ValueError("Duplicate column names")
    return df
