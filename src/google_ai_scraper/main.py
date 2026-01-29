import time
import random
from .core.scraper import GoogleAIModeScraper
from .utils.display import print_banner, print_result
from .utils.storage import save_to_file

def main():
    print_banner()
    
    headless = input("Run in headless mode? (y/n) [n]: ").strip().lower() == "y"
    scraper = None
    results = []

    try:
        scraper = GoogleAIModeScraper(headless=headless)
        print("\n✓ Scraper initialized. Type 'quit' to exit, 'save' to dump JSON.")

        while True:
            q = input("\n❓ Ask AI: ").strip()
            if not q: continue
            
            if q.lower() == 'quit': break
            if q.lower() == 'save':
                save_to_file(results)
                continue

            result = scraper.ask_ai_mode(q)
            results.append(result)
            print_result(result)

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        if scraper: scraper.close()
        if results and input("\nSave session? (y/n): ").lower() == 'y':
            save_to_file(results)

if __name__ == "__main__":
    main()