import random
from sqlalchemy.orm import Session
from models import DailyTask

# Simple task bank
TASK_BANK = {
    "SQL": [
        ("Write a query to find the second highest salary.", "Coding"),
        ("Explain the difference between DELETE and TRUNCATE.", "Conceptual"),
        ("Design a schema for a library management system.", "System Design"),
        ("Write a query to join three tables.", "Coding"),
        ("What is normalization? Explain 1NF, 2NF, 3NF.", "Conceptual")
    ],
    "Python": [
        ("Explain list comprehension with an example.", "Conceptual"),
        ("Write a function to reverse a string without slice.", "Coding"),
        ("What are decorators in Python?", "Conceptual"),
        ("Implement a singleton class.", "Coding"),
        ("Explain the difference between deep copy and shallow copy.", "Conceptual")
    ],
    "React": [
        ("Explain the Virtual DOM.", "Conceptual"),
        ("Create a counter component using hooks.", "Coding"),
        ("What is the difference between state and props?", "Conceptual"),
        ("Explain useEffect dependency array.", "Conceptual"),
        ("Implement a simple Todo list.", "Coding")
    ],
    "JavaScript": [
        ("What is event bubbling?", "Conceptual"),
        ("Explain closures with an example.", "Conceptual"),
        ("Implement Promise.all polyfill.", "Coding"),
        ("Difference between let, const, and var.", "Conceptual"),
        ("Explain the 'this' keyword.", "Conceptual")
    ],
    "DSA": [
        ("Implement Binary Search.", "Coding"),
        ("Reverse a linked list.", "Coding"),
        ("Check for balanced parentheses.", "Coding"),
        ("Find the LCA of a binary tree.", "Coding"),
        ("Explain QuickSort algorithm.", "Conceptual")
    ],
    "System Design": [
        ("Design a URL shortener.", "System Design"),
        ("Design Rate Limiter.", "System Design"),
        ("Design Instagram feed.", "System Design"),
    ]
}

DEFAULT_TASKS = [
    ("Tell me about yourself.", "Behavioral"),
    ("Why do you want this job?", "Behavioral"),
    ("Describe a challenging situation you faced.", "Behavioral")
]

def generate_tasks_for_plan(db: Session, plan_id: int, days: int, skills: list):
    """
    Generates daily tasks for the given plan and saves them to the database.
    """
    try:
        with open("task_gen.log", "a") as log:
            log.write(f"Generating tasks for Plan {plan_id}, Days: {days}, Skills: {skills}\n")
            
        tasks_to_create = []
        
        # Simple round-robin distribution of skills across days
        skills = skills or [] # Ensure list
        skill_count = len(skills)
        
        for day in range(1, days + 1):
            # Pick a skill for the day
            if skill_count > 0:
                current_skill = skills[(day - 1) % skill_count]
                possible_tasks = TASK_BANK.get(current_skill, [])
            else:
                current_skill = "General"
                possible_tasks = []

            if not possible_tasks:
                # Fallback to default or generic
                task_text, task_type = random.choice(DEFAULT_TASKS)
                task_skill = "Behavioral"
            else:
                task_text, task_type = random.choice(possible_tasks)
                task_skill = current_skill
                
            new_task = DailyTask(
                plan_id=plan_id,
                day=day,
                task=task_text,
                type=task_type,
                skill=task_skill
            )
            tasks_to_create.append(new_task)
        
        db.add_all(tasks_to_create)
        db.commit()
        
        with open("task_gen.log", "a") as log:
            log.write(f"Successfully created {len(tasks_to_create)} tasks for Plan {plan_id}\n")

    except Exception as e:
        db.rollback()
        with open("task_gen.log", "a") as log:
            log.write(f"ERROR generating tasks for Plan {plan_id}: {str(e)}\n")
        print(f"Error generating tasks: {e}")
