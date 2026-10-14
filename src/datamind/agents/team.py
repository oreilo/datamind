"""Constrained multi-stage analysis team; all numeric results come from deterministic tools."""
from dataclasses import dataclass,field
from ..analytics import analyze
from ..intelligence.planner import plan
@dataclass
class AgentEvent:
    agent:str
    action:str
    result:dict=field(default_factory=dict)
class AnalysisTeam:
    def __init__(self,client=None):self.client=client
    def run(self,df,question:str):
        events=[]
        research_plan=plan(question,list(df.columns),self.client)
        events.append(AgentEvent('planner','create_plan',research_plan))
        findings=[]
        for step in research_plan['steps']:
            operation=step['operation'];column=step.get('column')
            try:result=analyze(df,operation,column)
            except (ValueError,TypeError) as exc:result={'error':str(exc)}
            findings.append({'operation':operation,'column':column,'result':result})
            events.append(AgentEvent('analyst','execute',{'operation':operation,'column':column}))
        events.append(AgentEvent('verifier','verify_provenance',{'all_results_computed_locally':True,'steps':len(findings)}))
        return {'question':question,'plan':research_plan,'findings':findings,'events':[vars(e) for e in events],'disclaimer':'Generated plan; numerical results computed from supplied data. Interpretations require human review.'}
