import os
import time
import re
import google.api_core.exceptions
from google import genai
from PyPDF2 import PdfReader
from config.settings import GEMINI_API_KEY
from utils.database import JobDatabase


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text


def get_all_cvs_text(cv_folder="cv_storage"):
    if not os.path.exists(cv_folder):
        os.makedirs(cv_folder, exist_ok=True)
        print(f"Directory '{cv_folder}' created. Please put your CV PDFs there.")
        return None, []

    cv_files = [f for f in os.listdir(cv_folder) if f.lower().endswith('.pdf')]
    if not cv_files:
        return None, []

    combined_text = ""
    for file in cv_files:
        path = os.path.join(cv_folder, file)
        text = extract_text_from_pdf(path)
        combined_text += f"\n\n--- [CV File: {file}] ---\n{text}"

    return combined_text, cv_files


def analyze_jobs_with_cv(jobs, cv_folder="cv_storage"):
    if not GEMINI_API_KEY:
        print("Warning: Gemini API key is not set.")
        return

    print("Extracting text from all CVs...")
    cvs_text, cv_files = get_all_cvs_text(cv_folder)

    if not cvs_text:
        print(f"Warning: No CVs found in '{cv_folder}'.")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)
    model_id = "gemini-3.1-flash-lite-preview"

    os.makedirs("results", exist_ok=True)
    report_path = os.path.join("results", "cv_analysis_report.md")
    db = JobDatabase()

    if not os.path.exists(report_path):
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Job Analysis Report (Multi-CV)\n\n")

    for i, job in enumerate(jobs):
        print(f"[{i + 1}/{len(jobs)}] Analyzing: {job['Title']}...")

        prompt = (f"Here are {len(cv_files)} variants of my CV:\n{cvs_text}\n\n"
                  f"Job Title: {job['Title']}\nJob Description: {job['Description']}\n\n"
                  f"Task:\n"
                  f"1. Compare the job description against all provided CV variants.\n"
                  f"2. Choose the ONE best CV variant that gives the highest chance of getting an interview.\n"
                  f"3. Explain why it's the best fit and list Pros/Cons.\n"
                  f"4. If the Match Score for the winning CV is GREATER THAN 35%, write a tailored Cover Letter in Formal English, more polite, more humanized, a bit cheeky based on that CV. If score is 35% or lower, state 'No Cover Letter'.\n"
                  f"5. Write analysis in Russian.\n\n"
                  f"CRITICAL: End your response EXACTLY in this format:\n"
                  f"Recommended CV: [Exact file name]\n"
                  f"Match Score: [X]%\n"
                  f"---COVER LETTER---\n"
                  f"[Cover letter text or 'None']")

        success = False
        retries = 0
        wait_time = 30

        while not success and retries < 5:
            try:
                response = client.models.generate_content(model=model_id, contents=prompt)
                report_text = response.text

                score = None
                best_cv = None
                cover_letter = None

                score_match = re.search(r'Match Score:?\s*(\d{1,3})%', report_text, re.IGNORECASE)
                if score_match:
                    score = int(score_match.group(1))

                cv_match = re.search(r'Recommended CV:?\s*([a-zA-Z0-9_\-\.]+)', report_text, re.IGNORECASE)
                if cv_match:
                    best_cv = cv_match.group(1).strip()

                cl_split = report_text.split("---COVER LETTER---")
                if len(cl_split) > 1:
                    cover_letter = cl_split[1].strip()

                # Убираем блок Cover Letter из общего отчета для чистоты, если он найден
                main_report = cl_split[0].strip() if len(cl_split) > 1 else report_text

                db.update_analysis(job['Link'], score, main_report, best_cv, cover_letter)

                with open(report_path, "a", encoding="utf-8") as f:
                    f.write(f"## {job['Title']} - {job['Country']}\n")
                    f.write(f"{main_report}\n\n")
                    if score is not None:
                        f.write(f"**Score: {score}% | CV: {best_cv}**\n")
                    if cover_letter and cover_letter.lower() not in ['none', 'no cover letter']:
                        f.write(f"### Cover Letter:\n{cover_letter}\n")
                    f.write(f"---\n\n")

                success = True
                time.sleep(3)

            except google.api_core.exceptions.ResourceExhausted:
                retries += 1
                time.sleep(wait_time)
                wait_time *= 2
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

    db.close()