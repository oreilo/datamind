import pandas as pd
import pytest
from datamind.ingest import read_table
def test_csv(tmp_path):
    p=tmp_path/"sample.csv";p.write_text("x,y\n1,2\n3,4\n");assert read_table(p).shape==(2,2)
def test_unsupported(tmp_path):
    p=tmp_path/"x.exe";p.write_text("hi")
    with pytest.raises(ValueError):read_table(p)
