from utils.pdf_extractor import PDFExtractor
from utils.skill_extractor import SkillExtractor
from models.skill_analyzer import SkillAnalyzer
import json

def analyze_candidate(resume_path: str, job_title: str) -> dict:
    """
    Analyze a candidate's resume for a specific job position.
    
    Args:
        resume_path: Path to the PDF resume
        job_title: Title of the job position
    
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Initialize components
        pdf_extractor = PDFExtractor()
        skill_extractor = SkillExtractor()
        skill_analyzer = SkillAnalyzer('data/job_dataset.csv')
        
        # Extract text from PDF
        resume_text = pdf_extractor.extract_text_from_pdf(resume_path)
        
        # Extract skills from resume
        candidate_skills = skill_extractor.extract_skills(resume_text)
        
        # Extract education information
        education = skill_extractor.extract_education(resume_text)
        
        # Analyze skill gap
        analysis_result = skill_analyzer.analyze_skill_gap(job_title, candidate_skills)
        
        # Generate improvement suggestions if needed
        suggestions = []
        if not analysis_result['is_fit']:
            suggestions = skill_analyzer.suggest_improvements(analysis_result['missing_skills'])
        
        # Prepare final result
        result = {
            'candidate_profile': {
                'technical_skills': candidate_skills['technical_skills'],
                'soft_skills': candidate_skills['soft_skills'],
                'education': education
            },
            'job_analysis': {
                'position': job_title,
                'category': analysis_result['job_category'],
                'is_suitable': analysis_result['is_fit'],
                'match_percentage': analysis_result['match_percentage'],
                'matching_skills': analysis_result['matching_skills'],
                'skill_gaps': analysis_result['missing_skills'],
                'improvement_suggestions': suggestions if not analysis_result['is_fit'] else []
            }
        }
        
        return result
        
    except Exception as e:
        return {'error': str(e)}

def main():
    # Example usage
    resume_path = "data/resume.pdf"
    job_title = "Software Engineer"
    
    result = analyze_candidate(resume_path, job_title)
    
    # Print results in a formatted way
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()