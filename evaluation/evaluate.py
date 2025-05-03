import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score
from typing import List, Dict
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEvaluator:
    def __init__(self, data_path: str):
        """Initialize the evaluator with test data"""
        self.data = pd.read_csv(data_path)
        self.test_queries = self._prepare_test_queries()
    
    def _prepare_test_queries(self) -> List[Dict]:
        """Prepare test queries from the data"""
        # Group by query and collect assessment names
        test_queries = []
        for query, group in self.data.groupby('Query'):
            test_queries.append({
                'query': query,
                'relevant_assessments': group['Assessment_Name'].tolist()
            })
        return test_queries
    
    def precision_at_k(self, recommendations: List[str], relevant_items: List[str], k: int) -> float:
        """Calculate precision@k"""
        if not recommendations:
            return 0.0
        k = min(k, len(recommendations))
        relevant_recommendations = [item for item in recommendations[:k] if item in relevant_items]
        return len(relevant_recommendations) / k
    
    def mean_reciprocal_rank(self, recommendations: List[str], relevant_items: List[str]) -> float:
        """Calculate Mean Reciprocal Rank (MRR)"""
        for i, item in enumerate(recommendations, 1):
            if item in relevant_items:
                return 1.0 / i
        return 0.0
    
    def coverage(self, all_recommendations: List[List[str]], all_items: List[str]) -> float:
        """Calculate coverage of recommended items"""
        recommended_items = set()
        for recs in all_recommendations:
            recommended_items.update(recs)
        return len(recommended_items) / len(all_items)
    
    def diversity(self, recommendations: List[List[str]]) -> float:
        """Calculate diversity of recommendations"""
        if not recommendations:
            return 0.0
        
        # Calculate pairwise similarity between recommendations
        similarity = 0
        count = 0
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                set1 = set(recommendations[i])
                set2 = set(recommendations[j])
                if set1 and set2:
                    similarity += len(set1.intersection(set2)) / len(set1.union(set2))
                    count += 1
        
        return 1 - (similarity / count if count > 0 else 0)
    
    def evaluate(self, recommender, k_values: List[int] = [1, 3, 5, 10]) -> Dict:
        """Evaluate the recommender system"""
        results = {
            'precision_at_k': {k: [] for k in k_values},
            'mrr': [],
            'coverage': [],
            'diversity': []
        }
        
        all_recommendations = []
        all_items = set(self.data['Assessment_Name'].unique())
        
        for query_data in self.test_queries:
            query = query_data['query']
            relevant_items = query_data['relevant_assessments']
            
            # Get recommendations
            recommendations = [rec['assessment_name'] for rec in recommender.get_recommendations(query, top_n=max(k_values))]
            all_recommendations.append(recommendations)
            
            # Calculate metrics
            for k in k_values:
                precision = self.precision_at_k(recommendations, relevant_items, k)
                results['precision_at_k'][k].append(precision)
            
            mrr = self.mean_reciprocal_rank(recommendations, relevant_items)
            results['mrr'].append(mrr)
        
        # Calculate final metrics
        final_results = {
            'precision_at_k': {k: np.mean(scores) for k, scores in results['precision_at_k'].items()},
            'mrr': np.mean(results['mrr']),
            'coverage': self.coverage(all_recommendations, list(all_items)),
            'diversity': self.diversity(all_recommendations)
        }
        
        return final_results

def save_results(results: Dict, output_path: str):
    """Save evaluation results to a JSON file"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    logger.info(f"Results saved to {output_path}")

if __name__ == "__main__":
    from recommender import AssessmentRecommender
    
    # Initialize evaluator and recommender
    data_path = Path(__file__).parent.parent / "shl_assessment_recommendations.csv"
    evaluator = RecommendationEvaluator(data_path)
    recommender = AssessmentRecommender()
    
    # Run evaluation
    results = evaluator.evaluate(recommender)
    
    # Save results
    output_path = Path(__file__).parent / "evaluation_results.json"
    save_results(results, output_path)
    
    # Print results
    print("\nEvaluation Results:")
    print("------------------")
    for k, precision in results['precision_at_k'].items():
        print(f"Precision@{k}: {precision:.4f}")
    print(f"MRR: {results['mrr']:.4f}")
    print(f"Coverage: {results['coverage']:.4f}")
    print(f"Diversity: {results['diversity']:.4f}") 