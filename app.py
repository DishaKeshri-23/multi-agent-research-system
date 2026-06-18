import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS — dark theme matching the reference screenshots ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── tokens ── */
:root {
  --bg:        #0d1117;
  --surface:   #161b27;
  --surface2:  #1e2535;
  --border:    #2a3347;
  --orange:    #f97316;
  --orange-dim:#c05a0d;
  --orange-glow: rgba(249,115,22,.25);
  --text:      #e8eaf0;
  --muted:     #7b8499;
  --white:     #ffffff;
  --green:     #22c55e;
  --green-dim: rgba(34,197,94,.15);
  --blue-dim:  rgba(99,179,237,.12);
}

/* ── reset ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: var(--bg) !important;
  color: var(--text);
  font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
footer { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* remove default streamlit top padding */
[data-testid="stMainBlockContainer"] {
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
  max-width: 1280px !important;
}

/* ── hero ── */
.rm-hero {
  padding: 2.5rem 0 2rem;
}
.rm-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: .68rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: .7rem;
}
.rm-title {
  font-family: 'Syne', sans-serif;
  font-size: clamp(3rem, 6vw, 5.5rem);
  font-weight: 800;
  line-height: .95;
  margin: 0 0 1.2rem;
  letter-spacing: -.02em;
}
.rm-title .white { color: var(--white); }
.rm-title .orange { color: var(--orange); }
.rm-tagline {
  font-size: 1rem;
  color: var(--muted);
  line-height: 1.65;
  max-width: 500px;
}

/* ── input card ── */
.rm-input-wrap {
  margin-top: 2.4rem;
}
.rm-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: .68rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--orange);
  margin-bottom: .55rem;
}

/* override streamlit text_input */
div[data-testid="stTextInput"] input {
  background: var(--surface2) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 10px !important;
  color: var(--white) !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 1rem !important;
  padding: .75rem 1.1rem !important;
  caret-color: var(--orange);
}
div[data-testid="stTextInput"] input:focus {
  border-color: var(--orange) !important;
  box-shadow: 0 0 0 3px var(--orange-glow) !important;
  outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder {
  color: var(--muted) !important;
}

/* ── CTA button ── */
div[data-testid="stButton"] > button {
  width: 100%;
  background: linear-gradient(135deg, var(--orange) 0%, var(--orange-dim) 100%) !important;
  color: var(--white) !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  padding: .8rem 2rem !important;
  letter-spacing: .01em;
  cursor: pointer !important;
  box-shadow: 0 4px 24px var(--orange-glow) !important;
  transition: opacity .15s, box-shadow .15s !important;
}
div[data-testid="stButton"] > button:hover {
  opacity: .9 !important;
  box-shadow: 0 6px 32px rgba(249,115,22,.45) !important;
}
div[data-testid="stButton"] > button:disabled {
  background: var(--surface2) !important;
  color: var(--muted) !important;
  box-shadow: none !important;
}

/* ── suggestion chips ── */
.rm-try-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: .65rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 1.1rem;
  margin-bottom: .5rem;
}
.rm-chips { display: flex; flex-wrap: wrap; gap: .45rem; }
.rm-chip {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: .28rem .75rem;
  font-size: .8rem;
  color: var(--muted);
  cursor: pointer;
  transition: border-color .15s, color .15s;
}
.rm-chip:hover { border-color: var(--orange); color: var(--orange); }

/* ── pipeline panel header ── */
.rm-panel-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 1rem;
  letter-spacing: -.01em;
}

/* ── step cards ── */
.rm-step {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin-bottom: .65rem;
  display: flex;
  align-items: center;
  gap: .9rem;
  transition: border-color .2s, background .2s;
}
.rm-step.active {
  border-color: var(--orange);
  background: rgba(249,115,22,.07);
}
.rm-step.done {
  border-color: var(--green);
  background: var(--green-dim);
}
.rm-step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: .7rem;
  color: var(--orange);
  flex-shrink: 0;
  width: 1.6rem;
}
.rm-step-body { flex: 1; }
.rm-step-name {
  font-weight: 600;
  font-size: .95rem;
  color: var(--white);
  margin-bottom: .15rem;
}
.rm-step-desc {
  font-size: .78rem;
  color: var(--muted);
}
.rm-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: .65rem;
  letter-spacing: .08em;
  text-transform: uppercase;
  padding: .22rem .6rem;
  border-radius: 20px;
  flex-shrink: 0;
}
.badge-wait    { background: var(--surface2); color: var(--muted); }
.badge-running { background: rgba(249,115,22,.2); color: var(--orange); }
.badge-done    { background: var(--green-dim); color: var(--green); }

