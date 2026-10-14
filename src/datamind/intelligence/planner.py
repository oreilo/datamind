"""Structured, constrained LLM analysis plans."""
import json,re
from .llm import ModelClient
ALLOWED={'profile','summary','correlation','missing','outliers','value_counts'}
def plan(question:str,columns:list[str],client:ModelClient|None=None):
    client=client or ModelClient()
    instructions='Return ONLY JSON object {"steps":[{"operation":"profile|summary|correlation|missing|outliers|value_counts","column":null}],"explanation":"..."}. Use only supplied columns and operations. Never output executable code.'
    raw=client.chat([{'role':'system','content':instructions},{'role':'user','content':json.dumps({'question':question,'columns':columns})}])
    match=re.search(r'\{.*\}',raw,re.S)
    if not match:raise ValueError('Model did not return JSON')
    obj=json.loads(match.group());steps=obj.get('steps',[])
    if not isinstance(steps,list) or len(steps)>12:raise ValueError('Invalid plan length')
    for step in steps:
        if step.get('operation') not in ALLOWED or (step.get('column') is not None and step['column'] not in columns):raise ValueError('Unsafe or invalid analysis plan')
    return {'steps':steps,'explanation':str(obj.get('explanation',''))}
