import json
from pathlib import Path
import typer
from .ingest import read_table
from .analytics import profile,answer_question
app=typer.Typer(help="OREiLO DataMind - local analytics CLI")
@app.command()
def inspect(file:Path):typer.echo(json.dumps(profile(read_table(file)),indent=2,default=str))
@app.command()
def ask(file:Path,question:str):typer.echo(json.dumps(answer_question(read_table(file),question),indent=2,default=str))
@app.command()
def serve(host:str="127.0.0.1",port:int=8000):
    import uvicorn
    uvicorn.run("datamind.api:app",host=host,port=port)
if __name__=="__main__":app()
