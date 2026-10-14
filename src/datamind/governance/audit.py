"""Append-only local JSONL audit events; avoid secrets and raw dataset values."""
import json,datetime,threading
from pathlib import Path
_lock=threading.Lock()
def record(path,event:str,subject:str,metadata:dict|None=None):
    data={'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,'subject':subject,'metadata':metadata or {}}
    with _lock:
        target=Path(path);target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('a',encoding='utf8') as f:f.write(json.dumps(data,default=str)+'\n')
    return data
