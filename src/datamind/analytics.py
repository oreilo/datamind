import math
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def clean(value):
    if isinstance(value, (np.integer,)): return int(value)
    if isinstance(value, (np.floating,)): value = float(value)
    if isinstance(value, float) and not math.isfinite(value): return None
    if isinstance(value, (pd.Timestamp,)): return value.isoformat()
    if pd.isna(value) if not isinstance(value, (dict, list, tuple, np.ndarray)) else False: return None
    return value

def profile(df: pd.DataFrame):
    columns=[]
    for col in df.columns:
        s=df[col]
        record={"name":col,"dtype":str(s.dtype),"missing":int(s.isna().sum()),"unique":int(s.nunique(dropna=True)),"sample":[clean(v) for v in s.dropna().head(5).tolist()]}
        if pd.api.types.is_numeric_dtype(s):
            record["stats"]={k:clean(v) for k,v in {"mean":s.mean(),"median":s.median(),"std":s.std(),"min":s.min(),"max":s.max(),"sum":s.sum()}.items()}
        columns.append(record)
    return {"rows":len(df),"columns":len(df.columns),"duplicates":int(df.duplicated().sum()),"column_details":columns}

def analyze(df:pd.DataFrame, operation:str, column:str|None=None, group_by:str|None=None, top:int=20):
    if column and column not in df: raise ValueError("Unknown column")
    if group_by and group_by not in df: raise ValueError("Unknown grouping column")
    top=max(1,min(top,100))
    if operation == "profile": return profile(df)
    if operation == "correlation":
        nums=df.select_dtypes(include="number")
        return {"columns":nums.columns.tolist(),"matrix":nums.corr().replace({np.nan:None}).to_dict()}
    if operation == "missing": return {"missing":{str(k):int(v) for k,v in df.isna().sum().items()}}
    if operation == "describe":
        if not column: raise ValueError("column required")
        return {"column":column,"summary":{str(k):clean(v) for k,v in df[column].describe().items()}}
    if operation == "frequency":
        if not column: raise ValueError("column required")
        return {"column":column,"values":[{"value":clean(k),"count":int(v)} for k,v in df[column].value_counts(dropna=False).head(top).items()]}
    if operation == "group":
        if not column or not group_by: raise ValueError("column and group_by required")
        if not pd.api.types.is_numeric_dtype(df[column]): raise ValueError("Aggregation column must be numeric")
        grouped=df.groupby(group_by,dropna=False)[column].agg(["sum","mean","count"]).head(top)
        return {"group_by":group_by,"metric":column,"values":[{"group":clean(idx),"sum":clean(row["sum"]),"mean":clean(row["mean"]),"count":int(row["count"])} for idx,row in grouped.iterrows()]}
    if operation == "outliers":
        if not column or not pd.api.types.is_numeric_dtype(df[column]): raise ValueError("Numeric column required")
        s=df[column].dropna()
        if len(s)<4:return {"column":column,"count":0,"indices":[]}
        q1,q3=s.quantile([.25,.75]);iqr=q3-q1
        indices=s[(s<q1-1.5*iqr)|(s>q3+1.5*iqr)].index.tolist()
        return {"column":column,"count":len(indices),"indices":[int(i) if isinstance(i,(int,np.integer)) else str(i) for i in indices[:100]]}
    if operation == "anomalies":
        numeric=df.select_dtypes(include="number").dropna()
        if len(numeric)<10 or numeric.shape[1]==0:raise ValueError("At least 10 complete numeric rows required")
        labels=IsolationForest(random_state=42,contamination=.05).fit_predict(numeric)
        return {"count":int((labels==-1).sum()),"indices":[int(i) if isinstance(i,(int,np.integer)) else str(i) for i in numeric.index[labels==-1][:100]]}
    raise ValueError("Unknown operation")

def answer_question(df:pd.DataFrame,question:str):
    """Deterministic natural-language baseline: no fabricated LLM answers."""
    q=question.lower().strip()
    matches=[c for c in df.columns if c.lower() in q]
    if "missing" in q or "null" in q:return {"operation":"missing","result":analyze(df,"missing"),"method":"deterministic"}
    if "correlat" in q:return {"operation":"correlation","result":analyze(df,"correlation"),"method":"deterministic"}
    if "overview" in q or "profile" in q or "summary" in q:return {"operation":"profile","result":profile(df),"method":"deterministic"}
    if "outlier" in q and matches:return {"operation":"outliers","result":analyze(df,"outliers",matches[0]),"method":"deterministic"}
    if any(x in q for x in ("average","mean","total","sum","median","minimum","maximum")) and matches:
        col=matches[0]
        if not pd.api.types.is_numeric_dtype(df[col]):raise ValueError("Selected column is not numeric")
        mapping={"average":"mean","mean":"mean","total":"sum","sum":"sum","median":"median","minimum":"min","maximum":"max"}
        key=next(k for k in mapping if k in q)
        return {"operation":mapping[key],"column":col,"value":clean(getattr(df[col],mapping[key])()),"method":"deterministic"}
    return {"operation":"unresolved","message":"Question is not covered by the deterministic engine. Use the explicit analysis endpoints; no values were invented.","available_columns":df.columns.tolist(),"method":"deterministic"}