/* ── status bar ── */
.rm-status {
  font-family: 'JetBrains Mono', monospace;
  font-size: .8rem;
  color: var(--orange);
  padding: .6rem 1rem;
  background: rgba(249,115,22,.08);
  border: 1px solid rgba(249,115,22,.2);
  border-radius: 8px;
  margin-bottom: 1rem;
}
.rm-status-ok {
  font-family: 'JetBrains Mono', monospace;
  font-size: .8rem;
  color: var(--green);
  padding: .6rem 1rem;
  background: var(--green-dim);
  border: 1px solid rgba(34,197,94,.25);
  border-radius: 8px;
  margin-bottom: 1rem;
}

/* ── result sections ── */
.rm-result {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.6rem 1.8rem;
  margin-bottom: 1.2rem;
}
.rm-result-hdr {
  display: flex;
  align-items: center;
  gap: .7rem;
  padding-bottom: .9rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
}
.rm-result-icon { font-size: 1.15rem; }
.rm-result-title {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--white);
  flex: 1;
}
.rm-result-chip {
  font-family: 'JetBrains Mono', monospace;
  font-size: .65rem;
  text-transform: uppercase;
  letter-spacing: .1em;
  padding: .2rem .6rem;
  border-radius: 20px;
  background: rgba(249,115,22,.15);
  color: var(--orange);
}
.rm-result-body {
  font-size: .93rem;
  line-height: 1.8;
  color: #c8ccd8;
  white-space: pre-wrap;
}
.rm-feedback-body {
  font-size: .93rem;
  line-height: 1.8;
  color: #c8ccd8;
  white-space: pre-wrap;
  background: rgba(251,191,36,.06);
  border-left: 3px solid #f59e0b;
  border-radius: 0 8px 8px 0;
  padding: 1rem 1.2rem;
}
.rm-raw-box {
  background: #0a0e16;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: .9rem 1.1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .75rem;
  color: #7b8499;
  max-height: 220px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

/* ── divider ── */
.rm-hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 2rem 0;
}

/* expander override */
details summary {
  background: var(--surface) !important;
  color: var(--muted) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}
details[open] summary {
  border-radius: 8px 8px 0 0 !important;
}

