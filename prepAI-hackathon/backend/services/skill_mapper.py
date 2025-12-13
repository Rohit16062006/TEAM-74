import json
import os

# Path to the JSON file
MAP_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "role_skill_map.json")

def get_skills_for_role(job_title: str, experience: str) -> list:
    """
    Reads the role_skill_map.json and returns a list of skills for the given job_title and experience.
    """
    try:
        if not os.path.exists(MAP_FILE):
             print(f"Warning: Skill map file not found at {MAP_FILE}")
             return []
        
        with open(MAP_FILE, "r") as f:
            data = json.load(f)
            
        key = f"{job_title}:{experience}"
        return data.get(key, []) # Return empty list if key not found
    except Exception as e:
        print(f"Error loading skill map: {e}")
        return []
