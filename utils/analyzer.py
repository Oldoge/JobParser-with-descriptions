import os
import time
import re
import sqlite3
import google.api_core.exceptions
from google import genai
from PyPDF2 import PdfReader
from config.settings import GEMINI_API_KEY


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def update_job_in_db(link, score, report, db_path="results/jobs.db"):
    """Update the job entry in the database with the match score and analysis report."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
                       UPDATE jobs
                       SET match_score     = ?,
                           analysis_report = ?
                       WHERE link = ?
                       ''', (score, report, link))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error db when adding: {e}")


def analyze_jobs_with_cv(jobs, cv_file_path="cv.pdf"):
    if not GEMINI_API_KEY:
        print("Warning: Gemini API key is not set. Skipping analysis.")
        return

    if not os.path.exists(cv_file_path):
        print(f"Warning: CV file '{cv_file_path}' not found.")
        return

    print("Extracting text from CV...")
    cv_text = extract_text_from_pdf(cv_file_path)

    client = genai.Client(api_key=GEMINI_API_KEY)
    model_id = "gemini-3-pro-preview"

    os.makedirs("results", exist_ok=True)
    report_path = os.path.join("results", "cv_analysis_report.md")

    # Saving the report in Markdown format for better readability
    if not os.path.exists(report_path):
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Job Analysis Report\n\n")

    print("Starting analysis (with auto-retry logic)...")

    for i, job in enumerate(jobs):
        print(f"[{i + 1}/{len(jobs)}] Analyzing: {job['Title']}...")

        prompt = (f"CV: {cv_text}\n\nJob: {job['Title']}\nDesc: {job['Description']}\n\n"
                  f"Analyze Pros and Cons.\n\n"
                  f"Provide a concise analysis of how well the CV matches the job description, highlighting key strengths and potential gaps. Use bullet points for clarity.\n\n"
                  f"Be honest and critical, but also constructive. Focus on the most relevant skills, experiences, and qualifications. Avoid generic statements and provide specific insights based on the CV and job description.\n\n"
                  f"Format the response in markdown with clear sections for Pros and Cons.\n\n"
                  f"Write the analysis in Russian, but keep the job title and country in English for clarity. Make sure to provide a balanced view, acknowledging both the strengths and weaknesses of the CV in relation to the job description.\n\n"
                  f"CRITICAL: At the very end of your response, write the final match score strictly in this format: 'Match Score: X%', where X is a number from 0 to 100 based on your analysis.")

        success = False
        retries = 0
        max_retries = 5
        wait_time = 30

        while not success and retries < max_retries:
            try:
                response = client.models.generate_content(model=model_id, contents=prompt)
                report_text = response.text

                # Parsing the match score from the end of the response
                score = None
                match = re.search(r'(?:Match Score:?\s*|Итоговая оценка:?\s*|Совпадение:?\s*)?(\d{1,3})%', report_text,
                                  re.IGNORECASE)
                if match:
                    score = int(match.group(1))

                # Writing the analysis report and score back to the database
                update_job_in_db(job['Link'], score, report_text)

                    # Saving the report in a Markdown file for better readability
                with open(report_path, "a", encoding="utf-8") as f:
                    f.write(f"## {job['Title']} - {job['Country']}\n")
                    f.write(f"{report_text}\n\n")
                    if score is not None:
                        f.write(f"**Extracted Match Score: {score}%**\n")
                    f.write(f"---\n\n")

                success = True
                time.sleep(3)

            except google.api_core.exceptions.ResourceExhausted:
                retries += 1
                print(f"   Rate limit hit. Waiting {wait_time}s before retry {retries}/{max_retries}...")
                time.sleep(wait_time)
                wait_time *= 2  # Exponential backoff
            except Exception as e:
                print(f"   Unexpected error: {e}")
                break

    print(f"Analysis complete. Report: {report_path}")