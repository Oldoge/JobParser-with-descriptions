import os
import time
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

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Job Analysis Report\n\n")

    print("Starting analysis (with auto-retry logic)...")

    for i, job in enumerate(jobs):

        print(f"[{i + 1}/{len(jobs)}] Analyzing: {job['Title']}...")

        prompt = (f"CV: {cv_text}\n\nJob: {job['Title']}\nDesc: {job['Description']}\n\nAnalyze Pros and Cons. Today is {time.strftime('%Y-%m-%d')}."
                  f"n\nProvide a concise analysis of how well the CV matches the job description, highlighting key strengths and potential gaps. Use bullet points for clarity."
                  f"n\nBe honest and critical, but also constructive. Focus on the most relevant skills, experiences, and qualifications. Avoid generic statements and provide specific insights based on the CV and job description."
                  f"n\nFormat the response in markdown with clear sections for Pros and Cons."
                  f"n\nWrite on Russian."
                  f"n\nExample format:\n\n## {job['Title']} - {job['Country']}\n\n### Pros:\n- Relevant experience in X\n- Strong skills in Y\n\n### Cons:\n- Lack of experience in Z\n- Missing certification in W\n\n---\n"
                  f"n\nWrite the analysis in Russian, but keep the job title and country in English for clarity. Make sure to provide a balanced view, acknowledging both the strengths and weaknesses of the CV in relation to the job description. Avoid being overly negative or positive, and focus on providing actionable insights that could help improve the CV or better align it with the job requirements."
                  f"n\n Wrtie summary, but in percents, how well the CV matches the job description, based on the analysis of pros and cons. Provide a percentage score that reflects the overall fit of the CV for the job, considering both the strengths and weaknesses identified in the analysis. The score should be a balanced reflection of how well the CV meets the key requirements and qualifications outlined in the job description, while also acknowledging any potential gaps or areas for improvement.")


        success = False
        retries = 0
        max_retries = 5
        wait_time = 30  # Initial wait in seconds if blocked

        while not success and retries < max_retries:
            try:
                response = client.models.generate_content(model=model_id, contents=prompt)

                with open(report_path, "a", encoding="utf-8") as f:
                    f.write(f"## {job['Title']} - {job['Country']}\n")
                    f.write(f"{response.text}\n\n---\n\n")

                success = True
                time.sleep(3)  # Safe gap between successful requests

            except google.api_core.exceptions.ResourceExhausted as e:
                retries += 1
                print(f"   Rate limit hit. Waiting {wait_time}s before retry {retries}/{max_retries}...")
                time.sleep(wait_time)
                wait_time *= 1  # Wait longer each time
            except Exception as e:
                print(f"   Unexpected error: {e}")
                break

    print(f"Analysis complete. Report: {report_path}")