# llm-web-scraper

The **LLM Web Scraper** is a flexible tool that uses natural language instructions and a large language model to intelligently extract structured JSON data from web pages for RAG integration.

## Environment Setup

Follow these steps to set up the Python environment for this project.

### Prerequisites
Make sure you have the following installed:

- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer (included with Python)
- **conda**: Recommend using conda to manage python enviroment
- **openai**: Ensure your OpenAI API key is set and accessible in your OS environment

After python enviroment created, use ```pip install -r requirements.txt``` to install required packages.

## Usage

1. Running the scraper and analyzer: After setting up the environment and installing dependencies, run the following command to start the scraping and analysis process:

   ```python main.py```

2. Customization: You can modify the target URL and instructions in the main.py file to scrape and analyze different web pages.

3. Output: You can monitor the progress for scraping and analysis after program started.
   
   ![Output Progress](https://github.com/lhwzds/llm-web-scraper/blob/main/output_progress.png)

## Project Structure

This project consists of two main components that work together to scrape web content and analyze it using LLM (Language Learning Models) tools.

### RefusClient.py

1. scrape
    This function is responsible for web scraping and retrieving the content of a target URL. It uses Selenium to automate the browser for accessing dynamic web pages and BeautifulSoup for parsing the HTML content to extract text and sub links.

2. analyze
    This function takes the scraped content and sends it to an LLM (such as OpenAI’s GPT) for analysis. It is designed to handle large documents by truncating the input and extracting key insights from web pages with Structured JSON Outputs.

### main.py

    The main.py file is the entry point of the project. It orchestrates the scraping and analyzing tasks using the RufusClient class defined in RefusClient.py. This script is responsible for initialize RufusClient and execute scrape and analyze tasks for main url and sub urls. Finally it writes the analysis results to analysis_result.json.

## Challenges

### Sub-link Scraping and Dynamic Content with Selenium

**Challenge:**

    Scraping sub-links can be challenging due to the dynamic nature of modern websites. Many websites use JavaScript to load content asynchronously, which makes it difficult to retrieve all necessary data without rendering the page in a browser.

**Solution:**

    Selenium is used to address this challenge by automating a real web browser (Chrome). It allows for the loading and rendering of dynamic content (such as pages that require scrolling or interaction).
    WebDriverWait ensures that the necessary elements are fully loaded before attempting to scrape them.
    However, scraping multiple sub-links requires managing browser resources efficiently and ensuring that you don’t overload the target server with requests.

### Structured JSON Outputs for GPT Integration in RAG Systems

**Challenge:**

    When sending scraped content to GPT for analysis, generating structured outputs in JSON format is essential for integrating with Retrieval-Augmented Generation (RAG) systems. Unstructured text can be difficult to process and align with downstream tasks.

**Solution:**

    Instructing GPT to return results in a strictly structured JSON format ensures that the responses can be easily parsed and used programmatically.
    For this,the analyze method leverages object definition and supply objects along system messages that guide GPT to format its outputs as JSON. This ensures consistency in the format across different responses. The structured JSON is particularly useful for RAG systems, where the output from the LLM is combined with retrieved documents, enabling more organized and scalable responses.

## output examples

Two example output files are stored in the output_example folder, named ```analysis_result_chima.json``` and ```analysis_result_wiki.json```. These files contain structured JSON responses generated from the web scraping and analysis performed using the RufusClient. The JSON output produced by the web scraping and analysis process is structured in a hierarchical manner to organize the scraped content and analyzed results efficiently. This design ensures that the data is easy to parse, understand, and integrate into RAG system or other machine learning pipelines.

Here is an overview of the JSON structure and its design rationale:

1. **Top-Level Keys: URLs**

    Each entry in the JSON output corresponds to a specific URL that was scraped and analyzed. The URL serves as the key, and its value is a detailed breakdown of the content scraped from that URL.
    
    ```
    {
        "https://www.withchima.com/": { ... },
        "https://en.wikipedia.org/wiki/Intelligent_agent": { ... }
    }
    ```

2. **Second Level: response Array**

    Under each URL key, there is a response array that contains the results of the analysis. This array organizes the analyzed content into different categories, such as product features or customer FAQs, depending on instructions input.
    
    ```
    {
        "https://www.withchima.com/": {
            "response": [
                {
                    "title": "Product Features",
                    "answerList": [ ... ]
                },
                {
                    "title": "Customer FAQs",
                    "answerList": [ ... ]
                }
            ]
        }
    }
    ```

3. **Third Level: title and answerList**
   
    Each object in the response array contains two key elements:
    
    title: This field defines the category or topic of the analyzed content. For example, it might be "Product Features" or "Customer FAQs".
    
    answerList: This is an array of detailed answers or explanations. Each entry in the answerList provides specific insights about the topic, using a structured format.
    
    ```
    {
        "title": "Product Features",
        "answerList": [
            {
                "subAnswer": "1. **Easy Integration**: Chima provides AI agents that integrate seamlessly..."
            },
            {
                "subAnswer": "2. **Monitor Baseline Metrics**: Chima sets benchmarks for process efficiency..."
            }
        ]
    }
    ```

4. **Fourth Level: subAnswer**
    
    Inside the answerList, each entry contains a single field:
    
    subAnswer: This field holds the detailed response or analysis result. It can include formatted text or markdown-style elements (such as bold or italic text) to emphasize certain parts of the response.
    
    ```
    {
        "subAnswer": "1. **Easy Integration**: Chima provides AI agents that integrate seamlessly..."
    }
    ```
    This structured design provides a reliable and efficient way to manage and analyze web-scraped content, making it well-suited for further analysis, storage, or integration into RAG systems.

