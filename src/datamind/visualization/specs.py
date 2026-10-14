"""Framework-independent Vega-Lite compatible chart specifications."""
import pandas as pd
ALLOWED={'bar','line','point','area','tick'}
def spec(df:pd.DataFrame,kind:str,x:str,y:str|None=None,limit:int=500):
    if kind not in ALLOWED:raise ValueError('Unsupported chart kind')
    if x not in df or (y and y not in df):raise ValueError('Unknown column')
    columns=[x]+([y] if y else []);data=df[columns].head(limit).copy()
    data=data.where(pd.notna(data),None)
    encoding={'x':{'field':x,'type':'quantitative' if pd.api.types.is_numeric_dtype(df[x]) else 'nominal'}}
    if y:encoding['y']={'field':y,'type':'quantitative' if pd.api.types.is_numeric_dtype(df[y]) else 'nominal'}
    else:encoding['y']={'aggregate':'count','type':'quantitative'}
    return {'$schema':'https://vega.github.io/schema/vega-lite/v5.json','mark':kind,'data':{'values':data.astype(object).to_dict('records')},'encoding':encoding}
