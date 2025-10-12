import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="MBTI Personality AI",
    page_icon="✨",
    layout="wide"
)

# --- Custom CSS for the New Purple Theme ---
st.markdown("""
<style>
/* Import stylish and readable Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&family=Poppins:wght@300;400&display=swap');

/* FIXED: A beautiful purple gradient background */
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Style the main content block to look like a modern card */
[data-testid="stVerticalBlock"] {
    background-color: white;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.07);
}

/* General font for readability */
body, .stMarkdown {
    font-family: 'Poppins', sans-serif;
    color: #333333;
}

/* Style the Question Font */
.question-title {
    font-family: 'Quicksand', sans-serif;
    font-weight: 700;
    font-size: 2.2em !important;
    color: #667eea; /* Purple color */
    text-align: center;
    margin-bottom: 20px;
}

/* Style the answer choices */
.stRadio div[role="radiogroup"] > label {
    font-size: 1.2em;
    background-color: #F0F2F6;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
}

/* Style the main action button */
.stButton>button {
    border: none;
    border-radius: 20px;
    padding: 12px 30px;
    background-color: #764ba2; /* Matching purple */
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

/* Animation for the title */
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

.main-title {
  animation: fadeIn 1s ease-in-out;
}
</style>
""", unsafe_allow_html=True)