/* download button */
div[data-testid="stDownloadButton"] > button {
  background: var(--surface2) !important;
  color: var(--orange) !important;
  border: 1px solid var(--orange) !important;
  border-radius: 8px !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: .88rem !important;
  padding: .5rem 1.4rem !important;
  box-shadow: none !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: rgba(249,115,22,.1) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in [("result", None), ("running", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

STEPS = [
    ("01", "Search Agent",  "Gathers recent web information"),
    ("02", "Reader Agent",  "Scrapes & extracts deep content"),
    ("03", "Writer Chain",  "Drafts the full research report"),
    ("04", "Critic Chain",  "Reviews & scores the report"),
]
SUGGESTIONS = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress", "Quantum computing 2025"]

def render_pipeline(active=-1, done=set()):
    html = f'<div class="rm-panel-title">Pipeline</div>'
    for i, (num, name, desc) in enumerate(STEPS):
        if i in done:
            cls, bcls, btxt = "done", "badge-done", "✓ done"
        elif i == active:
            cls, bcls, btxt = "active", "badge-running", "● running"
        else:
            cls, bcls, btxt = "", "badge-wait", "waiting"
        html += f"""
        <div class="rm-step {cls}">
          <div class="rm-step-num">{num}</div>
          <div class="rm-step-body">
            <div class="rm-step-name">{name}</div>
            <div class="rm-step-desc">{desc}</div>
          </div>
          <span class="rm-badge {bcls}">{btxt}</span>
        </div>"""
    return html

# ── Layout: left col (input) + right col (pipeline) ───────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    # Hero
    st.markdown("""
    <div class="rm-hero">
      <div class="rm-eyebrow">Multi-Agent AI System</div>
      <div class="rm-title">
        <span class="white">Research</span><span class="orange">Mind</span>
      </div>
      <div class="rm-tagline">
        Four specialised AI agents collaborate — searching, scraping, writing, and
        critiquing — to deliver a polished research report on any topic.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Input
    st.markdown('<div class="rm-label">Research Topic</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
    run_btn = st.button(
        "⚡  Run Research Pipeline",
        disabled=st.session_state.running,
        use_container_width=True,
    )

    # Suggestion chips
    st.markdown('<div class="rm-try-label">Try →</div>', unsafe_allow_html=True)
    chips_html = '<div class="rm-chips">' + "".join(
        f'<span class="rm-chip">{s}</span>' for s in SUGGESTIONS
    ) + "</div>"
    st.markdown(chips_html, unsafe_allow_html=True)

with col_right:
    pipeline_ph = st.empty()
    pipeline_ph.markdown(render_pipeline(), unsafe_allow_html=True)

# ── Status bar placeholder (full width, below columns) ─────────────────────────
status_ph = st.empty()

# ── Run ────────────────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.running = True
    st.session_state.result = None
    done_steps = set()
    state = {}

    def step(idx, msg):
        pipeline_ph.markdown(render_pipeline(active=idx, done=done_steps), unsafe_allow_html=True)
        status_ph.markdown(f'<div class="rm-status">● {msg}</div>', unsafe_allow_html=True)

    # Step 0
    step(0, "Search agent is gathering sources…")
    sa = build_search_agent()
    res = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
    state["search_results"] = res["messages"][-1].content
    done_steps.add(0)

    # Step 1
    step(1, "Reader agent is scraping top resources…")
    ra = build_reader_agent()
    res2 = ra.invoke({"messages": [("user",
        f"Based on the following search results about '{topic}', "
        f"pick the most relevant URL and scrape it for deeper content.\n\n"
        f"Search Results:\n{state['search_results'][:800]}")]})
    state["scraped_content"] = res2["messages"][-1].content
    done_steps.add(1)

    # Step 2
    step(2, "Writer is drafting the research report…")
    combined = (f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}")
    state["report"] = writer_chain.invoke({"topic": topic, "research": combined})
    done_steps.add(2)

    # Step 3
    step(3, "Critic is reviewing and scoring the report…")
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    done_steps.add(3)

    pipeline_ph.markdown(render_pipeline(active=-1, done=done_steps), unsafe_allow_html=True)
    status_ph.markdown('<div class="rm-status-ok">✓ Research complete — report ready below</div>', unsafe_allow_html=True)
    st.session_state.result = state
    st.session_state.running = False

elif run_btn and not topic.strip():
    status_ph.markdown('<div class="rm-status">⚠ Enter a topic first</div>', unsafe_allow_html=True)

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result
    st.markdown('<hr class="rm-hr">', unsafe_allow_html=True)

    with st.expander("🔍  Raw Search Results", expanded=False):
        st.markdown(f'<div class="rm-raw-box">{res["search_results"]}</div>', unsafe_allow_html=True)

    with st.expander("📄  Scraped Web Content", expanded=False):
        st.markdown(f'<div class="rm-raw-box">{res["scraped_content"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rm-result">
      <div class="rm-result-hdr">
        <span class="rm-result-icon">✍️</span>
        <span class="rm-result-title">Research Report</span>
        <span class="rm-result-chip">Final Output</span>
      </div>
      <div class="rm-result-body">{res['report']}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rm-result">
      <div class="rm-result-hdr">
        <span class="rm-result-icon">🧐</span>
        <span class="rm-result-title">Critic Feedback</span>
        <span class="rm-result-chip">Quality Review</span>
      </div>
      <div class="rm-feedback-body">{res['feedback']}</div>
    </div>""", unsafe_allow_html=True)

    st.download_button(
        "⬇  Download Report as .txt",
        data=res["report"],
        file_name=f"research_{topic[:40].replace(' ','_')}.txt",
        mime="text/plain",
    )