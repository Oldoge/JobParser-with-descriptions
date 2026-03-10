import time
import random
import re
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from config.settings import MAX_PAGES, STOP_LINK_TEXTS


def calculate_absolute_time(relative_str):
    """convert relative time strings like '2 hours ago' to absolute timestamps"""
    if not relative_str or relative_str == "Not specified":
        return relative_str

    relative_str = relative_str.lower()
    now = datetime.now()

    # Поиск числа в строке
    match = re.search(r'\d+', relative_str)
    if not match:
        if "just now" in relative_str or "now" in relative_str:
            return now.strftime("%Y-%m-%d %H:%M:%S")
        return relative_str

    value = int(match.group())

    if "minute" in relative_str or "min" in relative_str:
        delta = timedelta(minutes=value)
    elif "hour" in relative_str:
        delta = timedelta(hours=value)
    elif "day" in relative_str:
        delta = timedelta(days=value)
    elif "week" in relative_str:
        delta = timedelta(weeks=value)
    elif "month" in relative_str:
        delta = timedelta(days=value * 30)
    elif "year" in relative_str:
        delta = timedelta(days=value * 365)
    else:
        return relative_str

    absolute_time = now - delta
    return absolute_time.strftime("%Y-%m-%d %H:%M:%S")


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
                            raw_posted_date = card.find_element(By.TAG_NAME, "time").text.strip()
                            calc_time = calculate_absolute_time(raw_posted_date)
                            final_posted = f"{raw_posted_date} ({calc_time})"
                        except:
                            final_posted = "Not specified"

                        jobs.append({
                            "Title": text,
                            "Link": href.split("?")[0],
                            "Country": site["country"],
                            "Source": site["source"],
                            "Posted": final_posted
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
                    raw_posted = link['posted']
                    calc_time = calculate_absolute_time(raw_posted)

                    if raw_posted != "Not specified" and raw_posted != calc_time:
                        final_posted = f"{raw_posted} ({calc_time})"
                    else:
                        final_posted = raw_posted

                    jobs.append({
                        "Title": link['title'],
                        "Link": link['href'],
                        "Country": site["country"],
                        "Source": site["source"],
                        "Posted": final_posted
                    })
        except Exception as e:
            pass

    if not jobs:
        print("   Warning: No jobs found on the page.")

    unique_jobs = {job['Link']: job for job in jobs}.values()
    return list(unique_jobs)