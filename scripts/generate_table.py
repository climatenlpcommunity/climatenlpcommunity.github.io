"""Generate a markdown table from papers.jsonl."""
import json
from datetime import datetime
from pathlib import Path

def format_date(date_str: str) -> str:
    """Format date string to YYYY-MM-DD."""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date.strftime('%Y-%m-%d')
    except (ValueError, AttributeError):
        return date_str

def sanitize_field(value: str | None) -> str:
    """Sanitize a field value for markdown table."""
    if value is None:
        return ''
    return str(value).replace('|', '\\|').replace('\n', ' ')

def main() -> None:
    """Generate markdown table from papers.jsonl."""
    path = Path(__file__).parent.parent / "data/papers.jsonl"
    
    with open(path, 'r') as f:
        all_papers = [json.loads(line) for line in f if line.strip()]
    
    all_papers.sort(key=lambda x: x.get('published_date', ''), reverse=True)
    
    # Use dict comprehension to keep only the first (newest) occurrence of each title
    papers = list({
        paper.get('title', '').strip(): paper 
        for paper in all_papers 
        if paper.get('title', '').strip()
    }.values())

    # Generate markdown table
    markdown = """# Climate NLP Research

Papers are sorted by publication date.

| Date | Title | Authors | URL |
|------|--------|---------|-----|
"""

    for paper in papers:
        date = format_date(paper.get('published_date', ''))
        title = paper.get('title', '').replace('|', '\\|')
        try:
            authors = paper.get('author', "").replace('|', '\\|')
        except:
            authors = ""
        url = paper.get('url', '')
        
        markdown += f"| {date} | {title} | {authors} | [Link]({url}) |\n"

    # Write to PAPERS.md
    with open('PAPERS.md', 'w') as f:
        f.write(markdown)

if __name__ == '__main__':
    main() 