MAX_PAGES = 3

# LinkedIn time parameters:
# &f_TPR=r604800 (Past week)
# &f_TPR=r86400  (Past 24 hours)

# The base search keyword is set to "Python" to capture all related engineering roles.
# The exact role titles will be filtered later by the script.
SITES = [
    # CV-Online
    {"country": "Latvia", "source": "CV.lv", "url": "https://cv.lv/lv/search?limit=50&keywords%5B0%5D=python"},
    {"country": "Estonia", "source": "CV.ee", "url": "https://www.cv.ee/en/search?limit=50&keywords%5B0%5D=python"},
    {"country": "Lithuania", "source": "CV.lt",
     "url": "https://www.cvonline.lt/en/search?limit=50&keywords%5B0%5D=python"},

    # LinkedIn (Filter: Past week)
    {"country": "Latvia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Latvia&f_TPR=r604800"},
    {"country": "Estonia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Estonia&f_TPR=r604800"},
    {"country": "Lithuania", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Lithuania&f_TPR=r604800"},
    {"country": "Poland", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Poland&f_TPR=r604800"},
    {"country": "Czechia", "source": "LinkedIn",
     "url": "https://www.linkedin.com/jobs/search?keywords=Python&location=Czechia&f_TPR=r604800"},

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