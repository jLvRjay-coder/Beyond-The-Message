# Beyond the Message — Full Build (readability + features)
# Layout: Off-white background, navy headers, gold accents
# Features: 4 weeks expanded, AI Q&A, Holman Insights (preloaded + button), Salvation section, Reflection & Prayer

from __future__ import annotations
import os, json
import streamlit as st
from dotenv import load_dotenv

# ----- Load API key & model -----
load_dotenv()
API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
MODEL   = os.getenv("BTM_MODEL", "gpt-4.1").strip()

# OpenAI client (SDK v1)
client = None
try:
    from openai import OpenAI
    if API_KEY:
        client = OpenAI(api_key=API_KEY)
except Exception:
    client = None


# ================== CONTENT ==================
DEFAULT_WEEKS = {
    "week1": {
        "tag": "moses_obedience",
        "title": "Moses — Obedience & Calling",
        "verse_of_week": "“As my Father hath sent me, even so send I you.” (John 20:21, KJV)",
        "overview": "God calls reluctant men; He supplies what He commands. Obedience grows as we trust His presence over our insufficiency.",
        "scripture": "Exodus 3–4; John 20:21; Acts 2",
        "questions": [
            "Where am I arguing with God’s call?",
            "What sign or grace has He already given me?",
            "Who can I invite to stand with me this week (an ‘Aaron’)?"
        ],
        "notes": [
            "God’s presence, not our eloquence, qualifies the messenger (Ex 3:12; 4:10–12).",
            "Calling clarifies assignment; obedience reveals trust. Excuses fade where God’s name stands.",
            "God often pairs us with others (Moses/Aaron) to steady courage and share the work.",
            "Small obediences precede public breakthroughs; faithfulness in secret forms leaders.",
            "Signs are confirmations of God’s word, not replacements for it."
        ],
        "holman": (
            "In Exodus 3–4, Moses’ reluctance exposes the human tendency to magnify personal limitation over divine sufficiency. "
            "The Lord answers each objection not with flattery but with Himself: ‘I will be with thy mouth’ (Ex 4:12). "
            "Holman notes emphasize how the covenant name (YHWH) anchors mission; God’s ‘I AM’ meets our ‘I am not.’ "
            "Moses’ signs (staff-serpent, leprous hand, Nile blood) authenticate a word already grounded in God’s character. "
            "Obedience, therefore, is worship in motion—action that trusts God’s presence more than human skill."
        )
    },
    "week2": {
        "tag": "david_integrity",
        "title": "David — Repentance & Integrity",
        "verse_of_week": "“Create in me a clean heart, O God.” (Psalm 51:10, KJV)",
        "overview": "Integrity is restored through honest repentance. Grace cleanses, renews, and recommissions leaders.",
        "scripture": "2 Samuel 11–12; Psalm 51; Psalm 32",
        "questions": [
            "Where do I need to repent specifically?",
            "What amends do I need to make this week?",
            "What guardrails will I add to protect integrity?"
        ],
        "notes": [
            "Hidden sin erodes public trust; confession reopens fellowship (Ps 32:3–5).",
            "Repentance is more than regret—it seeks cleansing, renewal, and a steadfast spirit (Ps 51:7–12).",
            "Integrity requires structures: honest community, boundaries, and humble accountability.",
            "God restores the brokenhearted leader to ministry usefulness (Ps 51:13).",
            "Mercy is not permissiveness; grace forms a new sobriety toward temptation."
        ],
        "holman": (
            "David’s prayer in Psalm 51 moves from confession to cleansing to commissioning. "
            "Holman highlights the inner work of God—‘a clean heart,’ ‘a right spirit’—as the true locus of renewal. "
            "Sin fractures vertical fellowship and horizontal vocation; grace heals both. "
            "Nathan’s confrontation (2 Sam 12) reveals how God’s word rescues leaders from self-deception. "
            "Restored integrity is not private sentiment but public service: ‘then will I teach transgressors thy ways’ (Ps 51:13)."
        )
    },
    "week3": {
        "tag": "nehemiah_rebuild",
        "title": "Nehemiah — Vision, Prayer & Rebuilding",
        "verse_of_week": "“The joy of the LORD is your strength.” (Nehemiah 8:10, KJV)",
        "overview": "God births vision through prayer and strengthens hands to build amid opposition.",
        "scripture": "Nehemiah 1–6; Nehemiah 8",
        "questions": [
            "What wall (discipline) needs rebuilding first?",
            "Who is on my wall team?",
            "What opposition do I expect and how will I pray?"
        ],
        "notes": [
            "Burden leads to prayer; prayer births plans; plans become action (Neh 1–2).",
            "Opposition clarifies calling; watchfulness couples with work (Neh 4:17).",
            "Unity in families/teams accelerates progress—everyone builds near his house.",
            "Joy strengthens endurance; Scripture-centered renewal fuels sustainable work (Neh 8:10).",
            "Leaders model both intercession and initiative—knees and hands aligned."
        ],
        "holman": (
            "Holman’s insights on Nehemiah stress covenant identity shaping practical leadership. "
            "The rebuilding is not merely civic but spiritual: walls protect worship. "
            "Prayer saturates planning; the king’s favor is providential, not accidental. "
            "Opposition—mockery, threats, internal fatigue—serves as a stage for faith’s resilience. "
            "Joy arises from hearing and understanding God’s word (Neh 8), fueling a holy perseverance."
        )
    },
    "week4": {
        "tag": "jesus_servant_leadership",
        "title": "Jesus — Servant Leadership & Mission",
        "verse_of_week": "“For even the Son of man came not to be ministered unto, but to minister.” (Mark 10:45, KJV)",
        "overview": "Christ redefines greatness as service; leaders lay down privilege to lift people to the Father.",
        "scripture": "Mark 10:42–45; John 13:1–17; John 20:21",
        "questions": [
            "Where am I conforming to worldly power instead of Christ-like service?",
            "What one act of humble service can I take this week?",
            "Who can I equip and send as Jesus sent the Twelve?"
        ],
        "notes": [
            "Greatness = cross-shaped service; authority is stewardship, not entitlement (Mk 10:42–45).",
            "Jesus washes feet to expose pride and to dignify people we might overlook (Jn 13).",
            "Sending continues the pattern: as the Father sent the Son, so the Son sends us (Jn 20:21).",
            "Holiness and mission are friends: love moves us toward people with truth and grace.",
            "Leadership multiplies when we equip, not just perform."
        ],
        "holman": (
            "Holman notes observe that Jesus reframes leadership through self-giving service. "
            "The basin and towel (John 13) become emblems of authority under love: power kneels. "
            "True sending (John 20:21) carries the character of the Sender; mission without humility distorts the message. "
            "The ransom saying (Mark 10:45) anchors Christian leadership in atonement—our service is derivative of His."
        )
    }
}


