# SHL Assessment Recommendation System

A web application that recommends relevant SHL assessments based on natural language queries or job descriptions.

## 🔍 Features

- Natural language query processing  
- Recommends up to 10 most relevant SHL assessments  
- Each recommendation includes:  
  - Assessment name and URL (linked to SHL's catalog)  
  - Remote Testing Support (Yes/No)  
  - Adaptive/IRT Support (Yes/No)  
  - Duration and Test type  
  - Description and Skills  
  - Relevance score  

## 🗂️ Project Structure

shl-recommender/
├── backend/ # FastAPI backend
│ ├── main.py # API endpoints
│ └── recommender.py # Recommendation engine
├── frontend/ # Streamlit frontend
│ └── app.py # Web interface
├── data/ # Data files
│ └── shl_assessment_recommendations.csv
├── evaluation/ # Evaluation metrics and results
├── requirements.txt # Python dependencies
└── README.md # Project documentation

bash
Copy
Edit

## ⚙️ Setup and Installation

1. **Clone the repository**

git clone https://github.com/CyanArya/shl-recommender.git
cd shl-recommender
Create and activate a virtual environment

bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate    # On Windows
source .venv/bin/activate # On Linux/Mac
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Start the backend server

bash
Copy
Edit
cd backend
uvicorn main:app --reload
Start the frontend
Open a new terminal and run:

bash
Copy
Edit
cd frontend
streamlit run app.py
🧠 API Documentation
POST /recommend — Get assessment recommendations

Request Body:

json
Copy
Edit
{
  "query": "your query",
  "max_results": 10
}
Response: A JSON list of recommended assessments with details
Evaluation Metrics
Precision@K: Accuracy of top-K predictions

Mean Reciprocal Rank (MRR): Ranking quality metric

Coverage: Percentage of total assessments the model can recommend

Diversity: Variety across recommended items

🛠️ Technical Stack
Backend: FastAPI (Python 3.8+)

Frontend: Streamlit

ML/NLP: scikit-learn, pandas, NumPy

Data Processing: pandas, NumPy

Evaluation: scikit-learn metrics

🧪 Approach
1. Data Preprocessing
Clean and normalize assessment metadata

Extract useful features (skills, test type, etc.)

Generate TF-IDF text embeddings

2. Recommendation Engine
Use cosine similarity over TF-IDF vectors

Score and rank results based on relevance

Return top-N highest scoring assessments

3. Evaluation
Train/test split of assessment dataset

Use standard ranking metrics (MRR, Precision@K)

Measure how diverse and comprehensive the recommendations are

⚡ Performance Optimization
Cached repeated queries for faster lookup

Optimized data loading and vectorization

Used sparse matrices and dictionaries for memory efficiency

Batch recommendation supported using multiprocessing
