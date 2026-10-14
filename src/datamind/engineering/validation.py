"""Schema and quality checks that return actionable findings."""
import pandas as pd
def validate(df:pd.DataFrame,rules:list[dict]):
    results=[]
    for rule in rules:
        op=rule['type'];col=rule.get('column');ok=True;violations=0
        if col and col not in df:raise ValueError(f'Unknown column: {col}')
        if op=='required':violations=int(df[col].isna().sum())
        elif op=='unique':violations=int(df[col].duplicated().sum())
        elif op=='minimum':violations=int((pd.to_numeric(df[col],errors='coerce')<rule['value']).sum())
        elif op=='maximum':violations=int((pd.to_numeric(df[col],errors='coerce')>rule['value']).sum())
        elif op=='allowed':violations=int((~df[col].isin(rule['values'])).sum())
        elif op=='min_rows':violations=max(0,int(rule['value'])-len(df))
        else:raise ValueError(f'Unknown rule: {op}')
        results.append({'rule':rule,'passed':violations==0,'violations':violations})
    return {'passed':all(x['passed'] for x in results),'results':results}
