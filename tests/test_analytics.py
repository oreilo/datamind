import pandas as pd
import pytest
from datamind.analytics import profile,analyze,answer_question
@pytest.fixture
def data():return pd.DataFrame({"region":["A","B","A","B"],"revenue":[10,20,30,40],"cost":[1,2,3,4]})
def test_profile(data):assert profile(data)["rows"]==4
def test_group(data):assert analyze(data,"group","revenue","region")["values"][0]["sum"]==40
def test_mean(data):assert answer_question(data,"average revenue")["value"]==25
def test_unknown(data):assert answer_question(data,"predict my future")["operation"]=="unresolved"
def test_missing(data):assert analyze(data,"missing")["missing"]["region"]==0
def test_correlation(data):assert analyze(data,"correlation")["matrix"]["revenue"]["cost"]==1.0
def test_bad_column(data):
    with pytest.raises(ValueError):analyze(data,"describe","wrong")