# ================== HELPERS ==================
def ai_guard() -> bool:
    if not API_KEY or not client:
        st.error("🔑 AI is disabled. Set OPENAI_API_KEY in your .env and restart.")
        return True
    if not MODEL:
        st.error("⚙️ No model set. Add BTM_MODEL=gpt-4.1 to your .env.")
        return True
    return False


def call_ai(prompt: str, week_meta: dict, mode: str) -> str:
    """Generic AI call with style rules based on mode."""
    if ai_guard():
        return ""
    system = (
        "You are a careful Bible study helper for a Christian men's study called 'Beyond the Message'. "
        "Always ground answers in KJV Scripture (Book Chapter:Verse). "
        "Prefer Holman Study Bible, Matthew Henry, Vine’s, Strong’s. Keep tone pastoral, concise, and faithful."
    )
    if mode == "refs":
        rules = [
            "Return: Summary (1–2 sentences); Key passages (bullets Book Chap:Verse — one-line insight); Application (1–2 bullets)."
        ]
    elif mode == "deeper":
        rules = [
            "Return: Summary (2–3 sentences); Key passages; Cross-references; Word study (brief); Practical applications (3 bullets)."
        ]
    else:  # holman style
        rules = [
            "Return: Holman Study Bible style overview in 2–3 paragraphs: context, theology, and application with KJV references."
        ]
    user = (
        f"Week tag: {week_meta.get('tag','')}\n"
        f"Anchor Scripture: {week_meta.get('scripture','')}\n"
        f"Prompt/Focus: {prompt}\n"
        "Style rules:\n- " + "\n- ".join(rules)
    )
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ API error: {e}")
        return ""


def build_closing(week: dict) -> tuple[str, str]:
    qs = week.get("questions", [])
    q1 = qs[0] if qs else "What is the Lord asking me to do this week?"
    q2 = qs[1] if len(qs) > 1 else "Give me courage to obey."
    q3 = qs[2] if len(qs) > 2 else "Show me one practical step today."
    prayer = (
        "**A Prayer You Can Pray**\n\n"
        f"> Lord Jesus, thank You for Your Word. Concerning this week’s focus, *{q2.lower()}* and *{q3.lower()}*.  \n"
        "> Cleanse my heart, align my motives, and strengthen my hands.  \n"
        "> Fill me with the Holy Ghost for witness and work. In Jesus’ name, amen.\n"
    )
    return q1, prayer


# ================== THEME & PAGE ==================
st.set_page_config(page_title="Beyond the Message", page_icon="✝️", layout="wide")

