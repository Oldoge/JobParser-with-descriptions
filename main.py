import os
from config.settings import SITES
from scraper.driver import setup_driver
from scraper.collector import collect_links
from scraper.parser import extract_job_details
from utils.filters import is_unsuitable_job, is_matching_target
from utils.analyzer import analyze_jobs_with_cv
from utils.database import JobDatabase


def main():
    print("Starting Modular Deep Scraper...")
    driver = setup_driver()
    db = JobDatabase()

    all_links = []
    try:
        for site in SITES:
            found_links = collect_links(driver, site)
            print(f"Unique links found: {len(found_links)}")
            all_links.extend(found_links)

        print(f"\nStarting deep parsing for {len(all_links)} jobs...")

        processed_jobs = []
        for i, job in enumerate(all_links):
            print(f"[{i + 1}/{len(all_links)}] Analyzing: {job['Title']} ({job['Country']}) - {job['Posted']}")
            detailed_job = extract_job_details(driver, job)

            if is_unsuitable_job(detailed_job["Title"], detailed_job["Description"]):
                print("   -> Skipped: Senior role or 4+ years of experience required.")
                continue

            if not is_matching_target(detailed_job["Title"], detailed_job["Description"]):
                print("   -> Skipped: Non-target role.")
                continue

            # Saving normal jobs to the database
            db.save_job(detailed_job)
            processed_jobs.append(detailed_job)
            print(f"   -> Added as {detailed_job['Grade']} to Database")

    finally:
        driver.quit()
        db.close()

    print(f"\nDone! Perfect target jobs saved/verified in Database: {len(processed_jobs)}")
    print(f"Database location: {os.path.abspath('results/jobs.db')}")

    # Start Gemini analysis only if we have suitable jobs to analyze
    if processed_jobs:
        analyze_jobs_with_cv(processed_jobs)


if __name__ == "__main__":
    main()