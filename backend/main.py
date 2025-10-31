import sys
import os
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

# Add the parent directory (Insights/) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import pandas as pd
from analyze_insights import validate_dataset, clean_dataset, train_model
from create_gpt_prompt import generate_gpt_prompt
from gpt_utils import ask_gpt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

latest_model_info = None
latest_df = None

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),  # tells FastAPI to expect a file field
    target_column: str = Form(...) # tells FastAPI to expect something from a form
):
    contents = await file.read()

    # Convert bytes into a pandas DataFrame
    try:
        df = pd.read_csv(pd.io.common.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")
   
    errors = validate_dataset(df, target_column)
    if errors:
        raise HTTPException(status_code=400, detail=errors)

    X_clean, y = clean_dataset(df, target_column)
    result = train_model(X_clean, y, target_column)

    global latest_model_info, latest_df
    latest_model_info = result
    latest_df = df

    return result


@app.post("/ask")
async def ask(question: str = Form(...)):
    global latest_model_info, latest_df
    if not latest_model_info or latest_df is None:
        raise HTTPException(status_code=400, detail="No model has been analyzed yet.")

    prompt = generate_gpt_prompt(latest_model_info, latest_df, question)
    answer = ask_gpt(prompt)
    return {"answer": answer}

