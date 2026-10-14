"""Connection metadata without ever serializing credentials."""
from dataclasses import dataclass
from urllib.parse import urlsplit
@dataclass(frozen=True)
class ConnectionInfo:
    dialect:str
    host:str
    database:str
    def to_dict(self):return vars(self)
def inspect_url(url:str):
    parts=urlsplit(url)
    return ConnectionInfo(parts.scheme.split('+')[0],parts.hostname or 'local',parts.path.lstrip('/') or ':memory:')
