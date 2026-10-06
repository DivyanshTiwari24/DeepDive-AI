import os
import time
from dotenv import load_dotenv

load_dotenv()

from Agent import critic_chain, write_chain, finder, read


def print_step(step: str, source: str, message: str) -> None:
    print("\n" + "=" * 80)
    print(f"{step} | Source: {source}")
    print("=" * 80)
    print(message)
    print("=" * 80)


def invoke_with_retry(agent_or_chain, payload: dict, max_retries: int = 3, backoff: float = 1.5):
    """Safely invoke an agent or chain with exponential backoff on transient network reset errors."""
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            return agent_or_chain.invoke(payload)
        except Exception as exc:
            last_exc = exc
            print(f"[Network Retry {attempt}/{max_retries}] Exception encountered: {exc}. Retrying in {backoff}s...")
            if attempt < max_retries:
                time.sleep(backoff)
                backoff *= 2
    raise last_exc


def run_pipe(topic: str, on_step=None) -> dict:
    state = {}

    def notify(step: str, title: str, detail: str = "") -> None:
        """Optional progress hook for UIs. Never breaks the pipeline."""
        if callable(on_step):
            try:
                on_step(step, title, detail)
            except Exception:
                pass

    notify("search", "Searching the web", f"Topic: {topic}")
    print_step("STEP 1 - Starting research", "Pipeline", f"Topic: {topic}")
    
    search_agent = finder()
    search_result = invoke_with_retry(
        search_agent,
        {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
    )

    state["search_results"] = search_result["messages"][-1].content

    print_step(
        "STEP 1 - Search result extracted",
        "finder() research agent",
        state["search_results"],
    )

    notify("scrape", "Reading the strongest source", "Picking a URL from the search results")

    reader_agent = read()
    print_step(
        "STEP 2 - Sending search result to reader",
        "Pipeline -> read() agent",
        state["search_results"][:800],
    )
    
    reader_result = invoke_with_retry(
        reader_agent,
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}",
                )
            ]
        }
    )
    
    state["reader_res"] = reader_result["messages"][-1].content
    print_step(
        "STEP 2 - Detailed content extracted",
        "read() scraping agent",
        state["reader_res"],
    )

    combine_search = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['reader_res']}"
    )

    print_step(
        "STEP 3 - Sending research to report writer",
        "Pipeline -> write_chain",
        combine_search,
    )
    notify("write", "Writing the report", f"Combining {len(combine_search)} characters of research")
    
    state["report"] = invoke_with_retry(
        write_chain,
        {"topic": topic, "research": combine_search}
    )
    
    print_step(
        "STEP 3 - Report extracted",
        "write_chain",
        state["report"],
    )

    print_step(
        "STEP 4 - Sending report for review",
        "Pipeline -> critic_chain",
        state["report"],
    )

    notify("review", "Critic reviewing the draft", "Scoring structure, facts and sources")
    
    state["feedback"] = invoke_with_retry(
        critic_chain,
        {"report": state["report"]}
    )

    print_step(
        "STEP 4 - Critic feedback extracted",
        "critic_chain",
        state["feedback"],
    )

    return state


if __name__ == "__main__":
    topic = str(input("\n Enter a research topic : "))
    run_pipe(topic)