import time
import random
from selenium.webdriver.common.by import By
from utils.filters import detect_grade


def extract_job_details(driver, job):
    driver.get(job["Link"])
    time.sleep(random.uniform(2, 4))

    description = "Could not extract"
    salary = "Not specified"

    try:
        if job["Source"] == "LinkedIn":

            try:
                driver.execute_script("""
                    var btn = document.querySelector('.show-more-less-html__button');
                    if (btn) { btn.click(); }

                    var overlays = document.querySelectorAll('.modal__overlay, .contextual-sign-in-modal');
                    overlays.forEach(function(el) { el.remove(); });
                    document.body.style.overflow = 'auto';
                """)
                time.sleep(1)
            except:
                pass


            try:
                description = driver.execute_script("""
                    var el = document.querySelector('.show-more-less-html__markup, .jobs-description-content__text');
                    return el ? el.textContent : null;
                """)

                if not description or len(description.strip()) < 10:
                    desc_el = driver.find_element(By.CSS_SELECTOR,
                                                  ".show-more-less-html__markup, .jobs-description-content__text")
                    description = desc_el.text
            except:
                if "auth_wall" in driver.current_url or "sign in" in driver.title.lower():
                    description = "LinkedIn requires authorization to view (Auth wall hard block)"

            try:
                salary = driver.execute_script("""
                    var el = document.querySelector('.compensation__salary-tooltip-text');
                    return el ? el.textContent : 'Not specified';
                """)
                if salary == 'Not specified' or not salary:
                    sal_el = driver.find_element(By.CSS_SELECTOR, ".compensation__salary-tooltip-text")
                    salary = sal_el.text
            except:
                pass

        else:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            iframe_found = False
            for iframe in iframes:
                if "cv.lv" in iframe.get_attribute("src") or "description" in iframe.get_attribute("id").lower():
                    driver.switch_to.frame(iframe)
                    description = driver.find_element(By.TAG_NAME, "body").text
                    driver.switch_to.default_content()
                    iframe_found = True
                    break

            if not iframe_found:
                try:
                    desc_el = driver.find_element(By.CSS_SELECTOR, ".vacancy-description, .job-description, article")
                    description = desc_el.text
                except:
                    description = driver.find_element(By.TAG_NAME, "body").text

            try:
                sal_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '€')]")
                for el in sal_elements:
                    text = el.text.strip()
                    if len(text) < 30 and any(char.isdigit() for char in text):
                        salary = text
                        break
            except:
                pass

    except Exception as e:
        pass

    if description:
        job["Description"] = description.replace("\n", " | ").strip()
    else:
        job["Description"] = "Could not extract"

    if salary:
        job["Salary"] = salary.strip()
    else:
        job["Salary"] = "Not specified"

    job["Grade"] = detect_grade(job["Title"], job["Description"])

    return job