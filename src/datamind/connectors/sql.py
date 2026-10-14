"""Read-only SQL access with strict single-statement guards and result limits."""
import re
from sqlalchemy import create_engine, text, inspect
FORBIDDEN = re.compile(r"\b(insert|update|delete|drop|alter|create|truncate|grant|revoke|merge|execute|exec|call|copy|attach|detach|pragma|vacuum|replace|into|load_extension)\b",re.I)
class UnsafeQuery(ValueError):pass
def validate_query(sql:str)->str:
    clean=sql.strip().rstrip(';').strip()
    if not clean or ';' in clean or '--' in clean or '/*' in clean or not re.match(r'^select\b',clean,re.I) or FORBIDDEN.search(clean):
        raise UnsafeQuery('Only a single read-only SELECT statement is allowed')
    return clean
def query(url:str,sql:str,parameters:dict|None=None,limit:int=1000):
    if not 1<=limit<=10000:raise ValueError('limit must be 1..10000')
    clean=validate_query(sql)
    engine=create_engine(url,pool_pre_ping=True)
    try:
        with engine.connect() as con:
            with con.begin():
                result=con.execute(text(f'SELECT * FROM ({clean}) AS datamind_readonly LIMIT :dm_limit'),{**(parameters or {}),'dm_limit':limit})
                return {'columns':list(result.keys()),'rows':[dict(row._mapping) for row in result.fetchall()]}
    finally:engine.dispose()
def schema(url:str):
    engine=create_engine(url,pool_pre_ping=True)
    try:
        inspector=inspect(engine)
        return {table:[{'name':c['name'],'type':str(c['type']),'nullable':c.get('nullable',True)} for c in inspector.get_columns(table)] for table in inspector.get_table_names()}
    finally:engine.dispose()