# --- Data Dictionaries (Descriptions, Compatibility, etc.) ---
personality_descriptions = {
    "ISTJ": "The Inspector 🧐: A walking encyclopedia of facts and rules. They probably have a color-coded spreadsheet for their sock drawer. Extremely loyal, but don't you dare mess up their perfectly organized system.",
    "ISFJ": "The Protector 🛡️: The kindest, most supportive person you'll ever meet. They remember your birthday, your dog's birthday, and that one time you mentioned you liked a certain type of cookie. They run on tea and the happiness of others.",
    "INFJ": "The Advocate 🔮: A mystical unicorn who understands your soul better than you do. They have deep thoughts, a strong moral compass, and are probably planning how to quietly save the world. Also needs 3-5 business days to recover from a party.",
    "INTJ": "The Mastermind 🧠: Has a plan for everything, including a backup plan for the backup plan. Their brain is a finely tuned machine running on logic, sarcasm, and coffee. Socializing is a task to be optimized for efficiency.",
    "ISTP": "The Crafter 🛠️: The cool, quiet person who can suddenly fix a car, build a computer, or master a new skill in an afternoon. They live in the world of action and have little patience for theoretical nonsense. Motto: 'Why talk when you can do?'",
    "ISFP": "The Artist 🎨: A sensitive soul who sees beauty everywhere. They live in the moment and express themselves through art, music, or a killer sense of style. Spontaneous, charming, and likely to disappear on a whim to follow a butterfly.",
    "INFP": "The Dreamer 몽상가: A poetic soul living in a world of beautiful melancholy and epic daydreams. Their head is full of stories, ideals, and a deep desire for authenticity. They feel everything, all the time. Protect them at all costs.",
    "INTP": "The Logician 🤓: A walking library of random, brilliant ideas. They love debating abstract concepts and will happily fall down a Wikipedia rabbit hole for 6 hours. Small talk is their personal kryptonite.",
    "ESTP": "The Dynamo ⚡: The life of the party and a thrill-seeker. They're energetic, charismatic, and live for the moment. Rules are more like... gentle suggestions. They're probably bungee jumping while closing a business deal on the phone.",
    "ESFP": "The Performer 🌟: A literal burst of sunshine and confetti. They love being the center of attention and making everyone laugh. Life is a stage, and they are the star. Spontaneous and fun, their motto is 'YOLO'.",
    "ENFP": "The Champion 🎉: An enthusiastic puppy in human form. They have a million ideas, a million friends, and a passionate belief that everything is possible. They'll start five projects today and forget about them tomorrow, but with infectious joy.",
    "ENTP": "The Debater 😈: Loves a good argument more than anything. They'll play devil's advocate just to see what happens. Quick-witted, innovative, and will challenge every idea you've ever had, mostly just for fun.",
    "ESTJ": "The Executive 👔: Born to be a boss. They are organized, efficient, and have a plan to make sure everyone else is, too. They get things done, period. Their idea of relaxing is making a to-do list for their relaxation time.",
    "ESFJ": "The Consul 🤗: The ultimate social butterfly and community organizer. They know everyone's name, story, and favorite snack. Extremely caring and practical, they are the glue that holds the friend group together.",
    "ENFJ": "The Protagonist 🧑‍🏫: An inspiring and charismatic leader who wants to help everyone reach their full potential. They are passionate, persuasive, and genuinely believe in people. They can't help but try to motivate everyone, including their houseplants.",
    "ENTJ": "The Commander 🎖️: A natural-born leader with a will of iron. They see the big picture and have a strategic plan to conquer it. If you don't have a goal, they will assign you one. Challenge accepted? Always."
}
compatibility_mapping = {
    # Compatibility mapping is the same as before
    "INTJ": [("ENFP", "The ENFP's spontaneous energy brings the INTJ out of their shell, while the INTJ's planning helps ground the ENFP's brilliant chaos."), ("ENTJ", "A true power couple. Both are strategic, driven, and understand the need for a well-executed plan.")],
    "INTP": [("ENTJ", "The ENTJ can help turn the INTP's theoretical ideas into reality, while the INTP offers unique perspectives the ENTJ might miss."), ("ENFJ", "The ENFJ's warmth and social grace can draw the INTP out, creating a balanced and inspiring connection.")],
    "ENTJ": [("INTP", "A partnership of intellect and strategy. The INTP provides the genius ideas, and the ENTJ builds the empire."), ("ISTP", "Both are logical and action-oriented, creating a highly efficient and practical team.")],
    "ENTP": [("INFJ", "A deeply intriguing match. The INFJ's insight fascinates the ENTP, while the ENTP's wit and energy captivate the INFJ."), ("INTJ", "An unstoppable force of intellectual sparring and grand-scale innovation.")],
    "INFJ": [("ENTP", "The ENTP's adventurous spirit encourages the INFJ to explore, while the INFJ's depth provides a meaningful connection for the ENTP."), ("ENFP", "A bond built on shared ideals, deep conversations, and mutual understanding of each other's inner worlds.")],
    "INFP": [("ENFJ", "The ENFJ is the supportive champion for the INFP's dreams, providing encouragement and structure to their creative passions."), ("ENTJ", "An unlikely a powerful pair. The ENTJ provides direction, while the INFP offers creativity and a strong moral compass.")],
    "ENFJ": [("INFP", "A relationship full of warmth and mutual support. The ENFJ loves to nurture the INFP's gentle spirit."), ("INTP", "The ENFJ is fascinated by the INTP's mind, and the INTP is drawn to the ENFJ's charismatic warmth.")],
    "ENFP": [("INTJ", "The classic 'opposites attract' pairing. The INTJ's structure and the ENFP's spontaneity create a perfect balance."), ("INFJ", "Two idealists who connect on a deep, emotional level, sharing a passion for making the world a better place.")],
    "ISTJ": [("ESFP", "The ESFP brings fun and excitement to the ISTJ's stable world, while the ISTJ provides a sense of security and reliability."), ("ISFJ", "A stable, harmonious pairing built on shared values of duty, loyalty, and practical care.")],
    "ISFJ": [("ESTP", "The ESTP's adventurous nature helps the ISFJ step out of their comfort zone, while the ISFJ offers a warm, stable home base."), ("ESFP", "A fun-loving and caring duo who both enjoy creating wonderful experiences for others.")],
    "ESTJ": [("INTP", "The ESTJ's organizational skills can bring the INTP's brilliant theories to life, creating a productive and logical team."), ("ISTP", "Both are no-nonsense, practical types who respect competence and get things done.")],
    "ESFJ": [("INTP", "The ESFJ helps the INTP navigate the social world with ease, while the INTP offers the ESFJ new and interesting ideas to think about."), ("ISFP", "A gentle and caring match. The ESFJ creates a secure environment for the ISFP to be their authentic, artistic self.")],
    "ISTP": [("ESTJ", "A direct and efficient partnership. Both are grounded in reality and respect each other's competence and independence."), ("ESFJ", "The ESFJ's warmth can help the ISTP connect with their feelings, while the ISTP's practicality keeps things grounded.")],
    "ISFP": [("ENFJ", "The ENFJ is a natural mentor who can help the ISFP find direction for their artistic talents."), ("ESFJ", "A harmonious pairing where both types value creating a beautiful and comfortable environment for their loved ones.")],
    "ESTP": [("ISFJ", "The ISFJ's nurturing nature provides a stable counterpoint to the ESTP's thrill-seeking tendencies."), ("ISTJ", "A straightforward and practical match, although the ESTP's spontaneity might occasionally clash with the ISTJ's love of routine.")],
    "ESFP": [("ISTJ", "The ISTJ provides the stability that the ESFP secretly craves, while the ESFP brings color and excitement into the ISTJ's life."), ("ISFJ", "A warm, fun, and generous couple who love hosting parties and taking care of their friends.")],
}
famous_indians = {
    # Famous Indians mapping is the same as before
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
    st.session_state.question_index = -1 # -1 indicates the start screen
    st.session_state.scores = {'I': 0, 'E': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
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


# --- Main App Logic (Start Screen, Quiz, or Results) ---

# State -1: Show the initial welcome screen
if st.session_state.question_index == -1:
    st.markdown("<h1 class='main-title' style='text-align: center; color: #667eea;'>Come Here to Know Your Personality ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Answer a fun, quick quiz to unlock your MBTI type!</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # FIXED: The explainer sections are now on the start screen
    with st.expander("🤔 So, what's this MBTI thing anyway?"):
        st.write("""
            The **Myers-Briggs Type Indicator (MBTI)** is basically a personality sorting hat! It helps you understand yourself by seeing your preferences in four key areas:
            - **Introversion (I) vs. Extroversion (E):** Where do you get your energy? 🔋 (Cozy blanket fort vs. Big party)
            - **Sensing (S) vs. Intuition (N):** How do you see the world? 🌎 (What is vs. What could be)
            - **Thinking (T) vs. Feeling (F):** How do you make decisions? 🧠 (Logic & facts vs. Harmony & hearts)
            - **Judging (J) vs. Perceiving (P):** How do you like to live? 🗓️ (Checklists & plans vs. Go with the flow)
        """)

    with st.expander("🎭 Meet the 16 Personality Types!"):
        for p_type, description in personality_descriptions.items():
            st.markdown(f"**{p_type}** - {description}")

    st.markdown("---")
    if st.button("Start the Quiz!"):
        st.session_state.question_index = 0
        st.rerun()

# State 0 to n-1: Show the quiz questions
elif st.session_state.question_index < len(questions):
    st.markdown("---")
    
    # Progress Bar
    progress_value = (st.session_state.question_index) / len(questions)
    st.progress(progress_value, text=f"Question {st.session_state.question_index + 1}/{len(questions)}")
    
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

# State n: Show the results
else:
    # Calculate final scores
    for i, answer in st.session_state.answers.items():
        trait = questions[i]["options"][answer]
        st.session_state.scores[trait] += 1
    
    scores = st.session_state.scores
    result = ("I" if scores['I'] > scores['E'] else "E") + \
             ("S" if scores['S'] > scores['N'] else "N") + \
             ("T" if scores['T'] > scores['F'] else "F") + \
             ("J" if scores['J'] > scores['P'] else "P")

    st.balloons()
    
    # --- All the result page features ---
    st.markdown(f"<h2 style='text-align: center;'>Your Predicted Personality Type is...</h2>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: #667eea;'>{result}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2em;'>{personality_descriptions[result]}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Trait Percentages
    st.subheader("📊 Your Personality Breakdown")
    col1, col2 = st.columns(2)
    def calculate_percentage(score1, score2, label1, label2):
        total = score1 + score2
        if total == 0: total = 1
        percent1 = round((score1 / total) * 100)
        percent2 = 100 - percent1
        return pd.DataFrame({'Percentage': [percent1, percent2]}, index=[label1, label2])
    with col1:
        st.write("**Energy: Introversion (I) vs. Extroversion (E)**")
        ie_df = calculate_percentage(scores['I'], scores['E'], 'Introversion', 'Extroversion')
        st.bar_chart(ie_df, color="#FF4B4B")
        st.write("**Decision Making: Thinking (T) vs. Feeling (F)**")
        tf_df = calculate_percentage(scores['T'], scores['F'], 'Thinking', 'Feeling')
        st.bar_chart(tf_df, color="#3D85C6")
    with col2:
        st.write("**Information: Sensing (S) vs. Intuition (N)**")
        sn_df = calculate_percentage(scores['S'], scores['N'], 'Sensing', 'Intuition')
        st.bar_chart(sn_df, color="#93C47D")
        st.write("**Lifestyle: Judging (J) vs. Perceiving (P)**")
        jp_df = calculate_percentage(scores['J'], scores['P'], 'Judging', 'Perceiving')
        st.bar_chart(jp_df, color="#FFD966")

    st.markdown("---")

    # Famous Indian Personalities
    with st.expander("🇮🇳 Famous Indians Who Share Your Type!"):
        indian_personalities = famous_indians.get(result, ["No famous Indian personalities found for this type."])
        st.write("You're in good company! Here are some well-known Indians believed to share your personality type:")
        for person in indian_personalities:
            st.markdown(f"- **{person}**")

    # Compatibility Section
    with st.expander("💖 Find your compatible personality pals!"):
        compatible_types = compatibility_mapping.get(result, [])
        for comp_type, reason in compatible_types:
            st.subheader(f"🤝 The {comp_type}")
            st.write(f"**Their vibe:** {personality_descriptions[comp_type]}")
            st.write(f"**Why you might click:** {reason}")

    st.markdown("---")

    # Share Result Button
    share_text = f"I took the Personality AI quiz and my type is {result} - {personality_descriptions[result].split(':')[0]}! Find out yours here."
    components.html(f"""...""") # Share button code remains the same

    # Reset Button
    if st.button("Take the Quiz Again!"):
        # Reset the session state to go back to the start screen
        st.session_state.question_index = -1
        st.session_state.scores = {'I': 0, 'E': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
        st.session_state.answers = {}
        st.rerun()