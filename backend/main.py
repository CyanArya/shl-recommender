from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from backend.recommender import AssessmentRecommender
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="API for recommending SHL assessments based on job descriptions or queries",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize recommender
recommender = AssessmentRecommender()

class AssessmentResponse(BaseModel):
    assessment_name: str
    assessment_url: str
    remote_testing_support: str
    adaptive_irt_support: str
    duration: str
    test_type: str
    description: str
    skills: str
    similarity_score: float

class RecommendationRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10

@app.get("/")
async def root():
    return {"message": "SHL Assessment Recommendation API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/recommend", response_model=List[AssessmentResponse])
async def get_recommendations(request: RecommendationRequest):
    try:
        recommendations = recommender.get_recommendations(
            query=request.query,
            top_n=request.max_results
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
