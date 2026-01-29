import time
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Imports from our new custom modules
from .browser import setup_driver
from .parsing import clean_html_and_extract_answer

class GoogleAIModeScraper:
    """Orchestrates the scraping process using Selenium and the custom Parser."""

    AI_MODE_URL = (
        "https://google.com/search?q=&sourceid=chrome&ie=UTF-8&udm=50&aep=48&cud=0&qsubts=1764494340788"
    )

    def __init__(self, headless=True, verbose=True):
        self.verbose = verbose
        # Here we call the isolated function from browser.py
        self.driver = setup_driver(headless)
        self.log("✓ Browser driver initialized successfully")

    def log(self, message, level="INFO"):
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")

    def close(self):
        if self.driver:
            self.driver.quit()
            self.log("Browser closed")

    def human_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))

    def human_type(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

    def ask_ai_mode(self, question):
        try:
            self.log(f"🤖 Asking AI Mode: '{question}'")
            self.driver.get(self.AI_MODE_URL)
            self.human_delay(4, 6)

            self._handle_cookies()
            self.human_delay(2, 3)

            # Find input field
            search_input = self._find_input_box()
            if not search_input:
                return {
                    "question": question,
                    "success": False,
                    "error": "Could not find AI Mode input box.",
                }

            # Scroll to the input and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_input)
            self.human_delay(0.5, 1)
            search_input.click()
            
            # Type the question and submit
            search_input.clear()
            self.human_delay(0.3, 0.5)
            self.human_type(search_input, question)
            self.human_delay(0.5, 1)
            search_input.send_keys(Keys.RETURN)

            self.log("Waiting for AI response...")
            self.human_delay(6, 10)

            # Extract response HTML
            ai_response_html = self._extract_ai_response_html()

            if ai_response_html:
                # Here we use the isolated Parser from parsing.py
                full_text, answer_only, tables_md = clean_html_and_extract_answer(
                    ai_response_html, question
                )
                
                return {
                    "question": question,
                    "answer": answer_only or full_text,
                    "tables": tables_md,
                    "success": True,
                    "timestamp": datetime.now().isoformat(),
                    "format": "text",
                }
            else:
                return {
                    "question": question,
                    "success": False,
                    "error": "No AI response found in HTML.",
                }

        except Exception as e:
            self.log(f"Error asking AI Mode: {e}", "ERROR")
            return {
                "question": question,
                "success": False,
                "error": str(e),
            }

    def _find_input_box(self):
        self.log("Looking for input box...")
        selectors = [
            "//textarea[contains(@placeholder, 'Ask anything')]",
            "//textarea[@name='q']",
            "//textarea[contains(@aria-label, 'Search')]",
            "//input[@name='q']",
            "//div[@role='combobox']//textarea",
        ]

        for selector in selectors:
            try:
                el = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                return el
            except TimeoutException:
                continue
        return None

    def _handle_cookies(self):
        try:
            cookie_selectors = [
                "//button[contains(., 'Accept all')]",
                "//button[contains(., 'I agree')]",
                "//button[@id='L2AGLb']",
            ]
            for selector in cookie_selectors:
                try:
                    button = WebDriverWait(self.driver, 4).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    button.click()
                    self.log("✓ Cookie consent handled")
                    return
                except TimeoutException:
                    continue
        except Exception:
            pass

    def _extract_ai_response_html(self):
        response_selectors = [
            "//div[contains(@class, 'ai-mode-response')]",
            "//div[@data-attrid='AIResponse']",
            "//div[contains(@class, 'generated-content')]",
            "//div[@data-attrid='SGEAnswer']",
            "//div[@id='search']",  # Fallback
        ]

        for selector in response_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                for element in elements:
                    html = element.get_attribute("innerHTML") or ""
                    if html and len(html.strip()) > 50:
                        return html.strip()
            except Exception:
                continue
        return None