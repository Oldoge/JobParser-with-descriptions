import os
import sqlite3
from utils.analyzer import analyze_jobs_with_cv


def run_standalone_analysis():
    db_path = os.path.join("results", "jobs.db")

    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found. You must run the scraper at least once first.")
        return

    print(f"Loading unanalyzed jobs from {db_path} for processing...")

    jobs_to_analyze = []
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()


        cursor.execute("SELECT * FROM jobs WHERE match_score IS NULL")
        rows = cursor.fetchall()

        for row in rows:
            jobs_to_analyze.append({
                "Title": row["title"],
                "Country": row["country"],
                "Description": row["description"],
                "Link": row["link"]
            })
        conn.close()
    except Exception as e:
        print(f"Error reading Database: {e}")
        return

    if not jobs_to_analyze:
        print("No new jobs found in the Database to analyze.")
        return

    print(f"Found {len(jobs_to_analyze)} unanalyzed jobs. Starting Gemini analysis...")
    analyze_jobs_with_cv(jobs_to_analyze)


if __name__ == "__main__":
    run_standalone_analysis()