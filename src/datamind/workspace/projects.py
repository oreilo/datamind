"""SQLite-backed project and saved query metadata."""
import sqlite3,json,uuid
from pathlib import Path
class Workspace:
    def __init__(self,path):
        self.path=str(path);Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY,name TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
            db.execute('CREATE TABLE IF NOT EXISTS saved_queries(id TEXT PRIMARY KEY,project_id TEXT NOT NULL,name TEXT NOT NULL,question TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)')
    def connect(self):return sqlite3.connect(self.path)
    def create_project(self,name):
        id=str(uuid.uuid4())
        with self.connect() as db:db.execute('INSERT INTO projects(id,name) VALUES (?,?)',(id,name))
        return {'id':id,'name':name}
    def projects(self):
        with self.connect() as db:return [{'id':id,'name':name} for id,name in db.execute('SELECT id,name FROM projects ORDER BY created_at DESC')]
    def save_query(self,project_id,name,question):
        id=str(uuid.uuid4())
        with self.connect() as db:
            if not db.execute('SELECT 1 FROM projects WHERE id=?',(project_id,)).fetchone():raise ValueError('Project not found')
            db.execute('INSERT INTO saved_queries(id,project_id,name,question) VALUES (?,?,?,?)',(id,project_id,name,question))
        return {'id':id,'project_id':project_id,'name':name,'question':question}
    def queries(self,project_id):
        with self.connect() as db:return [{'id':id,'name':name,'question':question} for id,name,question in db.execute('SELECT id,name,question FROM saved_queries WHERE project_id=?',(project_id,))]
