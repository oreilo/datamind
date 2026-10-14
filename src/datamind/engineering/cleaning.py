"""Deterministic, auditable data cleaning transformations."""
import pandas as pd
ALLOWED={'drop_duplicates','drop_missing','fill_missing','rename','cast','trim','lowercase','uppercase'}
def transform(df:pd.DataFrame,steps:list[dict]):
    out=df.copy();audit=[]
    for step in steps:
        op=step.get('operation');column=step.get('column');before=len(out)
        if op not in ALLOWED:raise ValueError(f'Unsupported transformation: {op}')
        if column is not None and column not in out:raise ValueError(f'Unknown column: {column}')
        if op=='drop_duplicates':out=out.drop_duplicates(subset=[column] if column else None)
        elif op=='drop_missing':out=out.dropna(subset=[column] if column else None)
        elif op=='fill_missing':
            if column is None:raise ValueError('column required')
            out[column]=out[column].fillna(step.get('value'))
        elif op=='rename':
            if column is None or not step.get('target'):raise ValueError('column and target required')
            out=out.rename(columns={column:step['target']})
        elif op=='cast':out[column]=out[column].astype(step['dtype'])
        elif op=='trim':out[column]=out[column].astype('string').str.strip()
        elif op=='lowercase':out[column]=out[column].astype('string').str.lower()
        elif op=='uppercase':out[column]=out[column].astype('string').str.upper()
        audit.append({'operation':op,'rows_before':before,'rows_after':len(out),'column':column})
    return out,audit
