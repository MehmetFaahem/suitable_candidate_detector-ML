import pandas as pd
from typing import Dict, List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class SkillAnalyzer:
    def __init__(self, dataset_path: str):
        """Initialize with job dataset."""
        self.df = pd.read_csv(dataset_path)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def get_job_requirements(self, job_title: str) -> Dict:
        """Get required skills for a specific job title."""
        # Filter dataset for the specific job title
        job_data = self.df[self.df['job_title'].str.lower() == job_title.lower()]
        
        if job_data.empty:
            raise ValueError(f"No job found with title: {job_title}")
            
        # Get required skills
        required_skills = eval(job_data['job_skill_set'].iloc[0])  # Assuming skills are stored as string representation of list
        category = job_data['category'].iloc[0]
        
        return {
            'title': job_title,
            'category': category,
            'required_skills': required_skills
        }
    
    def analyze_skill_gap(self, 
                         job_title: str, 
                         candidate_skills: Dict[str, List[str]]) -> Dict:
        """Analyze skill gap between job requirements and candidate skills."""
        # Get job requirements
        job_req = self.get_job_requirements(job_title)
        required_skills = set(job_req['required_skills'])
        
        # Combine candidate's technical and soft skills
        candidate_skill_set = set(candidate_skills['technical_skills'] + 
                                candidate_skills['soft_skills'])
        
        # Find matching and missing skills
        matching_skills = required_skills.intersection(candidate_skill_set)
        missing_skills = required_skills - candidate_skill_set
        
        # Calculate match percentage
        match_percentage = (len(matching_skills) / len(required_skills)) * 100
        
        # Determine fitness
        is_fit = match_percentage >= 70  # Threshold can be adjusted
        
        return {
            'is_fit': is_fit,
            'match_percentage': round(match_percentage, 2),
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'job_category': job_req['category']
        }
    
    def suggest_improvements(self, missing_skills: List[str]) -> List[str]:
        """Generate improvement suggestions based on missing skills."""
        suggestions = []
        for skill in missing_skills:
            suggestions.append(f"Consider developing '{skill}' through online courses or practical projects")
        return suggestions