import spacy
import re
from typing import List, Dict

class SkillExtractor:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common technical skills and keywords
        self.technical_skills = {
            'programming_languages': ['python', 'java', 'javascript', 'c++', 'ruby', 'php'],
            'frameworks': ['django', 'flask', 'spring', 'react', 'angular'],
            'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle'],
            'tools': ['git', 'docker', 'kubernetes', 'jenkins'],
            'cloud': ['aws', 'azure', 'gcp', 'cloud computing'],
        }
        
        # Common soft skills
        self.soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving',
            'time management', 'analytical', 'creativity', 'adaptability'
        ]

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract both technical and soft skills from text."""
        text = text.lower()
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Initialize results
        found_skills = {
            'technical_skills': [],
            'soft_skills': []
        }
        
        # Extract technical skills
        for category, skills in self.technical_skills.items():
            for skill in skills:
                if re.search(r'\b' + skill + r'\b', text):
                    found_skills['technical_skills'].append(skill)
        
        # Extract soft skills
        for skill in self.soft_skills:
            if re.search(r'\b' + skill + r'\b', text):
                found_skills['soft_skills'].append(skill)
        
        # Remove duplicates
        found_skills['technical_skills'] = list(set(found_skills['technical_skills']))
        found_skills['soft_skills'] = list(set(found_skills['soft_skills']))
        
        return found_skills

    def extract_education(self, text: str) -> List[str]:
        """Extract education information."""
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma']
        doc = self.nlp(text.lower())
        
        education = []
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in education_keywords):
                education.append(sent.text.strip())
        
        return education