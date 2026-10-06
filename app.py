"""
folio — Perplexity / Linear Minimalist Obsidian UI for Multi-Agent Research Pipeline.

Run:
    streamlit run app.py
"""

import html
import json
import os
import re
import time
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------------------------------- #
# Application Branding & Configuration
# --------------------------------------------------------------------------- #
BRAND = "FOLIO"
KICKER = "MULTI-AGENT RESEARCH ENGINE"

STEPS = [
    ("search", "Search", "Web search for reliable sources"),
    ("scrape", "Scrape", "Deep scrape of primary source"),
    ("write", "Write", "Synthesize findings into report"),
    ("review", "Review", "Evaluate structure, depth & facts"),
]
STEP_KEYS = [s[0] for s in STEPS]

# API key check (supports TRAVILY_API_KEY and TAVILY_API_KEY)
TAVILY_KEY = os.getenv("TRAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY")

MISSING_KEYS = []
if not TAVILY_KEY:
    MISSING_KEYS.append("TAVILY_API_KEY / TRAVILY_API_KEY")
if not MISTRAL_KEY:
    MISSING_KEYS.append("MISTRAL_API_KEY")

st.set_page_config(
    page_title=f"{BRAND} — Autonomous Research Desk",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------- #
# Minimalist Obsidian Dark CSS Design System (Linear / Perplexity Style)
# --------------------------------------------------------------------------- #
OBSIDIAN_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* CSS Variables - Minimalist Obsidian Palette */
:root {
    --bg-obsidian: #09090b;
    --bg-surface: #121215;
    --bg-card: #18181b;
    --bg-card-hover: #202024;
    
    --border-subtle: #27272a;
    --border-highlight: #3f3f46;
    
    --text-bright: #fafafa;
    --text-body: #d4d4d8;
    --text-muted: #80808a;
    --text-dim: #52525b;
    
    --accent-glow: #6366f1;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
}

/* Global Reset */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-obsidian) !important;
    color: var(--text-body) !important;
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

[data-testid="stHeader"], [data-testid="stToolbar"], footer, #MainMenu {
    display: none !important;
}

.block-container {
    max-width: 1050px !important;
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.8rem !important;
    padding-left: 1.1rem !important;
    padding-right: 1.1rem !important;
}

[data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
    color: var(--text-body) !important;
}

/* Navbar / Brand Header */
.brand-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.2rem;
    margin-bottom: 3rem;
    border-bottom: 1px solid var(--border-subtle);
}

.brand-mark {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.03em;
    color: var(--text-bright);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.brand-mark span {
    color: var(--accent-glow);
    font-size: 0.95rem;
}

.brand-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
}

.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    margin-right: 0.4em;
    vertical-align: middle;
}
.status-dot.ok { background-color: var(--accent-emerald); box-shadow: 0 0 6px var(--accent-emerald); }
.status-dot.warn { background-color: var(--accent-amber); box-shadow: 0 0 6px var(--accent-amber); }

/* Hero Section */
.hero-box {
    text-align: center;
    padding: 3rem 0 2rem;
    max-width: 780px;
    margin: 0 auto;
}

.hero-kicker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent-glow);
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1.15;
    letter-spacing: -0.03em;
    color: var(--text-bright);
    margin-bottom: 0.9rem;
}

.hero-sub {
    font-size: 1.05rem;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 620px;
    margin: 0 auto 2.5rem;
}

/* Perfect Column & Input Button Vertical Alignment */
div[data-testid="column"] {
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-end !important;
}

div[data-testid="stTextInput"] {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stTextInput"] label {
    display: none !important;
}

div[data-testid="stTextInput"] > div {
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
}

div[data-testid="stTextInput"] > div > div {
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
}

div[data-testid="stTextInput"] > div > div > input {
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    background-color: var(--bg-surface) !important;
    color: var(--text-bright) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    padding: 0 1.3rem !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    line-height: 50px !important;
    box-shadow: none !important;
    transition: border-color 0.15s ease !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: var(--text-dim) !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: var(--text-muted) !important;
    outline: none !important;
}

