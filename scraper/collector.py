import time
import random
from selenium.webdriver.common.by import By
from config.settings import MAX_PAGES, STOP_LINK_TEXTS


def collect_links(driver, site):
    jobs = []
    print(f"\n[{site['source']}] Collecting links ({site['country']})...")

    driver.get(site['url'])
    time.sleep(random.uniform(3, 5))

    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for btn in buttons:
            if any(x in btn.text.lower() for x in ["pieņemt visas", "accept all", "agree", "sutinku"]):
                btn.click()
                time.sleep(1)
                break
    except:
        pass

    print("   Scrolling to load more jobs...")
    for _ in range(MAX_PAGES):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))

        try:
            see_more_buttons = driver.find_elements(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button")
            for btn in see_more_buttons:
                if btn.is_displayed():
                    btn.click()
                    time.sleep(5)
        except:
            pass

    if site["source"] == "LinkedIn":
        if "auth_wall" in driver.current_url or "sign in" in driver.title.lower():
            print("   Warning: LinkedIn requested authorization. Aborting link collection for this request.")
            return []

        try:
            cards = driver.find_elements(By.CSS_SELECTOR, "li")
            for card in cards:
                try:
                    link_el = card.find_element(By.TAG_NAME, "a")
                    href = link_el.get_attribute("href")
                    if not href:
                        continue

                    text = link_el.text.strip()
                    text_lower = text.lower()

                    is_system_link = False
                    for stop_text in STOP_LINK_TEXTS:
                        if stop_text in text_lower:
                            is_system_link = True
                            break

                    if "job" in href and text and not is_system_link:
                        try:
                            posted_date = card.find_element(By.TAG_NAME, "time").text.strip()
                        except:
                            posted_date = "Not specified"

                        jobs.append({
                            "Title": text,
                            "Link": href.split("?")[0],
                            "Country": site["country"],
                            "Source": site["source"],
                            "Posted": posted_date
                        })
                except:
                    continue
        except Exception as e:
            pass
    else:
        try:
            links = driver.execute_script("""
                return Array.from(document.querySelectorAll('a[href*="/vacancy/"]')).map(a => {
                    const container = a.closest('li') || a.closest('div[class*="item"]');
                    let posted = "Not specified";
                    if (container) {
                        const timeEl = container.querySelector('span[class*="time"], div[class*="date"]');
                        if (timeEl) posted = timeEl.innerText.trim();
                    }
                    return {
                        title: a.innerText.trim(),
                        href: a.href,
                        posted: posted
                    };
                });
            """)
            for link in links:
                if link['title'] and "cv.lv" not in link['title'].lower():
                    jobs.append({
                        "Title": link['title'],
                        "Link": link['href'],
                        "Country": site["country"],
                        "Source": site["source"],
                        "Posted": link['posted']
                    })
        except Exception as e:
            pass

    if not jobs:
        print("   Warning: No jobs found on the page.")

    unique_jobs = {job['Link']: job for job in jobs}.values()
    return list(unique_jobs)