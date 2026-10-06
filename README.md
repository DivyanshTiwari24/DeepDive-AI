# DeepDive-AI

DeepDive-AI is an autonomous AI research desk that turns a single user question into a structured research report. It uses a multi-agent pipeline to search the web, read the most relevant source, synthesize findings into a report, and critique the final output.

The app is built as a Streamlit interface and uses LangChain with Mistral AI and Tavily for search and scraping.

## Features

- Web search for recent and relevant sources
- Source selection and deep content scraping
- AI-powered research report generation
- Automated evaluation and critique of the report
- Streamlit dashboard with a modern research UI
- Session history export for completed runs

## How it works

The pipeline runs in four stages:

1. Search agent: finds promising sources and snippets for the topic.
2. Reader agent: picks the strongest URL and scrapes deeper content.
3. Writer agent: combines findings into a polished research report.
4. Critic agent: scores the report and gives suggestions for improvement.

## Project structure

- `app.py` — Streamlit frontend and UI workflow
- `Pipeline.py` — orchestration for the multi-agent pipeline
- `Agent.py` — LLM agent and chain definitions
- `Tools.py` — Tavily search and URL scraping tools
- `requirements.txt` — Python dependencies
- `.streamlit/` — Streamlit configuration
- `.env` — local environment variables for API keys

## Tech stack

- Python 3.10+
- Streamlit
- LangChain
- Mistral AI (`ChatMistralAI`)
- Tavily API
- BeautifulSoup + requests
- Python-dotenv

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your keys:

```env
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

You can also use `TRAVILY_API_KEY` instead of `TAVILY_API_KEY`, since the app accepts both names.

## Run the app

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

## Example usage

In the app, enter a topic such as:

- "State of RISC-V in cloud data centers"
- "Recent developments in autonomous coding agents"
- "Growth of edge AI infrastructure"

The system will run its research pipeline and show:

- the search results
- scraped source content
- final report
- critic score and recommendations
- generated source list

## Notes

- This project depends on external API access for Tavily and Mistral.
- Some websites may block scraping or require rate limiting.
- The app is designed for research summarization and exploratory reporting rather than exact fact-checking or legal/compliance workflows.
- If a request fails due to transient network issues, the pipeline includes retry logic built into `invoke_with_retry`.

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, consider adding an open-source license appropriate for your use case.
