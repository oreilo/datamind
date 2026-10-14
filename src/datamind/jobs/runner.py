"""Thread-based local jobs with state transitions and cancellation signals."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass,field
from threading import Lock,Event
from uuid import uuid4
from datetime import datetime,timezone
@dataclass
class Job:
    id:str
    status:str='queued'
    result:object=None
    error:str|None=None
    cancelled:Event=field(default_factory=Event,repr=False)
class JobRunner:
    def __init__(self,workers:int=2):self.pool=ThreadPoolExecutor(max_workers=workers);self.jobs={};self.lock=Lock()
    def submit(self,fn,*args,**kwargs):
        job=Job(str(uuid4()))
        with self.lock:self.jobs[job.id]=job
        def work():
            if job.cancelled.is_set():job.status='cancelled';return
            job.status='running'
            try:
                result=fn(*args,**kwargs)
                if job.cancelled.is_set():job.status='cancelled'
                else:job.result=result;job.status='completed'
            except Exception as exc:job.error=f'{type(exc).__name__}: {exc}';job.status='failed'
        self.pool.submit(work)
        return job.id
    def get(self,id):return self.jobs.get(id)
    def cancel(self,id):
        job=self.get(id)
        if not job:return False
        job.cancelled.set()
        if job.status=='queued':job.status='cancelled'
        return True
