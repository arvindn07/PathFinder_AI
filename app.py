"""
PathFinder AI - Personalized Learning Path Generator
Streamlit prototype

Flow:
1. Goal input screen
2. Diagnostic quiz (maps directly to knowledge-graph topic nodes)
3. Personalized, topologically-sorted learning path with AI-generated
   explanations/resources per topic
4. Progress tracking
"""

import streamlit as st
from topic_graph import get_personalized_path, get_topic_title, validate_graph, build_path_diagram
from quiz import QUIZ_QUESTIONS, score_quiz
from gemini_helper import get_topic_explanation

st.set_page_config(page_title="PathFinder AI", page_icon="🧭", layout="centered")

# Validate graph once at startup
validate_graph()

# ---------------------------------------------------------------------------
# Session state setup
# ---------------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "goal"          # goal -> quiz -> path_overview -> learn
if "goal" not in st.session_state:
    st.session_state.goal = ""
if "known_topics" not in st.session_state:
    st.session_state.known_topics = set()
if "path" not in st.session_state:
    st.session_state.path = []
if "completed" not in st.session_state:
    st.session_state.completed = set()
if "topic_content_cache" not in st.session_state:
    st.session_state.topic_content_cache = {}

st.title("🧭 PathFinder AI")
st.caption("For people who have a goal but don't know the path to get there.")

# ---------------------------------------------------------------------------
# STAGE 1: Goal input
# ---------------------------------------------------------------------------
if st.session_state.stage == "goal":
    st.subheader("What's your goal?")
    goal = st.text_input(
        "Describe what you want to achieve",
        placeholder="e.g. I want to build and deploy ML models",
    )
    st.info("Currently this prototype supports the **ML / Data Science** learning domain.")

    if st.button("Start Diagnostic Quiz", type="primary", disabled=not goal.strip()):
        st.session_state.goal = goal
        st.session_state.stage = "quiz"
        st.rerun()

# ---------------------------------------------------------------------------
# STAGE 2: Diagnostic quiz
# ---------------------------------------------------------------------------
elif st.session_state.stage == "quiz":
    st.subheader("Quick Diagnostic Quiz")
    st.caption("This finds out what you already know, so we don't waste your time on it.")

    with st.form("quiz_form"):
        user_answers = {}
        for q in QUIZ_QUESTIONS:
            user_answers[q["id"]] = st.radio(
                q["question"], q["options"], index=None, key=q["id"]
            )
        submitted = st.form_submit_button("Generate My Path", type="primary")

    if submitted:
        if any(v is None for v in user_answers.values()):
            st.warning("Please answer all questions.")
        else:
            known = score_quiz(user_answers)
            st.session_state.known_topics = known
            st.session_state.path = get_personalized_path(known)
            st.session_state.stage = "path_overview"
            st.rerun()

# ---------------------------------------------------------------------------
# STAGE 3: Path overview (whole roadmap at a glance, before committing to learn)
# ---------------------------------------------------------------------------
elif st.session_state.stage == "path_overview":
    st.subheader(f"Your Path: {st.session_state.goal}")

    known_count = len(st.session_state.known_topics)
    if known_count:
        st.success(
            f"Nice — the quiz shows you already know {known_count} topic(s). "
            f"We've skipped those for you."
        )

    st.caption("Here's the full roadmap to reach your goal, in order.")
    st.divider()

    if st.session_state.path:
        diagram = build_path_diagram(st.session_state.path)
        st.graphviz_chart(diagram, use_container_width=True)
    else:
        st.info("You already know everything on this path! 🎉")

    st.divider()

    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        if st.button("📚 Learn Here", type="primary", use_container_width=True):
            st.session_state.stage = "learn"
            st.rerun()
    with col2:
        if st.button("🔄 Start Over", use_container_width=True):
            for key in ["stage", "goal", "known_topics", "path", "completed", "topic_content_cache"]:
                del st.session_state[key]
            st.rerun()

# ---------------------------------------------------------------------------
# STAGE 4: Learn Here — interactive path with explanations, resources, progress
# ---------------------------------------------------------------------------
elif st.session_state.stage == "learn":
    st.subheader(f"Learning: {st.session_state.goal}")

    total = len(st.session_state.path)
    done = len(st.session_state.completed)
    progress = done / total if total else 0
    st.progress(progress, text=f"{done} / {total} topics completed")

    st.divider()

    for i, topic_id in enumerate(st.session_state.path, 1):
        title = get_topic_title(topic_id)
        is_done = topic_id in st.session_state.completed

        with st.container(border=True):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"**{i}. {title}** {'✅' if is_done else ''}")
            with col2:
                checked = st.checkbox(
                    "Done", value=is_done, key=f"chk_{topic_id}", label_visibility="collapsed"
                )
                if checked and topic_id not in st.session_state.completed:
                    st.session_state.completed.add(topic_id)
                    st.rerun()
                elif not checked and topic_id in st.session_state.completed:
                    st.session_state.completed.discard(topic_id)
                    st.rerun()

            with st.expander("Show explanation & resource"):
                if topic_id not in st.session_state.topic_content_cache:
                    with st.spinner("Generating explanation..."):
                        st.session_state.topic_content_cache[topic_id] = get_topic_explanation(title)
                content = st.session_state.topic_content_cache[topic_id]
                st.write(content["explanation"])
                st.markdown(f"**Resource:** {content['resource']}")

    st.divider()
    if st.button("🔄 Start Over"):
        for key in ["stage", "goal", "known_topics", "path", "completed", "topic_content_cache"]:
            del st.session_state[key]
        st.rerun()
