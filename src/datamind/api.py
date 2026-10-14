import json,uuid
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header, Query
from fastapi.responses import Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import select
from . import config
from .db import SessionLocal, Dataset, Analysis, init_db
from .ingest import read_table, EXTENSIONS
from .analytics import analyze, answer_question
from .charts import plot
from .reports import render_report

app=FastAPI(title="OREiLO DataMind",version="1.0.0",docs_url="/api/docs",openapi_url="/api/openapi.json")
if config.ALLOWED_ORIGINS:app.add_middleware(CORSMiddleware,allow_origins=config.ALLOWED_ORIGINS,allow_methods=["GET","POST","DELETE"],allow_headers=["Authorization","X-API-Key","Content-Type"])
@app.on_event("startup")
def startup():init_db()
def auth(x_api_key:str|None=Header(None)):
    if not config.API_KEY:raise HTTPException(503,"DATAMIND_API_KEY must be configured")
    import hmac
    if not x_api_key or not hmac.compare_digest(x_api_key,config.API_KEY):raise HTTPException(401,"Invalid API key")

def get_dataset(id):
    with SessionLocal() as db:
        row=db.get(Dataset,id)
        if not row:raise HTTPException(404,"Dataset not found")
        return {"id":row.id,"name":row.name,"filename":row.filename,"path":row.path,"rows":row.rows,"columns":row.columns,"created_at":row.created_at.isoformat() if row.created_at else None}
def frame(id):return read_table(get_dataset(id)["path"])
class Operation(BaseModel):
    operation:str
    column:str|None=None
    group_by:str|None=None
    top:int=Field(default=20,ge=1,le=100)
class Question(BaseModel):question:str=Field(min_length=3,max_length=2000)
class Chart(BaseModel):kind:str;x:str;y:str|None=None
@app.get("/health")
def health():return {"status":"ok","product":"OREiLO DataMind"}
@app.get("/",response_class=HTMLResponse)
def index():return (Path(__file__).parent/"static"/"index.html").read_text(encoding="utf-8")
@app.post("/api/datasets",dependencies=[Depends(auth)])
async def upload(file:UploadFile=File(...)):
    filename=Path(file.filename or "").name
    suffix=Path(filename).suffix.lower()
    if suffix not in EXTENSIONS:raise HTTPException(400,"Unsupported file type")
    id=str(uuid.uuid4());target=config.UPLOAD_DIR/f"{id}{suffix}";size=0
    try:
        with target.open("wb") as output:
            while chunk:=await file.read(1024*1024):
                size+=len(chunk)
                if size>config.MAX_UPLOAD_MB*1024*1024:raise ValueError("Upload exceeds size limit")
                output.write(chunk)
        df=read_table(target)
        with SessionLocal() as db:
            db.add(Dataset(id=id,name=filename,filename=filename,path=str(target),rows=len(df),columns=len(df.columns)));db.commit()
        return {"id":id,"name":filename,"rows":len(df),"columns":len(df.columns)}
    except Exception as e:
        target.unlink(missing_ok=True)
        raise HTTPException(400,str(e))
@app.get("/api/datasets",dependencies=[Depends(auth)])
def list_datasets():
    with SessionLocal() as db:
        return [{"id":r.id,"name":r.name,"rows":r.rows,"columns":r.columns} for r in db.scalars(select(Dataset).order_by(Dataset.created_at.desc())).all()]
@app.get("/api/datasets/{id}",dependencies=[Depends(auth)])
def dataset(id:str):
    row=get_dataset(id);row.pop("path");return row
@app.delete("/api/datasets/{id}",dependencies=[Depends(auth)])
def delete_dataset(id:str):
    with SessionLocal() as db:
        row=db.get(Dataset,id)
        if not row:raise HTTPException(404,"Dataset not found")
        path=Path(row.path)
        for a in db.scalars(select(Analysis).where(Analysis.dataset_id==id)).all():db.delete(a)
        db.delete(row);db.commit();path.unlink(missing_ok=True)
    return {"deleted":id}
@app.get("/api/datasets/{id}/preview",dependencies=[Depends(auth)])
def preview(id:str,limit:int=Query(20,ge=1,le=100)):
    df=frame(id).head(limit)
    return json.loads(df.to_json(orient="records",date_format="iso"))
@app.post("/api/datasets/{id}/analyze",dependencies=[Depends(auth)])
def run_analysis(id:str,body:Operation):
    try:return analyze(frame(id),body.operation,body.column,body.group_by,body.top)
    except ValueError as e:raise HTTPException(422,str(e))
@app.post("/api/datasets/{id}/ask",dependencies=[Depends(auth)])
def ask(id:str,body:Question):
    try:result=answer_question(frame(id),body.question)
    except ValueError as e:raise HTTPException(422,str(e))
    with SessionLocal() as db:
        row=Analysis(id=str(uuid.uuid4()),dataset_id=id,question=body.question,result=json.dumps(result,default=str));db.add(row);db.commit()
    return result
@app.get("/api/datasets/{id}/history",dependencies=[Depends(auth)])
def history(id:str):
    get_dataset(id)
    with SessionLocal() as db:
        return [{"id":a.id,"question":a.question,"result":json.loads(a.result),"created_at":a.created_at.isoformat() if a.created_at else None} for a in db.scalars(select(Analysis).where(Analysis.dataset_id==id).order_by(Analysis.created_at.desc()).limit(100)).all()]
@app.post("/api/datasets/{id}/chart",dependencies=[Depends(auth)])
def chart(id:str,body:Chart):
    try:png=plot(frame(id),body.kind,body.x,body.y)
    except (ValueError,TypeError) as e:raise HTTPException(422,str(e))
    return Response(png,media_type="image/png")
@app.get("/api/datasets/{id}/report",dependencies=[Depends(auth)])
def report(id:str,fmt:str="pdf"):
    if fmt not in {"pdf","docx","html","md","json"}:raise HTTPException(422,"Unsupported format")
    row=get_dataset(id)
    payload={"dataset":{k:v for k,v in row.items() if k!="path"},"profile":analyze(frame(id),"profile")}
    data,mime=render_report(f"DataMind Report: {row['name']}",payload,fmt)
    return Response(data,media_type=mime,headers={"Content-Disposition":f'attachment; filename="datamind-report.{fmt}"'})

from .api_extended import router as advanced_router
app.include_router(advanced_router)