/* Primary Action Button (White Minimalist & Exactly Aligned) */
div[data-testid="stButton"] {
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stButton"] > button,
button[kind="primary"],
[data-testid="baseButton-primary"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    background-color: #fafafa !important;
    background: #fafafa !important;
    color: #09090b !important;
    border: 1px solid #fafafa !important;
    border-radius: 10px !important;
    padding: 0 1.5rem !important;
    margin: 0 !important;
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    line-height: 50px !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: none !important;
    transition: all 0.15s ease !important;
}

div[data-testid="stButton"] > button:hover,
button[kind="primary"]:hover,
[data-testid="baseButton-primary"]:hover {
    background-color: #e4e4e7 !important;
    background: #e4e4e7 !important;
    border-color: #e4e4e7 !important;
    color: #000000 !important;
    transform: translateY(-1px);
}

/* Secondary Buttons (History) */
[data-testid="baseButton-secondary"] {
    background-color: var(--bg-surface) !important;
    color: var(--text-body) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 0.85rem !important;
    transition: all 0.15s ease !important;
}

[data-testid="baseButton-secondary"]:hover {
    background-color: var(--bg-card-hover) !important;
    border-color: var(--border-highlight) !important;
    color: var(--text-bright) !important;
}

/* Download Button */
[data-testid="stDownloadButton"] button {
    background-color: var(--bg-surface) !important;
    color: var(--text-bright) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
}

[data-testid="stDownloadButton"] button:hover {
    border-color: var(--border-highlight) !important;
    background-color: var(--bg-card-hover) !important;
}

/* Active Progress Stepper Bar */
.stepper-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.88rem;
    color: var(--text-muted);
}

.step-item.active {
    color: var(--text-bright);
    font-weight: 600;
}

.step-item.done {
    color: var(--text-muted);
}

.step-dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 1px solid var(--border-subtle);
    background: var(--bg-obsidian);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
}

.step-item.active .step-dot {
    border-color: var(--accent-glow);
    background: var(--accent-glow);
    color: #ffffff;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
}

.step-item.done .step-dot {
    border-color: var(--text-muted);
    background: var(--border-subtle);
    color: var(--text-bright);
}

/* Execution Log Box */
.log-box {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    max-height: 180px;
    overflow-y: auto;
    margin-bottom: 1.5rem;
}

.log-row {
    display: flex;
    gap: 0.75rem;
    padding: 0.15rem 0;
}
.log-t { color: var(--text-dim); }
.log-k { color: var(--accent-glow); font-weight: 500; min-width: 4.5em; }
.log-m { color: var(--text-body); }

/* Results Header Metabar */
.meta-header {
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 1rem;
    margin-bottom: 1.8rem;
}

.meta-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-bright);
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}

.meta-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    display: flex;
    gap: 1.2rem;
}

/* Metric Cards */
.metric-box {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1rem 1.2rem;
}

.metric-num {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-bright);
    line-height: 1.1;
}

.metric-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-top: 0.3rem;
}

/* Tabs Override */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.3rem !important;
    background-color: var(--bg-surface) !important;
    padding: 0.3rem !important;
    border-radius: 8px !important;
    border: 1px solid var(--border-subtle) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    height: 38px !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
    background-color: transparent !important;
    border: none !important;
    padding: 0 1rem !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background-color: var(--bg-card) !important;
    color: var(--text-bright) !important;
}

/* Markdown Body Styling */
.report-content {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 2rem 2.2rem;
    font-size: 1rem;
    line-height: 1.75;
    color: #e4e4e7;
}

.report-content h1, .report-content h2, .report-content h3 {
    color: var(--text-bright);
    font-weight: 600;
    margin-top: 1.8rem;
    margin-bottom: 0.8rem;
}
.report-content h1 { font-size: 1.7rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.5rem; }
.report-content h2 { font-size: 1.35rem; color: #a1a1aa; }
.report-content h3 { font-size: 1.1rem; }

.report-content p { margin-bottom: 1.1rem; }
.report-content ul, .report-content ol { padding-left: 1.3rem; margin-bottom: 1.1rem; }
.report-content li { margin-bottom: 0.35rem; }
.report-content blockquote {
    border-left: 2px solid var(--accent-glow);
    padding-left: 1rem;
    margin: 1.2rem 0;
    color: var(--text-muted);
    font-style: italic;
}

/* Critic & Sources Styling */
.card-panel {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}

.panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
}