# Global CSS (readable light theme)
st.markdown(
    """
<style>
/* Background & typography */
body, .main, .block-container { background:#f8f9fa !important; }
.block-container { padding-top: 1.2rem; max-width: 1150px; }
h1, h2, h3 { color:#0a1f44; letter-spacing:.2px; }
h1 { font-weight:800; }
h2 { font-weight:700; margin-top:.25rem; }
p, li, label, span, .stMarkdown { color:#1a1a1a !important; }

/* Cards */
.btm-card {
  background:#ffffff; border:1px solid #e5e7eb; border-radius:14px;
  padding:1rem 1.25rem; box-shadow:0 6px 24px rgba(0,0,0,.06);
  margin-bottom: 1rem;
}

/* Accents */
.btm-quote { border-left:4px solid #d4af37; padding:.6rem 1rem; background:#fff; border-radius:10px; }

/* Sticky header actions */
.btm-sticky { position: sticky; top: 8px; z-index:50; }

/* Buttons */
.stButton>button {
  border-radius:10px; padding:.55rem .9rem; border:1px solid #cbd5e1; background:#ffffff;
}
.stButton>button:hover { border-color:#d4af37; color:#0a1f44; }

/* Collapsible box look */
.summary-box { background:#fffef6; border:1px solid #f2e4b8; border-radius:12px; padding:.8rem 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ================== HEADER ==================
st.markdown("<h1 style='color:#d4af37;'>Beyond the Message</h1>", unsafe_allow_html=True)
st.caption("Empowering men to speak up, lead with courage, and live with faith.")
st.markdown(
    "<em style='color:#0a1f44;'>“Follow me, and I will make you fishers of men.” (Matthew 4:19, KJV)</em>",
    unsafe_allow_html=True,
)

# Salvation sticky button
head_l, head_r = st.columns([7, 5])
with head_r:
    st.markdown("<div class='btm-sticky'>", unsafe_allow_html=True)
    if st.button("✝️ How to be saved"):
        st.session_state["show_salvation"] = True
    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("show_salvation"):
    with st.expander("How to be saved (KJV Scriptures + Prayer)", expanded=True):
        st.markdown(
            "- **Romans 3:23** — For all have sinned, and come short of the glory of God.  \n"
            "- **Romans 6:23** — For the wages of sin is death; but the gift of God is eternal life through Jesus Christ our Lord.  \n"
            "- **Romans 5:8** — But God commendeth his love toward us…  \n"
            "- **Romans 10:9,13** — …thou shalt be saved… whosoever shall call upon the name of the Lord shall be saved.  \n"
            "- **John 3:16** — For God so loved the world…  \n"
            "- **Ephesians 2:8–9** — By grace are ye saved through faith…  \n"
            "- **1 John 5:11–13** — …that ye may know that ye have eternal life.",
        )
        st.markdown(
            "**A Prayer You Can Pray**  \n"
            "> Lord Jesus, I confess I am a sinner and cannot save myself.  \n"
            "> I believe You died for my sins and rose again.  \n"
            "> I turn from sin and place my trust in You alone.  \n"
            "> Please forgive me, make me new, and be Lord of my life.  \n"
            "> I confess You as my Savior. Amen."
        )
        st.success("🙌 If you prayed that prayer, **welcome to God’s family!** (Luke 10:20; Rev 20:15).")

st.markdown("---")

# ================== LAYOUT ==================
left, right = st.columns([7, 5], gap="large")

# ---- LEFT: Weekly content ----
with left:
    st.markdown("<div class='btm-card'>", unsafe_allow_html=True)
    week_slug = st.selectbox(
        "Study Week",
        ["week1", "week2", "week3", "week4"],
        index=0,
    )
    week = DEFAULT_WEEKS[week_slug]

    st.subheader(week["title"])
    st.subheader("Verse of the Week")
    st.markdown(f"<div class='btm-quote'>{week['verse_of_week']}</div>", unsafe_allow_html=True)

    st.subheader("Overview")
    st.write(week["overview"])

    st.subheader("Expanded Study Notes")
    for n in week.get("notes", []):
        st.markdown(f"- {n}")

    st.caption(f"Anchor Scripture (KJV): {week.get('scripture','')}")

    # Collapsible Holman-style insights (preloaded)
    with st.expander("📝 Holman Insights (commentary-style)", expanded=False):
        st.markdown(f"<div class='summary-box'>{week.get('holman','')}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---- RIGHT: Questions + AI ----
with right:
    st.markdown("<div class='btm-card'>", unsafe_allow_html=True)
    st.subheader("Ask & Explore")
    questions = week.get("questions", [])
    q_choice = st.radio("Pick a question:", options=questions, index=0, label_visibility="collapsed")
    custom_q = st.text_input("Or type your own question")
    final_q = (custom_q or q_choice).strip()

    c1, c2, c3 = st.columns(3)
    run_refs   = c1.button("📖 Biblical References")
    run_deeper = c2.button("🔎 Dig Deeper")
    run_holman = c3.button("📝 Holman Insights")

    if final_q and (run_refs or run_deeper or run_holman):
        with st.spinner("Preparing study notes..."):
            mode = "refs" if run_refs else ("deeper" if run_deeper else "holman")
            ans = call_ai(final_q, week, mode)
            if ans:
                st.markdown(ans)
    elif (run_refs or run_deeper or run_holman) and not final_q:
        st.warning("Type a question or choose one from the list first.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---- Reflection & Prayer ----
st.markdown("<div class='btm-card'>", unsafe_allow_html=True)
st.subheader("Reflection & Prayer")
ref_q, prayer_md = build_closing(week)
st.markdown(f"**Reflection Question:** {ref_q}")
st.markdown(prayer_md)
st.markdown("</div>", unsafe_allow_html=True)

