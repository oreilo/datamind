import httpx
class DataMindClient:
    def __init__(self,base_url="http://127.0.0.1:8000",api_key="",timeout=60):
        self.client=httpx.Client(base_url=base_url,headers={"X-API-Key":api_key},timeout=timeout)
    def __enter__(self):return self
    def __exit__(self,*args):self.client.close()
    def datasets(self):r=self.client.get("/api/datasets");r.raise_for_status();return r.json()
    def upload(self,path):
        from pathlib import Path
        with open(path,"rb") as f:r=self.client.post("/api/datasets",files={"file":(Path(path).name,f)})
        r.raise_for_status();return r.json()
    def analyze(self,id,operation,**kwargs):r=self.client.post(f"/api/datasets/{id}/analyze",json={"operation":operation,**kwargs});r.raise_for_status();return r.json()
    def ask(self,id,question):r=self.client.post(f"/api/datasets/{id}/ask",json={"question":question});r.raise_for_status();return r.json()