.score-display {
    font-size: 3.2rem;
    font-weight: 700;
    color: var(--text-bright);
    line-height: 1;
}

.bullet-list {
    list-style: none;
    padding: 0;
    margin: 0.4rem 0;
}
.bullet-list li {
    position: relative;
    padding-left: 1.3rem;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 0.5rem;
    color: var(--text-body);
}
.bullet-list.good li::before { content: "✓"; position: absolute; left: 0; color: var(--accent-emerald); }
.bullet-list.bad li::before { content: "—"; position: absolute; left: 0; color: var(--accent-amber); }

.source-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--border-subtle);
    text-decoration: none !important;
}
.source-item:last-child { border-bottom: none; }
.source-title { font-size: 0.9rem; font-weight: 500; color: var(--text-bright); }
.source-domain { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--text-muted); }
.source-item:hover .source-title { color: var(--accent-glow); }

/* Alerts */
.alert-box {
    background: var(--bg-surface);
    border: 1px solid var(--accent-rose);
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    color: #fca5a5;
    margin-bottom: 1.2rem;
}
</style>
"""

st.markdown(OBSIDIAN_CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Helpers & Parsers
# --------------------------------------------------------------------------- #
def esc(text: str) -> str:
    return html.escape(str(text or ""), quote=True)


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:50] or "report"


def domain_of(url: str) -> str:
    clean = re.sub(r"^https?://(www\.)?", "", url)
    return clean.split("/")[0]


def parse_critic(text: str):
    """Robust, fail-safe parser for critic response text supporting varied markdown formats."""
    text = str(text or "")
    score = None
    
    # Flexible score regex (Score: X/10, **Score:** X/10, ### Score: X/10)
    m = re.search(r"(?:Score|Rating)\s*:?\s*\*{0,2}(\d+(?:\.\d+)?)\s*/\s*10", text, re.I)
    if m:
        try:
            score = float(m.group(1))
        except ValueError:
            score = None

    def grab(start_pat, end_pats):
        lookahead = ("(?=" + "|".join(end_pats) + r"|\Z)") if end_pats else r""
        rx = re.compile(start_pat + r"\s*:?\s*(.*?)" + lookahead, re.I | re.S)
        found = rx.search(text)
        if found:
            val = found.group(1)
            return val.strip() if val else ""
        return ""

    def bullets(block):
        out = []
        if not block:
            return out
        for line in block.splitlines():
            s = line.strip()
            if not s or re.match(r"^#{1,6}\s*|(score|strengths|areas to improve|improvements|one line verdict|verdict)\b", s, re.I):
                continue
            s = re.sub(r"^([-*\u2022]|\d+[.)])\s+", "", s)
            if s and len(s) > 2:
                out.append(s)
        return out

    tail = [r"Areas to Improve", r"Improvements", r"One line verdict", r"Verdict"]
    strengths = bullets(grab(r"Strengths", tail))
    improvements = bullets(grab(r"Areas to Improve|Improvements", [r"One line verdict", r"Verdict"]))
    verdict = " ".join(grab(r"(?:One line )?[Vv]erdict", []).split())

    return score, strengths, improvements, verdict


def parse_sources(search_text: str):
    pairs = re.findall(r"URL:\s*(\S+)\s*Title:\s*([^\n]+)", search_text or "")
    seen, out = set(), []
    for url, title in pairs:
        url = url.strip()
        if not url or url in seen:
            continue
        seen.add(url)
        out.append({"url": url, "title": title.strip()})
    if not out:
        for url in re.findall(r"https?://[^\s)\]>\"']+", search_text or ""):
            if url not in seen:
                seen.add(url)
                out.append({"url": url, "title": domain_of(url)})
    return out


def count_words(text: str) -> int:
    return len(re.findall(r"\w+", text or ""))


def estimate_reading_time(text: str) -> int:
    words = count_words(text)
    return max(1, round(words / 200))


# --------------------------------------------------------------------------- #
# State Initialization
# --------------------------------------------------------------------------- #
if "history" not in st.session_state:
    st.session_state["history"] = []
if "log" not in st.session_state:
    st.session_state["log"] = []
if "step_state" not in st.session_state:
    st.session_state["step_state"] = {"active": None, "done": [], "finished": False}
if "current_result" not in st.session_state:
    st.session_state["current_result"] = None


# --------------------------------------------------------------------------- #
# UI Component Renderers
# --------------------------------------------------------------------------- #
def render_brand_bar():
    is_ready = len(MISSING_KEYS) == 0
    status_cls = "ok" if is_ready else "warn"
    status_lbl = "System Ready" if is_ready else f"Missing: {', '.join(MISSING_KEYS)}"

    st.markdown(
        f'<div class="brand-bar">'
        f'  <div class="brand-mark"><span>✦</span> {BRAND}</div>'
        f'  <div class="brand-badge"><span class="status-dot {status_cls}"></span> {esc(status_lbl)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_stepper(step_state: dict) -> str:
    active = step_state.get("active")
    done = set(step_state.get("done") or [])
    finished = bool(step_state.get("finished"))

    items = []
    for i, (key, name, desc) in enumerate(STEPS):
        is_done = finished or i in done or (active is not None and i < active)
        is_active = (not finished) and active is not None and i == active

        cls = "done" if is_done else ("active" if is_active else "pending")
        dot_content = "✓" if is_done else f"{i + 1}"

        items.append(
            f'<div class="step-item {cls}">'
            f'  <div class="step-dot">{dot_content}</div>'
            f'  <div>{esc(name)}</div>'
            f'</div>'
        )

    return f'<div class="stepper-bar">{"".join(items)}</div>'


def render_log(rows: list) -> str:
    if not rows:
        return ""
    body = "".join(
        f'<div class="log-row">'
        f'  <span class="log-t">{esc(r.get("t", ""))}</span>'
        f'  <span class="log-k">{esc(r.get("k", ""))}</span>'
        f'  <span class="log-m">{esc(r.get("m", ""))}</span>'
        f'</div>'
        for r in rows
    )
    return f'<div class="log-box">{body}</div>'


def update_progress(stepper_box, log_box):
    if st.session_state["step_state"].get("active") is not None or st.session_state["log"]:
        stepper_box.markdown(render_stepper(st.session_state["step_state"]), unsafe_allow_html=True)
        log_box.markdown(render_log(st.session_state["log"]), unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Pipeline Execution Callback Runner
# --------------------------------------------------------------------------- #
def run_research_pipeline(topic: str, stepper_box, log_box, error_box):
    t0 = time.monotonic()
    st.session_state["log"] = []
    st.session_state["step_state"] = {"active": 0, "done": [], "finished": False}

    st.session_state["log"].append({
        "t": "+0.0s",
        "k": "INIT",
        "m": f"Launching 4 agents for topic: '{topic}'"
    })
    update_progress(stepper_box, log_box)

    try:
        from Pipeline import run_pipe
    except Exception as exc:
        st.session_state["step_state"]["active"] = None
        st.session_state["log"].append({"t": "+0.0s", "k": "FAIL", "m": "Pipeline import failed"})
        update_progress(stepper_box, log_box)
        error_box.markdown(
            f'<div class="alert-box"><strong>Import Error:</strong> Could not load Pipeline module.<br>{esc(exc)}</div>',
            unsafe_allow_html=True
        )
        return

    def on_step_cb(key: str, title: str, detail: str = ""):
        if key not in STEP_KEYS:
            return
        idx = STEP_KEYS.index(key)
        st.session_state["step_state"] = {
            "active": idx,
            "done": list(range(idx)),
            "finished": False,
        }
        msg = f"{title} — {detail}" if detail else title
        st.session_state["log"].append({
            "t": f"+{time.monotonic() - t0:04.1f}s",
            "k": key.upper(),
            "m": msg,
        })
    try:
        state = run_pipe(topic, on_step=on_step_cb)
    except Exception as exc:
        st.session_state["step_state"]["active"] = None
        err_str = str(exc)
        if "10054" in err_str or "ConnectionResetError" in err_str or "Connection aborted" in err_str:
            user_hint = "Network connection was interrupted by the API server or scraping target. Please click <strong>Research</strong> again to retry."
        else:
            user_hint = esc(err_str)
        st.session_state["log"].append({
            "t": f"+{time.monotonic() - t0:04.1f}s",
            "k": "FAIL",
            "m": err_str,
        })
        update_progress(stepper_box, log_box)
        error_box.markdown(
            f'<div class="alert-box"><strong>Execution Interrupted:</strong> {user_hint}</div>',
            unsafe_allow_html=True
        )
        return

    elapsed = time.monotonic() - t0
    report = state.get("report", "") or ""

    st.session_state["step_state"] = {
        "active": None,
        "done": list(range(len(STEPS))),
        "finished": True,
    }
    st.session_state["log"].append({
        "t": f"+{elapsed:04.1f}s",
        "k": "DONE",
        "m": f"Report complete ({len(report)} chars).",
    })

    payload = {
        "topic": topic,
        "state": state,
        "elapsed": elapsed,
        "timestamp": datetime.now().strftime("%b %d, %Y · %H:%M"),
        "report": report,
    }

    st.session_state["current_result"] = payload
    st.session_state["history"].insert(0, payload)
    update_progress(stepper_box, log_box)


# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.markdown(
        '<div style="font-size:0.95rem; font-weight:600; color:var(--text-bright); margin-bottom:1rem;">'
        'Research Desk</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="panel-title">Session History</div>', unsafe_allow_html=True)
    if not st.session_state["history"]:
        st.caption("No recent research runs.")
    else:
        for idx, item in enumerate(st.session_state["history"]):
            t_short = item["topic"][:26] + ("..." if len(item["topic"]) > 26 else "")
            if st.button(t_short, key=f"hist_{idx}", type="secondary", use_container_width=True):
                st.session_state["current_result"] = item
                st.session_state["selected_topic"] = item["topic"]

        if st.button("Clear History", key="cls_hist", type="secondary", use_container_width=True):
            st.session_state["history"] = []
            st.session_state["current_result"] = None
            st.rerun()

    st.markdown("<br><hr style='border-color:var(--border-subtle);'><br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-title">System Status</div>', unsafe_allow_html=True)
    if MISSING_KEYS:
        st.error(f"Missing: {', '.join(MISSING_KEYS)}")
    else:
        st.success("API Keys Connected")

    # Export Full Session Data
    if st.session_state["history"]:
        st.markdown("<br>", unsafe_allow_html=True)
        session_json = json.dumps(st.session_state["history"], indent=2)
        st.download_button(
            "Export Session JSON",
            data=session_json,
            file_name=f"folio_session_{int(time.time())}.json",
            mime="application/json",
            use_container_width=True,
        )


# --------------------------------------------------------------------------- #
# Main Layout
# --------------------------------------------------------------------------- #
render_brand_bar()

# Perplexity-Style Hero Input View
st.markdown(
    f'<div class="hero-box">'
    f'  <div class="hero-kicker">{KICKER}</div>'
    f'  <div class="hero-title">What would you like to research?</div>'
    f'  <div class="hero-sub">4 AI agents collaborate to search the web, scrape primary sources, synthesize a report, and score the evidence.</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Search Input Bar & Trigger Button (Aligned Perfectly)
c_input, c_btn = st.columns([4.2, 1.2], vertical_alignment="bottom", gap="small")

with c_input:
    topic_query = st.text_input(
        "",
        key="search_field",
        label_visibility="collapsed",
        placeholder="Ask anything (e.g. State of RISC-V in cloud data centers)...",
    )

with c_btn:
    run_btn = st.button("Research", type="primary", use_container_width=True)

warn_box = st.empty()
stepper_box = st.empty()
log_box = st.empty()
error_box = st.empty()

update_progress(stepper_box, log_box)

# Handle Run Trigger
if run_btn:
    active_topic = topic_query.strip()
    if not active_topic:
        warn_box.markdown('<div class="alert-box"><strong>Topic required:</strong> Enter a research prompt above.</div>', unsafe_allow_html=True)
    elif MISSING_KEYS:
        warn_box.markdown(f'<div class="alert-box"><strong>Missing API Keys:</strong> Please add <code>{", ".join(MISSING_KEYS)}</code> to your <code>.env</code> file.</div>', unsafe_allow_html=True)
    else:
        warn_box.empty()
        run_research_pipeline(active_topic, stepper_box, log_box, error_box)
        st.rerun()


# --------------------------------------------------------------------------- #
# Results View
# --------------------------------------------------------------------------- #
if st.session_state.get("current_result"):
    res = st.session_state["current_result"]
    topic = res["topic"]
    state = res["state"]
    report = res["report"]
    elapsed = res["elapsed"]
    timestamp = res["timestamp"]

    word_cnt = count_words(report)
    read_mins = estimate_reading_time(report)
    sources = parse_sources(state.get("search_results", ""))
    score, strengths, improvements, verdict = parse_critic(state.get("feedback", ""))

    st.markdown("<hr style='border-color:var(--border-subtle); margin:2.5rem 0;'>", unsafe_allow_html=True)

    # Result Header Metabar
    st.markdown(
        f'<div class="meta-header">'
        f'  <div class="meta-title">{esc(topic)}</div>'
        f'  <div class="meta-sub">'
        f'      <span>Generated: {timestamp}</span>'
        f'      <span>Time: {elapsed:.1f}s</span>'
        f'      <span>Words: {word_cnt} ({read_mins} min read)</span>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        score_txt = f"{score:g}/10" if score is not None else "—"
        st.markdown(f'<div class="metric-box"><div class="metric-num" style="color:var(--accent-glow);">{score_txt}</div><div class="metric-lbl">Critic Score</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{len(sources)}</div><div class="metric-lbl">Sources Found</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"><div class="metric-num">{word_cnt}</div><div class="metric-lbl">Word Count</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-box"><div class="metric-num" style="color:var(--accent-emerald);">{elapsed:.1f}s</div><div class="metric-lbl">Elapsed Time</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Workspace Tabs
    t_report, t_critic, t_sources, t_logs = st.tabs([
        "📄 Research Report",
        "🎯 Critic Evaluation",
        "🌐 Cited Sources",
        "⚡ Agent Audit Logs",
    ])

    with t_report:
        st.markdown(f'<div class="report-content">{report}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            "Download Markdown (.md)",
            data=report,
            file_name=f"{slugify(topic)}.md",
            mime="text/markdown",
        )

    with t_critic:
        c1, c2 = st.columns([1, 1.8], gap="medium")
        with c1:
            st.markdown(
                f'<div class="card-panel">'
                f'  <div class="panel-title">Overall Score</div>'
                f'  <div class="score-display">{score_txt}</div>'
                f'  {f"<div style=margin-top:1rem;font-style:italic;color:var(--text-bright);>“{esc(verdict)}”</div>" if verdict else ""}'
                f'</div>',
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown('<div class="card-panel">', unsafe_allow_html=True)
            if strengths:
                st.markdown('<div class="panel-title" style="color:var(--accent-emerald);">Strengths</div>', unsafe_allow_html=True)
                st.markdown('<ul class="bullet-list good">' + "".join(f"<li>{esc(s)}</li>" for s in strengths) + '</ul>', unsafe_allow_html=True)

            if improvements:
                st.markdown('<div class="panel-title" style="color:var(--accent-amber); margin-top:1rem;">Areas to Improve</div>', unsafe_allow_html=True)
                st.markdown('<ul class="bullet-list bad">' + "".join(f"<li>{esc(s)}</li>" for s in improvements) + '</ul>', unsafe_allow_html=True)

            if not verdict and not strengths and not improvements:
                st.text(state.get("feedback", "No feedback provided."))
            st.markdown('</div>', unsafe_allow_html=True)

    with t_sources:
        if sources:
            st.markdown('<div class="card-panel">', unsafe_allow_html=True)
            for src in sources:
                u = esc(src["url"])
                t = esc(src["title"])
                d = esc(domain_of(src["url"]))
                st.markdown(
                    f'<a class="source-item" href="{u}" target="_blank" rel="noopener noreferrer">'
                    f'  <span class="source-title">{t}</span>'
                    f'  <span class="source-domain">🌐 {d} ↗</span>'
                    f'</a>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No sources were recorded for this run.")

    with t_logs:
        with st.expander("Finder Agent Search Output", expanded=False):
            st.code(state.get("search_results", ""), language="text")
        with st.expander("Reader Agent Scraped Output", expanded=False):
            st.code(state.get("reader_res", ""), language="text")
        with st.expander("Critic Agent Evaluation Raw Output", expanded=False):
            st.code(state.get("feedback", ""), language="text")
