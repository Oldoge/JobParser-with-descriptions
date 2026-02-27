import csv
import os
from utils.analyzer import analyze_jobs_with_cv


def run_standalone_analysis():
    csv_path = os.path.join("results", "perfect_target_jobs.csv")

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. You must run the scraper at least once first.")
        return

    print(f"Loading jobs from {csv_path} for re-analysis...")

    jobs_to_analyze = []
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs_to_analyze.append(row)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    if not jobs_to_analyze:
        print("No jobs found in the CSV file to analyze.")
        return

    print(f"Found {len(jobs_to_analyze)} jobs. Starting Gemini analysis...")
    # This calls the function in your utils/analyzer.py
    analyze_jobs_with_cv(jobs_to_analyze)


if __name__ == "__main__":
    run_standalone_analysis()