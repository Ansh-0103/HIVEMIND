import streamlit as st #sreamlit is a library that is use to build user interface for the web app
from backend import ask_council, MODELS, saved_questions, ask_offline 

LABELS = {"gemini": "Gemini", "groq": "GPT-OSS (Groq)"} #gemini: internal identifier,Gemini: display name

st.set_page_config(page_title="Hive Mind", page_icon="⬡", layout="wide") #set the page title, icon, and layout for the web app

#here is the CSS code to style the web app. It changes the background color, text color, button color, and other styles.
st.markdown(""" 
<style> 
.stApp { background: radial-gradient(1000px 500px at 50% -10%, rgba(255,42,61,.25), transparent 60%), #07060a; }
h1.hive { text-align:center; font-size:64px; letter-spacing:.16em; color:#ffe9ea; margin-bottom:0;
  text-shadow:0 0 12px rgba(255,42,61,.9), 0 0 36px rgba(255,42,61,.55); }
.tag { text-align:center; color:#a69598; margin-bottom:24px; }
div.stButton > button { background:linear-gradient(180deg,#e0202f,#a50f1b); color:white;
  border:1px solid #ff2a3d; letter-spacing:.12em; font-weight:700;
  box-shadow:0 0 20px rgba(255,42,61,.5); }
  .pills { display:flex; justify-content:center; gap:10px; margin-bottom:18px;
  font-family:monospace; font-size:12px; letter-spacing:.08em; }
.pill { display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px;
  border:1px solid #3a1620; background:rgba(17,12,20,.8); color:#eadcdf; }
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
</style>
""", unsafe_allow_html=True)
#display markdown content in streamlit
st.markdown('<h1 class="hive">HIVE MIND</h1>', unsafe_allow_html=True)
st.markdown('<p class="tag">Ask once. Hear the whole hive.</p>', unsafe_allow_html=True)
live = not st.session_state.get("offline_mode", False)
dot = "#3de1ff" if live else "#ffb347"
label = "LIVE" if live else "OFFLINE DEMO"
st.markdown(
    f'<div class="pills"><span class="pill"><span class="dot" style="background:{dot};box-shadow:0 0 10px {dot}"></span>{label}</span>'
    f'<span class="pill">{len(MODELS)} AIs online</span></div>',
    unsafe_allow_html=True)

mode = st.radio("Mode", ["Single AI", "Full Council", "Custom Mix"], horizontal=True) #display three horizontal radio buttons for the user to choose the mode of the AI council.
names = list(MODELS)#create list of keys from the MODELS dictionary, which contains the names of the AI models available in the council.
#lambda function is  a short lived function that is written in a single line.
if mode == "Single AI":
    selected = [st.selectbox("Choose an AI", names, format_func=lambda n: LABELS[n])]
elif mode == "Full Council":
    selected = names                 #select all ai models
    st.caption("All AIs will answer, then the Hive merges them.")
else:
    selected = st.multiselect("Pick your AIs", names, default=names,
                              format_func=lambda n: LABELS[n])

offline = st.toggle("Offline demo (saved answers)", key="offline_mode") #toggle button to switch between live and offline mode.

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
        with st.spinner("The hive is thinking..."): #spinner to display loading indicator while the AI models are generating answers.
            if offline:
                st.session_state["result"] = ask_offline(question)
            else:
                st.session_state["result"] = ask_council(question, selected)#sends question to ask council.
            st.session_state["selected"] = selected
if "result" in st.session_state:
    result = st.session_state["result"]
    sel = st.session_state["selected"]

    st.subheader("Voices of the Hive")
    cols = st.columns(len(sel))
    for col, n in zip(cols, sel): #creates a column for each selected AI model and displays the answer from that model in the corresponding column.
        with col:
            with st.container(border=True):
                st.markdown("**" + LABELS[n] + "**")
                st.write(result[n]) #display the answer
    
    if len(sel) >= 2:
        with st.container(border=True):
            st.subheader("HIVE VERDICT")
            st.write(result["final"])
    if result.get("hive"):
        with st.container(border=True):
            st.subheader("LET THE HIVE SPEAK")
            st.write(result["hive"])

    votes = result.get("votes")
    if votes:
        import pandas as pd
        import altair as alt #altair is libraray to create interactive visualizations in python
        df = pd.DataFrame({"AI": [LABELS[n] for n in votes], "Share": list(votes.values())}) #create a table with two columns: "AI":AI model and "Share":Score.
        pie = (alt.Chart(df).mark_arc(innerRadius=60) #create a pie chart with inner radius of 60 pixels to create a donut chart effect.
               .encode(theta="Share:Q",#maps the "Share" column to the angle of each slice in the pie chart.
                       color=alt.Color("AI:N",#specify colors for each slice based on the "AI" column.
                                       scale=alt.Scale(range=["#ff2a3d", "#3de1ff", "#ffb347"]),
                                       legend=alt.Legend(title=None)),#legend title is set to None to remove the legend title from the chart.
                       tooltip=["AI", "Share"])#tooltip to display ai model name and score
               .properties(height=280))
        with st.container(border=True):
            st.subheader("HIVE'S PICK")
            st.caption("How strongly the Hive favours each answer. An AI judge scores them without knowing which AI wrote which.")
            st.altair_chart(pie, use_container_width=True)#display the pie chart
            best = max(votes, key=votes.get)#find the AI model with the highest score in the votes dictionary.
            st.write("The Hive favours **" + LABELS[best] + "** with " + str(votes[best]) + "%.")                   
            