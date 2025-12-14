import json
import os

# Path to the JSON file
MAP_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "role_skill_map.json")

def get_skills_for_role(job_title: str, experience: str) -> list:
    """
    Returns a list of skills for the given job_title and experience.
    Uses exact match from JSON first, then falls back to keyword matching.
    """
    job_title = job_title.lower().strip()
    experience = experience.lower().strip()
    
    # 1. Try Exact/Configured Match
    try:
        if os.path.exists(MAP_FILE):
            with open(MAP_FILE, "r") as f:
                data = json.load(f)
                # Try exact key
                key = f"{job_title}:{experience}"
                if key in data:
                    return data[key]
                
                # Try just job title
                for map_key, skills in data.items():
                    if map_key.split(":")[0] == job_title:
                        return skills
    except Exception as e:
        print(f"Error loading skill map: {e}")

    # 2. Keyword Matching (Heuristic Fallback)
    skills = set()
    
    # Textual triggers
    if "frontend" in job_title or "react" in job_title or "web" in job_title:
        skills.update(["React", "JavaScript", "CSS"])
    
    if "backend" in job_title or "api" in job_title:
        skills.update(["Python", "SQL", "System Design"])
    
    if "data" in job_title or "analyst" in job_title or "science" in job_title:
        skills.update(["Python", "SQL", "DSA"])
    
    if "full" in job_title and "stack" in job_title:
        skills.update(["React", "Python", "SQL", "System Design"])
        
    if "java" in job_title:
        skills.add("DSA") # Assuming we map Java to DSA for now as we don't have Java tasks specific
        
    if "manager" in job_title or "lead" in job_title:
        skills.add("System Design")

    # Default if nothing matches
    if not skills:
        skills.update(["DSA", "Behavioral"])

    return list(skills)
