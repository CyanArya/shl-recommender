💡 Problem
We were tasked with building a system that takes a simple text query like a skill or job role — e.g., “problem solving” or “sales leadership” — and returns relevant assessment recommendations from SHL’s dataset. The output should be returned via an API, in JSON format.

🛠️ What I Built
🔍 Text Matching Model
I used TF-IDF (Term Frequency–Inverse Document Frequency) to convert all skills and descriptions in the dataset into vectors.

When a user sends a query, the system compares it against all entries using cosine similarity to find the closest matches.

🤖 Recommender Engine
A custom Python class called SHLRecommender reads the CSV data and finds the top N most relevant assessments.

For each query, it returns assessment names and URLs.

🌐 FastAPI Backend
I built a simple API using FastAPI.

Endpoint: POST /recommend

Payload format:

json
Copy
Edit
{ "text": "team leadership" }
Response:

json
Copy
Edit
{
  "recommendations": [
    { "assessment": "Leadership Potential", "url": "https://shl.com/leadership" },
    ...
  ]
}
🧪 Testing & Deployment
You can test the API locally using uvicorn:

bash
Copy
Edit
uvicorn main:app --reload
Errors like malformed CSV rows (e.g., unescaped quotes) are handled gracefully.

Easily extensible to support fuzzy matching or model upgrades.

📁 Folder Structure
bash
Copy
Edit
shl-recommender/
├── backend/
│   ├── main.py         # FastAPI app
│   ├── recommender.py  # Core recommendation logic
│   └── data.csv        # Skill-assessment mappings
✅ Summary
In short, this solution converts raw skills data into a smart matching engine that powers a clean, developer-friendly API. It’s modular, lightweight, and ready for production or further enhancement.
