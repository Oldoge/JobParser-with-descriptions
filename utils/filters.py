import re
from config.settings import TARGET_KEYWORDS, STOP_ROLES, QA_WORDS, STOP_SENIOR_WORDS, CLOUD_SIGNALS




def detect_grade(title, description):
    text = f"{title} {description}".lower()


    grade = "Not Specified"
    if any(word in text for word in ["junior", "intern", "trainee", "без опыта", "entry"]):
        grade = "Junior / Intern"
    elif any(word in text for word in ["middle", "mid-level", "2 years", "3 years", "2 gadi", "3 gadi", "2 года", "3 года"]):
        grade = "Middle"

    # 2. Cloud-signal prioritization (Приоритизация инфраструктурных ролей)
    if any(signal in text for signal in CLOUD_SIGNALS):
        if grade == "Not Specified":
            grade = "Cloud/Infra Priority"
        else:
            grade += " | Cloud/Infra Priority"

    return grade


def is_unsuitable_job(title, description):
    text = f"{title} {description}".lower()


    if any(word in text for word in STOP_SENIOR_WORDS):
        return True


    exp_pattern = re.compile(r'(?<!-)\b([4-9]|[1-9]\d)\+?\s*(?:years|yrs|gadi|gadu|лет|года|год)')
    plus_exp_pattern = re.compile(r'\+\s*([4-9]|[1-9]\d)\s*(?:years|yrs|gadi|gadu|лет|года|год)')

    if exp_pattern.search(text) or plus_exp_pattern.search(text):
        return True

    return False


def is_matching_target(title, description):
    title_lower = title.lower()
    desc_lower = description.lower()

    # 1. Mandatory check for Python (Language filtering)
    if "python" not in title_lower and "python" not in desc_lower:
        return False

    # 2. Check title for target keywords (Data Engineer, Cloud Engineer, etc.)
    if not any(keyword in title_lower for keyword in TARGET_KEYWORDS):
        return False

    # 3. Filter out Analyst and Data Scientist roles
    if any(role in title_lower for role in STOP_ROLES):
        return False

    # 4. Exception for QA: pass only if automation is mentioned
    if any(qa_word in title_lower for qa_word in QA_WORDS):
        if "automation" not in title_lower and "automation" not in desc_lower and "автоматизац" not in desc_lower:
            return False

    return True