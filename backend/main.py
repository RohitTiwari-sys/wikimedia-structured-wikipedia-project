from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="Wikipedia Dataset Project")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Wikipedia dataset
DATA_PATH = "../data/wikipedia_cleaned.parquet"
df = pd.read_parquet(DATA_PATH)


@app.get("/")
def home():
    return {"message": "Wikipedia Dataset API is running!"}


@app.get("/articles")
def get_articles():
    return df[["name", "description", "abstract", "url"]].head(10).to_dict(
        orient="records"
    )


@app.get("/stats")
def get_stats():
    return {
        "total_articles": len(df),
        "total_columns": len(df.columns)
    }
@app.get("/search")
def search_articles(q: str):
    results = df[
        df["name"].str.contains(q, case=False, na=False)
    ].head(10)

    return results.to_dict(orient="records")    