"""Generate a markdown table from papers.jsonl."""
import json
from datetime import datetime

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
    papers = []
    with open('papers.jsonl', 'r') as f:
        for line in f:
            if line.strip():
                papers.append(json.loads(line))

    # Sort papers by published date (newest first)
    papers.sort(key=lambda x: x.get('published_date', ''), reverse=True)

    # Generate markdown table
    markdown = """# Recent Climate NLP Papers

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