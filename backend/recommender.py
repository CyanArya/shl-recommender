import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Any
import os

class AssessmentRecommender:
    def __init__(self):
        """Initialize the recommender with assessment data"""
        self.data = self._load_data()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._prepare_features()
    
    def _load_data(self) -> pd.DataFrame:
        """Load and preprocess the assessment data"""
        # Load the CSV file
        data_path = os.path.join(os.path.dirname(__file__), '..', 'shl_assessment_recommendations.csv')
        df = pd.read_csv(data_path, encoding='utf-8', quotechar='"', escapechar='\\')
        
        # Add default values for required fields
        df['Remote_Testing_Support'] = 'Yes'  # Default value
        df['Adaptive_IRT_Support'] = 'Yes'    # Default value
        df['Duration'] = '60 minutes'          # Default value
        df['Test_Type'] = 'Technical'          # Default value
        df['Description'] = df['Assessment_Name']  # Use name as description if not available
        df['Skills'] = df['Query']             # Use query as skills if not available
        
        # Clean and preprocess the data
        df['combined_text'] = df.apply(lambda row: f"{row['Assessment_Name']} {row['Description']} {row['Skills']}", axis=1)
        return df
    
    def _prepare_features(self):
        """Prepare TF-IDF features for similarity calculation"""
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['combined_text'])
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess the query text"""
        # Remove special characters and convert to lowercase
        query = re.sub(r'[^\w\s]', '', query.lower())
        return query
    
    def get_recommendations(self, query: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Get recommendations based on the query
        
        Args:
            query: The search query or job description
            top_n: Number of recommendations to return
            
        Returns:
            List of recommended assessments with their details
        """
        # Preprocess the query
        processed_query = self._preprocess_query(query)
        
        # Transform query to TF-IDF vector
        query_vector = self.vectorizer.transform([processed_query])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top N recommendations
        top_indices = np.argsort(similarity_scores)[-top_n:][::-1]
        
        # Prepare recommendations
        recommendations = []
        for idx in top_indices:
            assessment = self.data.iloc[idx]
            recommendations.append({
                "assessment_name": assessment['Assessment_Name'],
                "assessment_url": assessment['Assessment_URL'],
                "remote_testing_support": assessment['Remote_Testing_Support'],
                "adaptive_irt_support": assessment['Adaptive_IRT_Support'],
                "duration": assessment['Duration'],
                "test_type": assessment['Test_Type'],
                "description": assessment['Description'],
                "skills": assessment['Skills'],
                "similarity_score": float(similarity_scores[idx])
            })
        
        return recommendations

# Testing code
if __name__ == "__main__":
    recommender = AssessmentRecommender()
    # Test with a sample query
    results = recommender.get_recommendations("Java")
    print(f"Found {len(results)} recommendations")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['assessment_name']} - {result['assessment_url']}")