import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- Page Configuration ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&family=Poppins:wght@300;400&display=swap');

/* Background gradient for app */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Main content block (quiz container) - now black */
[data-testid="stVerticalBlock"] {
    background-color: #111111 !important;  /* deep black */
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    color: #ffffff;  /* ensure text is readable */
}

/* General font */
body, .stMarkdown {
    font-family: 'Poppins', sans-serif;
    color: #ffffff;
}

/* Question title */
.question-title {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    font-size: 2.2em !important;
    color: #b399ff;  /* light purple for contrast */
    text-align: center;
    margin-bottom: 20px;
}

/* Radio buttons styling */
.stRadio div[role="radiogroup"] > label {
    font-size: 1.2em;
    background-color: #222222;
    color: #ffffff;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}
.stRadio div[role="radiogroup"] > label:hover {
    background-color: #3b2f5a;
    color: #ffffff;
}

/* Main action button */
.stButton>button {
    border: none;
    border-radius: 20px;
    padding: 12px 30px;
    background-color: #764ba2;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease-in-out;
    width: 100%;
    font-size: 1.3em;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #764ba2;
}

/* Animation for title */
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}
.main-title {
  animation: fadeIn 1s ease-in-out;
}
</style>
""", unsafe_allow_html=True)


# --- Data Dictionaries ---
personality_descriptions = {
    "ISTJ": "The Inspector 🧐: A walking encyclopedia of facts and rules. Extremely loyal, organized, and responsible.",
    "ISFJ": "The Protector 🛡️: Supportive, caring, and reliable. Always looks out for loved ones.",
    "INFJ": "The Advocate 🔮: Insightful, idealistic, and seeks meaning in life.",
    "INTJ": "The Mastermind 🧠: Strategic, logical, and plans everything meticulously.",
    "ISTP": "The Crafter 🛠️: Practical, action-oriented, and loves problem-solving.",
    "ISFP": "The Artist 🎨: Sensitive, spontaneous, and appreciates beauty around them.",
    "INFP": "The Dreamer 몽상가: Creative, idealistic, and guided by values.",
    "INTP": "The Logician 🤓: Analytical, curious, and loves exploring ideas.",
    "ESTP": "The Dynamo ⚡: Energetic, adventurous, and loves thrill and action.",
    "ESFP": "The Performer 🌟: Fun-loving, social, and enjoys being the center of attention.",
    "ENFP": "The Champion 🎉: Enthusiastic, creative, and inspires others.",
    "ENTP": "The Debater 😈: Quick-witted, innovative, and loves a challenge.",
    "ESTJ": "The Executive 👔: Organized, efficient, and natural leader.",
    "ESFJ": "The Consul 🤗: Warm, caring, and values harmony.",
    "ENFJ": "The Protagonist 🧑‍🏫: Charismatic, inspiring, and supportive.",
    "ENTJ": "The Commander 🎖️: Strategic, assertive, and driven leader."
}

compatibility_mapping = {
    "INTJ": [("ENFP", "The ENFP's energy balances the INTJ's structure."), ("ENTJ", "Both are strategic and driven.")],
    "INTP": [("ENTJ", "ENTJ helps turn INTP ideas into reality."), ("ENFJ", "ENFJ's warmth balances INTP's logic.")],
    "ENTJ": [("INTP", "Brains + strategy make a great team."), ("ISTP", "Logical and action-oriented partnership.")],
    "ENTP": [("INFJ", "INFJ fascinates ENTP, ENTP energizes INFJ."), ("INTJ", "Intellectual sparring and innovation.")],
    "INFJ": [("ENTP", "ENTP encourages exploration, INFJ provides depth."), ("ENFP", "Shared ideals and emotional bond.")],
    "INFP": [("ENFJ", "ENFJ supports INFP's dreams."), ("ENTJ", "ENTJ provides direction, INFP creativity.")],
    "ENFJ": [("INFP", "Mutual warmth and support."), ("INTP", "Fascinated by each other's mind and charm.")],
    "ENFP": [("INTJ", "Opposites attract."), ("INFJ", "Idealists connecting emotionally.")],
    "ISTJ": [("ESFP", "ESFP brings fun, ISTJ stability."), ("ISFJ", "Stable, harmonious pairing.")],
    "ISFJ": [("ESTP", "ESTP adventurous, ISFJ supportive."), ("ESFP", "Fun-loving duo.")],
    "ESTJ": [("INTP", "Organizational skills + ideas."), ("ISTP", "Practical and efficient match.")],
    "ESFJ": [("INTP", "ESFJ guides social world, INTP gives ideas."), ("ISFP", "Caring and gentle pairing.")],
    "ISTP": [("ESTJ", "Direct and efficient partnership."), ("ESFJ", "Warmth meets practicality.")],
    "ISFP": [("ENFJ", "ENFJ mentors ISFP's talents."), ("ESFJ", "Harmonious and comfortable pairing.")],
    "ESTP": [("ISFJ", "Balance between thrill and nurturing."), ("ISTJ", "Practical match with occasional clash.")],
    "ESFP": [("ISTJ", "ISTJ stability, ESFP excitement."), ("ISFJ", "Warm and generous duo.")]
}

famous_indians = {
    "INTJ": ["A.P.J. Abdul Kalam", "Jawaharlal Nehru"],
    "INTP": ["Srinivasa Ramanujan", "C.V. Raman"],
    "ENTJ": ["Shah Rukh Khan", "Dhirubhai Ambani"],
    "ENTP": ["Rabindranath Tagore", "Kailash Satyarthi"],
    "INFJ": ["Mahatma Gandhi", "Arundhati Roy"],
    "INFP": ["A.R. Rahman", "Irrfan Khan"],
    "ENFJ": ["Priyanka Chopra Jonas", "Nelson Mandela (Honorary)"],
    "ENFP": ["Kiran Bedi", "Amrita Pritam"],
    "ISTJ": ["Ratan Tata", "Sachin Tendulkar"],
    "ISFJ": ["Mother Teresa", "Anil Kumble"],
    "ESTJ": ["Virat Kohli", "Kapil Dev"],
    "ESFJ": ["Madhuri Dixit", "Anupam Kher"],
    "ISTP": ["M.S. Dhoni", "Aamir Khan"],
    "ISFP": ["Deepika Padukone", "Shashi Kapoor"],
    "ESTP": ["Ranveer Singh", "Virender Sehwag"],
    "ESFP": ["Karan Johar", "Govinda"],
}

# --- Initialize Session State ---
if 'question_index' not in st.session_state:
    st.session_state.question_index = -1
    st.session_state.scores = {'I':0,'E':0,'S':0,'N':0,'T':0,'F':0,'J':0,'P':0}
    st.session_state.answers = {}

# --- Quiz Questions ---
questions = [
    {"question": "After a long week, you'd rather...", "options": {"Have a quiet evening alone": "I", "Go out with a group of friends": "E"}},
    {"question": "When you learn something new, you prefer...", "options": {"Hands-on experience and practical facts": "S", "Exploring theories and abstract concepts": "N"}},
    {"question": "When a friend is upset, you're more likely to...", "options": {"Offer logical solutions to their problem": "T", "Provide emotional support and comfort": "F"}},
    {"question": "On vacation, you prefer to...", "options": {"Follow a well-planned itinerary": "J", "Spontaneously explore and see what happens": "P"}},
    {"question": "In a group, you are often seen as...", "options": {"More reserved and a good listener": "I", "More talkative and easy to approach": "E"}},
    {"question": "You are more interested in...", "options": {"The reality of how things are": "S", "The potential of what things could be": "N"}},
    {"question": "You pride yourself more on being...", "options": {"Fair and impartial": "T", "Compassionate and empathetic": "F"}},
    {"question": "Which sounds more satisfying?", "options": {"Finishing a task and ticking it off a list": "J", "Starting a new, exciting project": "P"}}
]

# --- Main App Logic ---
if st.session_state.question_index == -1:
    st.markdown("<h1 class='main-title' style='text-align: center; color: #667eea;'>Come Here to Know Your Personality ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Answer a fun, quick quiz to unlock your MBTI type!</p>", unsafe_allow_html=True)
    st.markdown("---")
    with st.expander("🤔 So, what's this MBTI thing anyway?"):
        st.write("""
            The **Myers-Briggs Type Indicator (MBTI)** helps you understand yourself by seeing your preferences in four areas:
            - **Introversion (I) vs. Extroversion (E)**
            - **Sensing (S) vs. Intuition (N)**
            - **Thinking (T) vs. Feeling (F)**
            - **Judging (J) vs. Perceiving (P)**
        """)
    with st.expander("🎭 Meet the 16 Personality Types!"):
        for p_type, description in personality_descriptions.items():
            st.markdown(f"**{p_type}** - {description}")
    st.markdown("---")
    if st.button("Start the Quiz!"):
        st.session_state.question_index = 0
        st.rerun()

elif st.session_state.question_index < len(questions):
    st.markdown("---")
    progress_value = (st.session_state.question_index)/len(questions)
    st.progress(progress_value, text=f"Question {st.session_state.question_index+1}/{len(questions)}")
    current_q = questions[st.session_state.question_index]
    st.markdown(f'<p class="question-title">{current_q["question"]}</p>', unsafe_allow_html=True)
    user_answer = st.radio(
        "Select an option:", 
        options=list(current_q["options"].keys()),
        key=f"q_{st.session_state.question_index}",
        label_visibility="collapsed"
    )
    button_label = "Next Question →"
    if st.session_state.question_index == len(questions) - 1:
        button_label = "✨ Reveal My Personality!"
    if st.button(button_label):
        st.session_state.answers[st.session_state.question_index] = user_answer
        st.session_state.question_index += 1
        st.rerun()

else:
    for i, answer in st.session_state.answers.items():
        trait = questions[i]["options"][answer]
        st.session_state.scores[trait] += 1
    scores = st.session_state.scores
    result = ("I" if scores['I'] > scores['E'] else "E") + \
             ("S" if scores['S'] > scores['N'] else "N") + \
             ("T" if scores['T'] > scores['F'] else "F") + \
             ("J" if scores['J'] > scores['P'] else "P")
    st.balloons()
    st.markdown(f"<h2 style='text-align: center;'>Your Predicted Personality Type is...</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #667eea;'>{result}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2em;'>{personality_descriptions[result]}</p>", unsafe_allow_html=True)
    
    # Personality Breakdown
    st.subheader("📊 Your Personality Breakdown")
    col1, col2 = st.columns(2)
    def calculate_percentage(score1, score2, label1, label2):
        total = score1 + score2
        if total == 0: total = 1
        percent1 = round((score1 / total) * 100)
        percent2 = 100 - percent1
        return pd.DataFrame({'Percentage':[percent1, percent2]}, index=[label1,label2])
    with col1:
        st.write("**Energy: Introversion vs. Extroversion**")
        st.bar_chart(calculate_percentage(scores['I'], scores['E'], 'Introversion', 'Extroversion'), color="#FF4B4B")
        st.write("**Decision Making: Thinking vs. Feeling**")
        st.bar_chart(calculate_percentage(scores['T'], scores['F'], 'Thinking', 'Feeling'), color="#3D85C6")
    with col2:
        st.write("**Information: Sensing vs. Intuition**")
        st.bar_chart(calculate_percentage(scores['S'], scores['N'], 'Sensing', 'Intuition'), color="#93C47D")
        st.write("**Lifestyle: Judging vs. Perceiving**")
        st.bar_chart(calculate_percentage(scores['J'], scores['P'], 'Judging', 'Perceiving'), color="#FFD966")
    
    st.markdown("---")
    
    # Famous Indians
    with st.expander("🇮🇳 Famous Indians Who Share Your Type!"):
        for person in famous_indians.get(result, []):
            st.markdown(f"- **{person}**")
    
    # Compatibility
    with st.expander("💖 Find your compatible personality pals!"):
        for comp_type, reason in compatibility_mapping.get(result, []):
            st.subheader(f"🤝 The {comp_type}")
            st.write(f"**Their vibe:** {personality_descriptions[comp_type]}")
            st.write(f"**Why you might click:** {reason}")
    
    st.markdown("---")
    
    # Reset Quiz
    if st.button("Take the Quiz Again!"):
        st.session_state.question_index = -1
        st.session_state.scores = {'I':0,'E':0,'S':0,'N':0,'T':0,'F':0,'J':0,'P':0}
        st.session_state.answers = {}
        st.rerun()
