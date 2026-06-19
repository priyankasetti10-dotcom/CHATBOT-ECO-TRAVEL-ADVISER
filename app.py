# =============================================================================
# TerraRoute AI  —  Eco Travel Assistant
# Pure native Streamlit components only (no raw HTML in content)
# =============================================================================

import streamlit as st
import requests
import uuid
import random
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TerraRoute AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# ── CSS (styling only — no content) ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

*, body { font-family: 'Inter', sans-serif !important; }

/* App background */
.stApp {
    background: linear-gradient(135deg, #020c18 0%, #041428 50%, #020c18 100%) !important;
}

/* Hide chrome */
#MainMenu, footer { display:none !important; }
.block-container { padding-top: 1rem !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020c18 !important;
    border-right: 1px solid rgba(0,180,255,0.15) !important;
}

/* All text default */
p, li, span, label { color: #c8dff0 !important; }
h1, h2, h3 { color: #00d4ff !important; }

/* Metric labels */
[data-testid="stMetricLabel"]  > div { color: rgba(0,180,255,0.65) !important; font-size:11px !important; letter-spacing:1px !important; text-transform:uppercase !important; }
[data-testid="stMetricValue"]  > div { color: #ffd700 !important; font-size:22px !important; font-weight:800 !important; }
[data-testid="stMetricDelta"] > div  { font-size:11px !important; }

/* Progress bars */
[data-testid="stProgressBar"] > div > div {
    border-radius: 4px !important;
}

/* Chat container background */
[data-testid="stChatMessageContent"] {
    background: rgba(0,40,80,0.45) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0,180,255,0.12) !important;
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"])
[data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(0,80,160,0.6), rgba(0,50,110,0.6)) !important;
    border-color: rgba(0,160,255,0.25) !important;
}

/* Bot message */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"])
[data-testid="stChatMessageContent"] {
    background: rgba(0,180,255,0.06) !important;
    border-color: rgba(0,180,255,0.15) !important;
}

/* Message text */
[data-testid="stChatMessageContent"] p  { color: #ddeeff !important; line-height: 1.6 !important; }
[data-testid="stChatMessageContent"] li { color: #c8e4f8 !important; }
[data-testid="stChatMessageContent"] strong { color: #00d4ff !important; }
[data-testid="stChatMessageContent"] code {
    background: rgba(0,100,180,0.3) !important;
    color: #7ee8ff !important;
    border-radius:4px !important;
    padding:1px 5px !important;
}

/* ── BLACK INPUT BOX ── */
.stChatInput textarea {
    background-color: #000000 !important;
    color: #00d4ff !important;
    border: 2px solid rgba(0,180,255,0.4) !important;
    border-radius: 14px !important;
    font-size: 14px !important;
    caret-color: #00d4ff !important;
    padding: 14px 16px !important;
}
.stChatInput textarea:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}
.stChatInput textarea::placeholder { color: #1a5070 !important; }
.stChatInput button {
    background: linear-gradient(135deg,#0066cc,#0044aa) !important;
    border-radius: 10px !important;
}

/* Quick-action buttons */
div[data-testid="column"] .stButton > button {
    background: rgba(0,40,90,0.7) !important;
    color: #7ec8e3 !important;
    border: 1px solid rgba(0,140,200,0.25) !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 9px 6px !important;
    width: 100% !important;
    transition: all 0.18s !important;
    text-align: center !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: rgba(0,90,180,0.8) !important;
    border-color: rgba(0,210,255,0.5) !important;
    color: #ffffff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px rgba(0,150,255,0.2) !important;
}

/* Primary action buttons (sidebar) */
.stButton > button {
    background: rgba(0,30,70,0.8) !important;
    color: #7ec8e3 !important;
    border: 1px solid rgba(0,140,200,0.25) !important;
    border-radius: 8px !important;
}

/* Info / success / warning boxes */
[data-testid="stInfo"]    { background: rgba(0,60,120,0.4) !important; border-color: rgba(0,140,200,0.3) !important; }
[data-testid="stSuccess"] { background: rgba(0,60,30,0.4)  !important; border-color: rgba(0,180,80,0.3)  !important; }
[data-testid="stWarning"] { background: rgba(80,50,0,0.4)  !important; border-color: rgba(200,150,0,0.3) !important; }
[data-testid="stError"]   { background: rgba(80,0,0,0.4)   !important; border-color: rgba(200,50,50,0.3) !important; }

/* Divider */
hr { border-color: rgba(0,140,200,0.15) !important; }

/* Caption */
.stCaptionContainer p { color: rgba(100,160,200,0.55) !important; font-size:10.5px !important; }

/* Expander */
[data-testid="stExpander"] {
    background: rgba(0,20,50,0.6) !important;
    border: 1px solid rgba(0,140,200,0.18) !important;
    border-radius: 10px !important;
}
[data-testid="stExpanderDetails"] p { color: #b8d8f0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    D = {
        "sid":    str(uuid.uuid4())[:10],
        "msgs":   [],
        "n":      0,
        "online": False,
        "trip": {"Destination":"—","Dates":"—","Budget":"—",
                 "Travelers":"—","Eco Level":"—"},
    }
    for k, v in D.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()


# ── Helpers ───────────────────────────────────────────────────────────────────
def ping() -> bool:
    try:
        return requests.get("http://localhost:5005/", timeout=3).status_code == 200
    except Exception:
        return False

def ask_rasa(text: str) -> list:
    try:
        r = requests.post(RASA_URL,
            json={"sender": st.session_state.sid, "message": text},
            timeout=15)
        return r.json() if r.status_code == 200 else [{"text": f"Server error {r.status_code}"}]
    except requests.ConnectionError:
        return [{"text": "**Cannot connect to Rasa.**\n\nEnsure both servers are running:\n```\nrasa run actions\nrasa run --enable-api --cors \"*\"\n```"}]
    except Exception as e:
        return [{"text": f"Error: {e}"}]

def extract_slots(text: str):
    t, tl = st.session_state.trip, text.lower()
    for key, markers in [
        ("Destination", ["destination:"]),
        ("Dates",       ["travel dates:", "dates:"]),
        ("Budget",      ["budget:"]),
        ("Travelers",   ["travelers:"]),
        ("Eco Level",   ["sustainability level:", "sustainability:"]),
    ]:
        for m in markers:
            if m in tl:
                after = text[text.lower().find(m) + len(m):]
                val = after.split("\n")[0].strip().lstrip("*").strip()
                if val and val != "—":
                    t[key] = val

def push(role: str, content: str):
    st.session_state.msgs.append({
        "role": role, "content": content,
        "ts": datetime.now().strftime("%H:%M")
    })
    st.session_state.n += 1
    if role == "assistant":
        extract_slots(content)

def send(text: str):
    text = text.strip()
    if not text:
        return
    push("user", text)
    with st.spinner("TerraRoute is thinking…"):
        for resp in ask_rasa(text):
            if resp.get("text"):
                push("assistant", resp["text"])


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;font-size:2rem;margin-bottom:0;'>"
    "🌐 TerraRoute AI</h1>"
    "<p style='text-align:center;color:rgba(0,180,255,0.5);font-size:12px;"
    "letter-spacing:3px;text-transform:uppercase;margin-top:2px;'>"
    "Intelligent Eco Travel Assistant · Powered by Rasa</p>",
    unsafe_allow_html=True
)
st.divider()

# ── Top metrics row ───────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
t = st.session_state.trip
m1.metric("🗺️ Destination",   t["Destination"])
m2.metric("📅 Dates",          t["Dates"])
m3.metric("💰 Budget",         t["Budget"])
m4.metric("👥 Travelers",      t["Travelers"])
m5.metric("🌱 Eco Level",      t["Eco Level"])
st.divider()

# ── Main columns ─────────────────────────────────────────────────────────────
chat_col, info_col = st.columns([2.4, 1], gap="large")


# ═══════════════════
#  LEFT — CHAT
# ═══════════════════
with chat_col:
    st.markdown("#### 💬 Chat with TerraRoute AI")

    # Messages
    chat_box = st.container(height=440, border=True)
    with chat_box:
        if not st.session_state.msgs:
            st.markdown(
                "<div style='text-align:center;padding:60px 20px;"
                "color:rgba(0,180,255,0.3);font-size:13px;'>"
                "🌐<br><br>No messages yet.<br>"
                "<span style='font-size:11px'>Use a Quick Action or type below</span>"
                "</div>",
                unsafe_allow_html=True
            )
        for msg in st.session_state.msgs:
            av = "🌐" if msg["role"] == "assistant" else "🧑"
            with st.chat_message(msg["role"], avatar=av):
                st.markdown(msg["content"])
                st.caption(msg["ts"])

    # Black input
    user_in = st.chat_input("Message TerraRoute AI…  (e.g. 'Plan a trip to Iceland')")
    if user_in:
        send(user_in)
        st.rerun()

    # Quick Actions
    st.markdown(
        "<p style='color:rgba(0,180,255,0.45);font-size:10px;font-weight:700;"
        "letter-spacing:2px;text-transform:uppercase;margin:10px 0 6px;'>"
        "⚡ QUICK ACTIONS</p>",
        unsafe_allow_html=True
    )
    qa_list = [
        ("🗺️ Plan My Trip",      "I want to plan an eco-friendly trip"),
        ("🏨 Eco Hotels",         "Show me eco-friendly hotels"),
        ("🚄 Green Transport",    "What are sustainable transport options?"),
        ("🌍 Carbon Calculator",  "Calculate my carbon footprint"),
        ("🎭 Local Activities",   "What eco-friendly activities are available?"),
        ("♻️ Carbon Offsets",     "Tell me about carbon offset programs"),
        ("🎒 Packing Tips",       "What should I pack for an eco trip?"),
        ("👤 Human Specialist",   "Connect me to a human agent"),
    ]
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    for i, (lbl, msg) in enumerate(qa_list):
        with cols[i % 4]:
            if st.button(lbl, key=f"qa_{i}", use_container_width=True):
                send(msg)
                st.rerun()


# ═══════════════════
#  RIGHT — INFO
# ═══════════════════
with info_col:

    # Connection
    if st.button("🔗 Check Connection", use_container_width=True):
        st.session_state.online = ping()
        st.rerun()
    if st.session_state.online:
        st.success("✅ Connected to Rasa API")
    else:
        st.warning("⚠️ Rasa Offline — click to check")

    st.divider()

    # ── CO₂ Transport Comparison ──────────────────────────────────────────
    st.markdown("**📊 CO₂ Emissions per km**")
    transport = [
        ("✈️ Flight",    255, "#ff4444"),
        ("⛴️ Ferry",    113, "#ff8800"),
        ("🚌 Bus",        89, "#ffcc00"),
        ("⚡ EV",         53, "#44aaff"),
        ("🚂 Train",      41, "#00cc88"),
        ("🚴 Cycling",     0, "#00ff88"),
    ]
    for icon_name, co2, color in transport:
        pct = co2 / 255
        c_left, c_bar = st.columns([1.1, 2])
        with c_left:
            st.markdown(
                f"<span style='font-size:11.5px;color:#9bbfdb'>{icon_name}</span>",
                unsafe_allow_html=True
            )
        with c_bar:
            st.markdown(
                f"<div style='background:rgba(0,40,80,0.5);border-radius:6px;"
                f"height:16px;margin-top:4px;overflow:hidden;'>"
                f"<div style='width:{int(pct*100)}%;background:{color};"
                f"height:100%;border-radius:6px;opacity:0.8'></div></div>"
                f"<span style='font-size:9px;color:rgba(140,180,210,0.6)'>{co2} g/km</span>",
                unsafe_allow_html=True
            )

    st.divider()

    # ── Trip Details ──────────────────────────────────────────────────────
    with st.expander("📋 Your Trip Details", expanded=True):
        for k, v in st.session_state.trip.items():
            ca, cb = st.columns([1, 1.3])
            ca.markdown(f"<span style='color:rgba(0,180,255,0.55);font-size:11.5px'>{k}</span>", unsafe_allow_html=True)
            cb.markdown(f"<span style='color:#b8d9f0;font-weight:600;font-size:11.5px'>{v}</span>", unsafe_allow_html=True)

    # ── Random Eco Fact ───────────────────────────────────────────────────
    facts = [
        "🌊 Trains use 90% less CO₂ than flights on the same route.",
        "🌲 1 tree absorbs ~22 kg CO₂/year. A short-haul flight emits ~255 kg.",
        "⚡ EV rentals produce 78% less CO₂ than petrol cars.",
        "🚂 Night trains replace flights AND save hotel costs.",
        "♻️ Eco hotels use 30% less water than conventional hotels.",
        "🐢 97% of sea turtles nest on eco-tourism-protected beaches.",
        "🌱 Local food cuts meal carbon footprint by up to 80%.",
        "🏔️ 150+ Alpine glaciers have disappeared since 1900.",
    ]
    st.info(f"💡 **Eco Insight**\n\n{random.choice(facts)}")

    # ── Eco Score Guide ───────────────────────────────────────────────────
    with st.expander("🏅 Eco Score Guide"):
        scores = [
            ("🟢", "90–100", "Excellent",   0.95),
            ("🟡", "70–89",  "Good",         0.75),
            ("🟠", "50–69",  "Fair",         0.55),
            ("🔴", "< 50",   "Needs Work",   0.35),
        ]
        for dot, rng, label, pct in scores:
            st.markdown(
                f"<span style='font-size:12px'>{dot} **{rng}** — {label}</span>",
                unsafe_allow_html=True
            )
            st.progress(pct)

    st.divider()

    # ── Reset + Export ────────────────────────────────────────────────────
    r1, r2 = st.columns(2)
    with r1:
        if st.button("🔄 Reset Chat", use_container_width=True, key="reset_btn"):
            for k in ["msgs", "n", "sid", "trip", "online"]:
                st.session_state.pop(k, None)
            st.rerun()
    with r2:
        if st.session_state.msgs:
            log = "\n".join(
                f"[{m['ts']}] {m['role'].upper()}: {m['content']}"
                for m in st.session_state.msgs
            )
            st.download_button(
                "📥 Export", log,
                file_name=f"terraroute_{st.session_state.sid}.txt",
                mime="text/plain",
                use_container_width=True,
                key="export_btn"
            )

    st.caption(f"Session `{st.session_state.sid}` · {st.session_state.n} messages")
