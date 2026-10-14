"""Expanded analytics endpoints, isolated from the original API surface."""
import os
from pathlib import Path
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from .api import auth,frame
from .statistics.advanced import regression,clusters,anomalies,forecast
from .engineering.cleaning import transform
from .engineering.validation import validate
from .visualization.specs import spec
from .workspace.projects import Workspace
from .agents.team import AnalysisTeam
from .connectors.sql import validate_query
router=APIRouter(prefix='/api/v2',dependencies=[Depends(auth)],tags=['Advanced analytics'])
class Regression(BaseModel):features:list[str];target:str
class Clustering(BaseModel):columns:list[str];count:int=Field(3,ge=2,le=30)
class Anomaly(BaseModel):columns:list[str];contamination:float=Field(.05,gt=0,le=.5)
class Forecast(BaseModel):date_column:str;value_column:str;periods:int=Field(6,ge=1,le=60)
class Transform(BaseModel):steps:list[dict]
class Validate(BaseModel):rules:list[dict]
class Visual(BaseModel):kind:str;x:str;y:str|None=None
class Research(BaseModel):question:str=Field(min_length=3,max_length=3000)
class ProjectIn(BaseModel):name:str=Field(min_length=1,max_length=200)
class SavedQueryIn(BaseModel):name:str;question:str
class SqlIn(BaseModel):sql:str
workspace=Workspace(os.getenv('DATAMIND_WORKSPACE_DB','./data/workspace.sqlite3'))
def checked(func,*args,**kwargs):
    try:return func(*args,**kwargs)
    except (ValueError,KeyError,TypeError) as exc:raise HTTPException(422,str(exc)) from exc
@router.post('/datasets/{id}/regression')
def regression_api(id:str,body:Regression):return checked(regression,frame(id),body.features,body.target)
@router.post('/datasets/{id}/clusters')
def clusters_api(id:str,body:Clustering):return checked(clusters,frame(id),body.columns,body.count)
@router.post('/datasets/{id}/anomalies')
def anomalies_api(id:str,body:Anomaly):return checked(anomalies,frame(id),body.columns,body.contamination)
@router.post('/datasets/{id}/forecast')
def forecast_api(id:str,body:Forecast):return checked(forecast,frame(id),body.date_column,body.value_column,body.periods)
@router.post('/datasets/{id}/transform')
def transform_api(id:str,body:Transform):
    df,audit=checked(transform,frame(id),body.steps)
    return {'rows':len(df),'columns':list(df.columns),'audit':audit,'preview':df.head(20).fillna('').astype(str).to_dict('records'),'note':'Non-destructive preview. Original dataset is unchanged.'}
@router.post('/datasets/{id}/validate')
def validation_api(id:str,body:Validate):return checked(validate,frame(id),body.rules)
@router.post('/datasets/{id}/visualization')
def visualization_api(id:str,body:Visual):return checked(spec,frame(id),body.kind,body.x,body.y)
@router.post('/datasets/{id}/agent-analysis')
def agent_analysis_api(id:str,body:Research):
    try:return AnalysisTeam().run(frame(id),body.question)
    except Exception as exc:
        from .intelligence.llm import ModelError
        if isinstance(exc,ModelError):raise HTTPException(503,str(exc)) from exc
        if isinstance(exc,(ValueError,KeyError)):raise HTTPException(422,str(exc)) from exc
        raise
@router.post('/sql/validate')
def sql_validate(body:SqlIn):return {'query':checked(validate_query,body.sql),'allowed':True}
@router.get('/projects')
def projects():return workspace.projects()
@router.post('/projects')
def create_project(body:ProjectIn):return workspace.create_project(body.name)
@router.get('/projects/{id}/queries')
def queries(id:str):return workspace.queries(id)
@router.post('/projects/{id}/queries')
def save_query(id:str,body:SavedQueryIn):return checked(workspace.save_query,id,body.name,body.question)
