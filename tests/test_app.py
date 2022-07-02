from xml.dom.minidom import TypeInfo
from fastapi.testclient import TestClient
#import os, sys
#sys.path.insert(1, os.path.join(sys.path[0], '..'))
from app import *
#python -m pytest tests/

client = TestClient(app)

def test_listdir():
    result = listdir()
    assert type(result) is list

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    
