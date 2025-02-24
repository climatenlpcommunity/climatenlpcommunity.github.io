from datetime import datetime
from exa_py import Exa
import json
import os
import sys
from rich.console import Console
from rich.progress import track
from pathlib import Path

from exa_py.api import _Result, SearchResponse

def fetch_climate_nlp_papers() -> list[dict]:
    """Fetch recent papers about climate NLP using Exa AI."""
    console = Console()

    console.print("[bold blue]Initializing Exa client...[/]")
    exa = Exa(os.environ["EXA_API_KEY"])
    
    query = """
    recent research papers about climate change and natural language processing
    """
    
    console.print(f"[bold green]Searching for papers with query:[/]\n{query.strip()}")
    search_response: SearchResponse[_Result] = exa.search(
        query,
        use_autoprompt=True,
        num_results=100,
        # include_domains=["arxiv.org", "acl-anthology.org", "aclweb.org"]
    )
    
    console.print(f"[bold green]Found {len(search_response.results)} results[/]")
    
    papers = []
    for result in track(search_response.results, description="Processing results"):
        paper = result.__dict__
        paper["date_retrieved"] = datetime.now().isoformat()
        papers.append(paper)
    
    return papers

def update_jsonl(papers: list[dict], output_file: str) -> None:
    """Update the JSONL file with new papers."""
    console = Console()
    
    console.print(f"[bold blue]Writing {len(papers)} papers to {output_file}[/]")
    with open(output_file, "a") as f:
        for paper in track(papers, description="Writing papers"):
            f.write(json.dumps(paper) + "\n")
    console.print("[bold green]Done![/]")

if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent.parent / "data/papers.jsonl"
    papers = fetch_climate_nlp_papers()
    update_jsonl(papers, output_file)
