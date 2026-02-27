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

    # LinkedIn (Filter: Past week)
    {"country": "Latvia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Latvia&f_TPR=r86400"},
    {"country": "Estonia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Estonia&f_TPR=r86400"},
    {"country": "Lithuania", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Lithuania&f_TPR=r86400"},
    {"country": "Poland", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Poland&f_TPR=r86400"},
    {"country": "Czechia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Czechia&f_TPR=r86400"},
    {"country": "Slovakia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Slovakia&f_TPR=r86400"},
    {"country": "Hungary", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Hungary&f_TPR=r86400"},
    {"country": "Romania", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Romania&f_TPR=r86400"},
    {"country": "Belgium", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Belgium&f_TPR=r86400"},
    {"country": "Netherlands", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Netherlands&f_TPR=r86400"},
    {"country": "Germany", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Germany&f_TPR=r86400"},
    {"country": "France", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=France&f_TPR=r86400"},
    {"country": "Spain", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Spain&f_TPR=r86400"},
    {"country": "Italy", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Italy&f_TPR=r86400"},
    {"country": "Portugal", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Portugal&f_TPR=r86400"},
    {"country": "Slovenia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Slovenia&f_TPR=r86400"},
    {"country": "United States", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=United%20States&f_TPR=r86400"},
    {"country": "Latvia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Latvia&f_TPR=r86400"},
    {"country": "Estonia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Estonia&f_TPR=r86400"},
    {"country": "Lithuania", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Lithuania&f_TPR=r86400"},
    {"country": "Poland", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Poland&f_TPR=r86400"},
    {"country": "Czechia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Czechia&f_TPR=r86400"},
    {"country": "Slovakia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Slovakia&f_TPR=r86400"},
    {"country": "Hungary", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Hungary&f_TPR=r86400"},
    {"country": "Romania", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Romania&f_TPR=r86400"},
    {"country": "Belgium", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Belgium&f_TPR=r86400"},
    {"country": "Netherlands", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Netherlands&f_TPR=r86400"},
    {"country": "Germany", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Germany&f_TPR=r86400"},
    {"country": "France", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=France&f_TPR=r86400"},
    {"country": "Spain", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Spain&f_TPR=r86400"},
    {"country": "Italy", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Italy&f_TPR=r86400"},
    {"country": "Portugal", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Portugal&f_TPR=r86400"},
    {"country": "Slovenia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Slovenia&f_TPR=r86400"},
    {"country": "United States", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States&f_TPR=r86400"},

    # LinkedIn (Europe Remote - Filter: Past 24 hours)
    {"country": "Europe (Remote)", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Europe&f_WT=2&f_TPR=r86400"}
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
    "cloud engineer"
]

# Stop roles (Removed "data", kept specific non-engineering data roles)
STOP_ROLES = ["analyst", "analytics", "machine learning", "ml engineer", "data scientist"]

# QA keywords (allowed only if automation is mentioned)
QA_WORDS = ["qa", "quality assurance", "test", "tester"]

# Stop words for senior roles and management
STOP_SENIOR_WORDS = ["senior", "lead", "principal", "architect", "head of", "staff", "manager", "director"]

