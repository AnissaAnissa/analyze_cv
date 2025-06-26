from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class CVInput(BaseModel):
    text:str
@app.post("/analyse")
def analyse_cv(data:CVInput):
    return{
        "message":"bien",
        "contenu":data.text
    }
