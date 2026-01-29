import re
from bs4 import BeautifulSoup

def clean_html_and_extract_answer(html: str, question: str):
    """Parses HTML to extract clean text, the specific AI answer, and tables."""
    if not html:
        return "", "", []

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    # Extract tables before flattening text
    tables_md = _extract_tables_markdown(soup)

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    full_clean = "\n".join(lines)
    full_clean = re.sub(r"\n{3,}", "\n\n", full_clean).strip()

    answer_only = _extract_answer_from_lines(lines, question)

    return full_clean, answer_only, tables_md

def _extract_answer_from_lines(lines, question: str) -> str:
    if not lines: return ""
    
    q = question.strip().lower()
    start_idx = 0
    
    # Find question start
    for i, line in enumerate(lines):
        if q and q in line.lower():
            start_idx = i
            break
            
    # Skip UI noise
    i = start_idx + 1
    skip_exact = {
        "thinking", "searching", "draft", "meet ai mode", "filters and topics",
        "ai mode", "all", "images", "videos", "news", "shopping"
    }
    
    while i < len(lines) and lines[i].strip().lower() in skip_exact:
        i += 1
        
    # Stop at footer markers
    footer_markers = ["ai can make mistakes", "your feedback helps", "search results", "sources"]
    collected = []
    
    for j in range(i, len(lines)):
        low = lines[j].lower()
        if any(marker in low for marker in footer_markers):
            break
        collected.append(lines[j])
        
    return re.sub(r"\s+", " ", "\n".join(collected)).strip()

def _extract_tables_markdown(soup: BeautifulSoup):
    tables_md = []
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if any(cells): rows.append(cells)
        
        if not rows: continue
        
        # Simple Markdown conversion
        header = rows[0]
        rows = rows[1:]
        md = f"| {' | '.join(header)} |\n| {' | '.join(['---']*len(header))} |"
        for r in rows:
            md += f"\n| {' | '.join(r)} |"
        tables_md.append(md)
        
    return tables_md