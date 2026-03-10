import os
from dotenv import load_dotenv


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MAX_PAGES = 6

# LinkedIn time parameters:
# &f_TPR=r604800 (Past week)
# &f_TPR=r86400  (Past 24 hours)

# The base search keyword is set to "Python" to capture all related engineering roles.
# The exact role titles will be filtered later by the script.
SITES = [
    # CV-Online
    #{"country": "Latvia", "source": "CV.lv", "url": "https://cv.lv/lv/search?limit=50&keywords%5B0%5D=python"},
    #{"country": "Estonia", "source": "CV.ee", "url": "https://www.cv.ee/en/search?limit=50&keywords%5B0%5D=python"},
    #{"country": "Lithuania", "source": "CV.lt",
     #"url": "https://www.cvonline.lt/en/search?limit=50&keywords%5B0%5D=python"},

    # ------------------ PYTHON ------------------
    {"country": "Latvia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Latvia&f_TPR=r86400"},
    {"country": "Estonia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Estonia&f_TPR=r86400"},
    {"country": "Lithuania", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Lithuania&f_TPR=r86400"},
    {"country": "Poland", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Poland&f_TPR=r86400"},
    {"country": "Czechia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Czechia&f_TPR=r86400"},
    {"country": "Slovakia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Slovakia&f_TPR=r86400"},
    {"country": "Hungary", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Hungary&f_TPR=r86400"},
    {"country": "Romania", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Romania&f_TPR=r86400"},
    {"country": "Belgium", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Belgium&f_TPR=r86400"},
    {"country": "Netherlands", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Netherlands&f_TPR=r86400"},
    {"country": "Germany", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Germany&f_TPR=r86400"},
    {"country": "France", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=France&f_TPR=r86400"},
    {"country": "Spain", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Spain&f_TPR=r86400"},
    {"country": "Italy", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Italy&f_TPR=r86400"},
    {"country": "Portugal", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Portugal&f_TPR=r86400"},
    {"country": "Slovenia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Slovenia&f_TPR=r86400"},
    {"country": "United States", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=United%20States&f_TPR=r86400"},

    # ------------------ SOFTWARE ENGINEER ------------------
    {"country": "Latvia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Latvia&f_TPR=r86400"},
    {"country": "Estonia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Estonia&f_TPR=r86400"},
    {"country": "Lithuania", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Lithuania&f_TPR=r86400"},
    {"country": "Poland", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Poland&f_TPR=r86400"},
    {"country": "Czechia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Czechia&f_TPR=r86400"},
    {"country": "Slovakia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Slovakia&f_TPR=r86400"},
    {"country": "Hungary", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Hungary&f_TPR=r86400"},
    {"country": "Romania", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Romania&f_TPR=r86400"},
    {"country": "Belgium", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Belgium&f_TPR=r86400"},
    {"country": "Netherlands", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Netherlands&f_TPR=r86400"},
    {"country": "Germany", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Germany&f_TPR=r86400"},
    {"country": "France", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=France&f_TPR=r86400"},
    {"country": "Spain", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Spain&f_TPR=r86400"},
    {"country": "Italy", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Italy&f_TPR=r86400"},
    {"country": "Portugal", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Portugal&f_TPR=r86400"},
    {"country": "Slovenia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Slovenia&f_TPR=r86400"},
    {"country": "United States", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States&f_TPR=r86400"},

    # ------------------ GRADUATE SOFTWARE ENGINEER 2026 ------------------
    {"country": "Latvia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Latvia&f_"},
    {"country": "Estonia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Estonia&f_"},
    {"country": "Lithuania", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Lithuania&f_"},
    {"country": "Poland", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Poland&f_"},
    {"country": "Czechia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Czechia&f_"},
    {"country": "Slovakia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Slovakia&f_"},
    {"country": "Hungary", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Hungary&f_"},
    {"country": "Romania", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Romania&f_"},
    {"country": "Belgium", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Belgium&f_"},
    {"country": "Netherlands", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Netherlands&f_"},
    {"country": "Germany", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Germany&f_"},
    {"country": "France", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=France&f_"},
    {"country": "Spain", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Spain&f_"},
    {"country": "Italy", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Italy&f_"},
    {"country": "Portugal", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Portugal&f_"},
    {"country": "Slovenia", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Slovenia&f_"},
    {"country": "United States", "source": "LinkedIn", "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=United%20States&f_"},

    # ------------------ EUROPE (REMOTE) ------------------
    {"country": "Europe (Remote)", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Europe&f_WT=2&f_TPR=r86400 "},
    {"country": "Europe (Remote)", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Europe&f_WT=2&f_TPR=r86400"},
    {"country": "Europe (Remote)", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Graduate%20Software%20Engineer%202026&location=Europe&f_WT=2&f_"}
]

# LinkedIn system links to ignore
STOP_LINK_TEXTS = [
    "about", "accessibility", "user agreement", "privacy policy",
    "cookie policy", "copyright policy", "brand policy",
    "guest controls", "community guidelines"
]

# Target keywords for the requested roles
TARGET_KEYWORDS = [
    "data engineer",
    "backend", "software engineer", "software developer", "developer", "programmer", "fullstack", "full-stack",
    "sre", "site reliability", "platform engineer",
    "cloud engineer", "graduate"
]

# Stop roles (Removed "data", kept specific non-engineering data roles)
STOP_ROLES = ["analyst", "analytics", "machine learning", "ml engineer",]

# QA keywords (allowed only if automation is mentioned)
QA_WORDS = ["qa", "quality assurance", "test", "tester"]

# Stop words for senior roles and management
STOP_SENIOR_WORDS = ["senior", "lead", "principal", "architect", "head of", "staff", "manager", "director"]

CLOUD_SIGNALS = [
    "sre", "site reliability", "platform engineer", "cloud",
    "devops", "kubernetes", "k8s", "aws", "gcp", "azure",
    "docker", "terraform", "ci/cd", "infrastructure"
]