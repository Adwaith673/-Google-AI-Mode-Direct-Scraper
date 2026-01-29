import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=True):
    """
    Setup Chrome driver with ENHANCED stealth options.
    Auto-detects Termux (Android) environment to use system driver.
    """
    chrome_options = Options()

    # --- 1. Base Stealth Options (Common for PC & Termux) ---
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=en-US")
    
    # Robust User Agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": "en-US,en",
        },
    )

    # --- 2. Driver Selection Logic ---
    termux_driver_path = "/data/data/com.termux/files/usr/bin/chromedriver"
    is_termux = os.path.exists(termux_driver_path)
    service = None

    if is_termux:
        logging.info(f"📱 Termux environment detected. Using system driver: {termux_driver_path}")
        # Termux specific adjustments
        chrome_options.add_argument("--headless=new") # Force headless on Termux usually
        service = Service(executable_path=termux_driver_path)
    else:
        # Standard PC Logic (Windows/Linux/Mac)
        if headless:
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
        
        try:
            # Auto-install matching driver version
            service = Service(ChromeDriverManager().install())
        except Exception as e:
            logging.error(f"Failed to download driver via manager: {e}")
            raise

    # --- 3. Initialize Driver ---
    try:
        # Suppress logs on PC if headless
        if not is_termux and headless:
            service.log_path = "NUL" if os.name == 'nt' else "/dev/null"
            
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # --- 4. CDP Stealth Injection (The Magic) ---
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    
                    window.chrome = { runtime: {} };
                    
                    const originalQuery = window.navigator.permissions.query;
                    window.navigator.permissions.query = (parameters) => (
                        parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                    );
                """
            },
        )
        return driver

    except Exception as e:
        logging.error(f"Failed to setup driver: {e}")
        if is_termux:
            logging.error("💡 Hint for Termux: Run 'pkg install chromium chromedriver' first.")
        raise