import streamlit as st
from backend import ask_council, MODELS, saved_questions, ask_offline

LABELS = {"gemini": "Gemini", "groq": "GPT-OSS (Groq)"}

st.set_page_config(page_title="Hive Mind", page_icon="⬡", layout="wide")

st.markdown("""
<style>
.stApp { background: radial-gradient(1000px 500px at 50% -10%, rgba(255,42,61,.25), transparent 60%), #07060a; }
h1.hive { text-align:center; font-size:64px; letter-spacing:.16em; color:#ffe9ea; margin-bottom:0;
  text-shadow:0 0 12px rgba(255,42,61,.9), 0 0 36px rgba(255,42,61,.55); }
.tag { text-align:center; color:#a69598; margin-bottom:24px; }
div.stButton > button { background:linear-gradient(180deg,#e0202f,#a50f1b); color:white;
  border:1px solid #ff2a3d; letter-spacing:.12em; font-weight:700;
  box-shadow:0 0 20px rgba(255,42,61,.5); }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="hive">HIVE MIND</h1>', unsafe_allow_html=True)
st.markdown('<p class="tag">Ask once. Hear the whole hive.</p>', unsafe_allow_html=True)

mode = st.radio("Mode", ["Single AI", "Full Council", "Custom Mix"], horizontal=True)
names = list(MODELS)

if mode == "Single AI":
    selected = [st.selectbox("Choose an AI", names, format_func=lambda n: LABELS[n])]
elif mode == "Full Council":
    selected = names
    st.caption("All AIs will answer, then the Hive merges them.")
else:
    selected = st.multiselect("Pick your AIs", names, default=names,
                              format_func=lambda n: LABELS[n])

offline = st.toggle("Offline demo (saved answers)")

if offline:
    saved = saved_questions()
    question = st.selectbox("Pick a saved question", saved) if saved else ""
else:
    question = st.text_area("Ask the Hive", height=120, placeholder="Type your question...")

if st.button("SUMMON THE HIVE"):
    if not question.strip():
        st.warning("Type a question first.")
    elif not selected:
        st.warning("Pick at least one AI.")
    else:
        with st.spinner("The hive is thinking..."):
            if offline:
                st.session_state["result"] = ask_offline(question)
            else:
                st.session_state["result"] = ask_council(question, selected)
            st.session_state["selected"] = selected
if "result" in st.session_state:
    result = st.session_state["result"]
    sel = st.session_state["selected"]

    st.subheader("Voices of the Hive")
    cols = st.columns(len(sel))
    for col, n in zip(cols, sel):
        with col:
            with st.container(border=True):
                st.markdown("**" + LABELS[n] + "**")
                st.write(result[n])

    if len(sel) >= 2:
        with st.container(border=True):
            st.subheader("HIVE VERDICT")
            st.write(result["final"])