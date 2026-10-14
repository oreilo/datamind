import pandas as pd
import pytest
from datamind.engineering.cleaning import transform
from datamind.engineering.validation import validate
from datamind.statistics.advanced import regression,clusters,anomalies,forecast
from datamind.connectors.sql import validate_query,UnsafeQuery
from datamind.visualization.specs import spec
from datamind.governance.masking import mask_text,mask_records
from datamind.integrations.webhooks import sign,validate_destination
from datamind.workspace.projects import Workspace
from datamind.jobs.runner import JobRunner
from datamind.intelligence.planner import plan
from datamind.agents.team import AnalysisTeam
@pytest.fixture
def df():return pd.DataFrame({'date':pd.date_range('2024-01-01',periods=12,freq='MS'),'x':range(12),'y':[2*i+1 for i in range(12)],'segment':['a','b']*6})
def test_transform(df):
    out,audit=transform(df,[{'operation':'rename','column':'segment','target':'category'},{'operation':'uppercase','column':'category'}]);assert out.category.iloc[0]=='A' and len(audit)==2
def test_validation(df):assert validate(df,[{'type':'required','column':'x'},{'type':'unique','column':'x'}])['passed']
def test_regression(df):assert regression(df,['x'],'y')['r2']>.99
def test_clusters(df):assert sum(clusters(df,['x','y'],2)['sizes'].values())==12
def test_anomalies(df):assert anomalies(df,['x','y'])['total']==12
def test_forecast(df):assert len(forecast(df,'date','y',3)['forecast'])==3
def test_chart(df):assert spec(df,'line','x','y')['mark']=='line'
@pytest.mark.parametrize('sql',['DELETE FROM users','SELECT * FROM x; DROP TABLE x','WITH t AS (DELETE FROM x) SELECT * FROM t','SELECT * FROM x -- comment'])
def test_unsafe_sql(sql):
    with pytest.raises(UnsafeQuery):validate_query(sql)
def test_safe_sql():assert validate_query(' SELECT name FROM products; ')=='SELECT name FROM products'
def test_mask():assert '[EMAIL]' in mask_text('test@example.com') and mask_records([{'email':'a'}],['email'])[0]['email']=='[REDACTED]'
def test_webhook():
    assert len(sign({'ok':True},'secret'))==64
    with pytest.raises(ValueError):validate_destination('http://localhost',{'localhost'})
def test_workspace(tmp_path):
    ws=Workspace(tmp_path/'workspace.db');project=ws.create_project('Demo');ws.save_query(project['id'],'Test','Revenue?');assert len(ws.queries(project['id']))==1
def test_job():
    import time
    runner=JobRunner();id=runner.submit(lambda:42)
    for _ in range(100):
        if runner.get(id).status=='completed':break
        time.sleep(.01)
    assert runner.get(id).result==42
def test_planner(df):
    class Fake:
        def chat(self,messages):return '{"steps":[{"operation":"profile","column":null}],"explanation":"overview"}'
    assert len(plan('overview',list(df.columns),Fake())['steps'])==1
    assert AnalysisTeam(Fake()).run(df,'overview')['findings']
