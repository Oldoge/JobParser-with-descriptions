import csv
import os
from config.settings import SITES
from scraper.driver import setup_driver
from scraper.collector import collect_links
from scraper.parser import extract_job_details
from utils.filters import is_unsuitable_job, is_matching_target


def main():
    print("Starting Modular Deep Scraper (Python focus, time filters applied)...")
    driver = setup_driver()

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
                print("   -> Skipped: Non-target role (No Python mentioned, or it is Data/QA).")
                continue

            processed_jobs.append(detailed_job)
            print(f"   -> Added as {detailed_job['Grade']}")

    finally:
        driver.quit()

    os.makedirs("results", exist_ok=True)
    filename = os.path.join("results", "perfect_target_jobs.csv")

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Grade", "Salary", "Country", "Posted", "Link", "Source",
                                               "Description"])
        writer.writeheader()
        writer.writerows(processed_jobs)

    print(f"\nDone! Perfect target jobs saved: {len(processed_jobs)}")
    print(f"File: {os.path.abspath(filename)}")


if __name__ == "__main__":
    main()