from fastapi import FastAPI
import json
import uvicorn
from utils.database import execute_query_json

app = FastAPI()

@app.get("/")
async def root():
    query = "SELECT * from pokereports.MESSAGES"
    result = await execute_query_json(query)
    result_dict = json.loads(result)
    return result_dict

@app.get("/api/version")
async def version():
    return { "version": "0.1.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)