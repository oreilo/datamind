"""Optional OpenAI-compatible LLM adapter. No provider required for deterministic analytics."""
import os,httpx
class ModelError(RuntimeError):pass
class ModelClient:
    def __init__(self,base_url=None,api_key=None,model=None,timeout=45):
        self.base_url=(base_url or os.getenv('DATAMIND_LLM_BASE_URL','')).rstrip('/')
        self.api_key=api_key or os.getenv('DATAMIND_LLM_API_KEY','')
        self.model=model or os.getenv('DATAMIND_LLM_MODEL','')
        self.timeout=timeout
        if not self.base_url or not self.model:raise ModelError('Set DATAMIND_LLM_BASE_URL and DATAMIND_LLM_MODEL')
    def chat(self,messages:list[dict],temperature:float=0):
        headers={'Content-Type':'application/json'}
        if self.api_key:headers['Authorization']=f'Bearer {self.api_key}'
        try:
            with httpx.Client(timeout=self.timeout,follow_redirects=False) as client:
                response=client.post(self.base_url+'/chat/completions',headers=headers,json={'model':self.model,'messages':messages,'temperature':temperature});response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except (httpx.HTTPError,KeyError,IndexError,TypeError) as exc:raise ModelError(f'LLM request failed: {type(exc).__name__}') from exc
