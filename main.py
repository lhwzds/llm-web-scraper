from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
from rich import print
from Rufus import RufusClient
import os
import json 
import traceback

# Get Rufus API key
key = os.getenv('Rufus_API_KEY')
client = RufusClient(api_key=key, verbose=True)

# instruction = "Find information about products features and customer FAQs"
# url = "https://www.withchima.com/"

instruction = "Find information about AI advantages and disadvantages."
url = "https://en.wikipedia.org/wiki/Intelligent_agent"

# Initialize the progress bar with elapsed time column
progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    TimeElapsedColumn()
)

try:
    # Open the progress context manager
    with progress:
        # Task 1: Scrape the main URL
        scrape_task = progress.add_task("[cyan]Scraping main URL...", total=1)
        documents, full_link_lst = client.scrape(url)
        progress.update(scrape_task, advance=1)
        
        analysis_results = {}
        max_links_to_analyze = 5

        # Task 2: Analyze the main URL
        if documents:
            analyze_task = progress.add_task("[green]Analyzing main document...", total=1)
            analysis_result = client.analyze(instruction, documents)
            progress.update(analyze_task, advance=1)

            if analysis_result is not None:
                analysis_results[url] = json.loads(analysis_result.content)
        else:
            print(f"[red]Unable to analyze web {url} information.[/red]")

        # Task 3: Scrape and analyze sub-links
        if full_link_lst:
            for link in full_link_lst[:max_links_to_analyze]:
                # Task 3a: Scrape the sub-link
                sub_scrape_task = progress.add_task(f"[cyan]Scraping sub-link: {link}...", total=1)
                sub_documents, _ = client.scrape(link)
                progress.update(sub_scrape_task, advance=1)

                if sub_documents:
                    # Task 3b: Analyze the sub-link
                    sub_analyze_task = progress.add_task(f"[green]Analyzing sub-document for {link}...", total=1)
                    sub_analysis_result = client.analyze(instruction, sub_documents)
                    progress.update(sub_analyze_task, advance=1)

                    if sub_analysis_result is not None:
                        analysis_results[link] = json.loads(sub_analysis_result.content)
                else:
                    print(f"[red]Unable to analyze sub-document for {link}[/red]")

        # Save analysis results
        if analysis_results:
            with open('analysis_result.json', 'w') as json_file:
                json.dump(analysis_results, json_file, indent=4, ensure_ascii=False)
            print("[green]Analysis results saved to analysis_result.json.[/green]")
        else:
            print("[yellow]No analysis results to save.[/yellow]")
            
except Exception as e:
    print("[red]An unexpected error occurred during processing.[/red]")
    traceback.print_exc()
    
# Close RufusClient
client.driver.quit()
