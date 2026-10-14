import os
os.environ.setdefault("DATAMIND_API_KEY","test-key")
from fastapi.testclient import TestClient
from datamind.api import app
from datamind.db import init_db
init_db()
client=TestClient(app)
def test_health():assert client.get('/health').json()['status']=='ok'
def test_auth():assert client.get('/api/datasets').status_code==401
def test_upload_and_analyze():
    h={'X-API-Key':'test-key'}
    r=client.post('/api/datasets',headers=h,files={'file':('sample.csv',b'region,revenue\nA,10\nB,20\n','text/csv')});assert r.status_code==200,r.text
    id=r.json()['id'];r=client.post(f'/api/datasets/{id}/analyze',headers=h,json={'operation':'profile'});assert r.json()['rows']==2
    r=client.post(f'/api/datasets/{id}/ask',headers=h,json={'question':'average revenue'});assert r.json()['value']==15
    assert client.get(f'/api/datasets/{id}/report?fmt=pdf',headers=h).status_code==200
    assert client.delete(f'/api/datasets/{id}',headers=h).status_code==200
