"""Reproducible advanced statistical analysis."""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.metrics import r2_score
def regression(df,x:list[str],y:str):
    data=df[x+[y]].apply(pd.to_numeric,errors='coerce').dropna()
    if len(data)<3:raise ValueError('At least 3 complete rows required')
    model=LinearRegression().fit(data[x],data[y]);pred=model.predict(data[x])
    return {'samples':len(data),'features':x,'target':y,'coefficients':dict(zip(x,map(float,model.coef_))),'intercept':float(model.intercept_),'r2':float(r2_score(data[y],pred))}
def clusters(df,columns:list[str],count:int=3):
    data=df[columns].apply(pd.to_numeric,errors='coerce').dropna()
    if not 2<=count<=len(data):raise ValueError('Cluster count must be 2..number of complete rows')
    model=KMeans(n_clusters=count,n_init=10,random_state=42).fit(data)
    return {'count':count,'sizes':pd.Series(model.labels_).value_counts().sort_index().to_dict(),'centers':[dict(zip(columns,map(float,row))) for row in model.cluster_centers_]}
def anomalies(df,columns:list[str],contamination:float=.05):
    data=df[columns].apply(pd.to_numeric,errors='coerce').dropna()
    if len(data)<5:raise ValueError('At least 5 complete rows required')
    if not 0<contamination<=.5:raise ValueError('contamination must be between 0 and 0.5')
    labels=IsolationForest(contamination=contamination,random_state=42).fit_predict(data)
    return {'total':len(data),'anomaly_count':int((labels==-1).sum()),'row_indices':data.index[labels==-1].tolist()}
def forecast(df,date_column:str,value_column:str,periods:int=6,freq:str='MS'):
    if not 1<=periods<=60:raise ValueError('periods must be 1..60')
    frame=df[[date_column,value_column]].copy();frame[date_column]=pd.to_datetime(frame[date_column],errors='coerce');frame[value_column]=pd.to_numeric(frame[value_column],errors='coerce');frame=frame.dropna().sort_values(date_column)
    if len(frame)<4:raise ValueError('At least 4 valid observations required')
    x=np.arange(len(frame)).reshape(-1,1);model=LinearRegression().fit(x,frame[value_column]);future=np.arange(len(frame),len(frame)+periods).reshape(-1,1)
    dates=pd.date_range(frame[date_column].max(),periods=periods+1,freq=freq)[1:]
    return {'method':'linear_trend_extrapolation','warning':'Baseline projection, not a validated forecasting model','forecast':[{'date':d.isoformat(),'value':float(v)} for d,v in zip(dates,model.predict(future))]}
