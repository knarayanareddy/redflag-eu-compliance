from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title="RedFlag — EU Product-Safety Pre-Flight Compliance Gate",
    description="Find out in 8 seconds whether the EU will let you sell your product — pre-flight screening against Regulation (EU) 2023/988 (GPSR), semantic recall matching against 20 years of EU Safety Gate data, and Sandbox-verified marketplace packs.",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}

@app.get("/v1/info")
def get_info():
    return {
        "project": "RedFlag — EU Product-Safety Pre-Flight Compliance Gate",
        "track": "Best Apps and Agents (Eligible for Best Use of Tavily $3,000)",
        "models": {
            "ultra": settings.model_ultra,
            "super": settings.model_super,
            "nano": settings.model_nano
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
