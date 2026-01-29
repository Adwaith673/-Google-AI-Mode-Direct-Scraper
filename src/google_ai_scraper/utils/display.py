from tabulate import tabulate

def print_banner():
    print("\n" + "="*50)
    print("   GOOGLE AI MODE SCRAPER (Modular CLI)")
    print("="*50 + "\n")

def print_result(result):
    print(f"\n[{'✓' if result.get('success') else '✗'}] Question: {result.get('question')}")
    
    if result.get("success"):
        print("\n🤖 AI Response:")
        print("-" * 60)
        print(result.get("answer"))
        
        for i, t in enumerate(result.get("tables", []), 1):
            print(f"\n📊 Table {i} detected (Markdown):")
            print(t) # Simple print, can be enhanced with tabulate if parsed
    else:
        print(f"\n❌ Error: {result.get('error')}")
    print("\n" + "=" * 60)