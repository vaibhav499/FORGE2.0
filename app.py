import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv
from google import genai

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Forge 2.0", layout="wide")

# ---------------------------
# UI STYLE
# ---------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #121212, #0F172A);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* Hide default */
#MainMenu, footer {
    visibility: hidden;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: 0.3s;
    text-align: center;
}

.glass:hover {
    transform: translateY(-5px);
}

/* Button */
.stButton>button {
    background: #FFCE1B;
    color: black;
    border-radius: 25px;
    height: 45px;
    width: 100%;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFCE1B;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD ENV
# ---------------------------
load_dotenv()
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
# ---------------------------
# DATABASE
# ---------------------------
def connect_db():
    return sqlite3.connect("forge.db", check_same_thread=False)

conn = connect_db()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS profile (
    user_id INTEGER,
    age INTEGER,
    height REAL,
    weight REAL,
    goal TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER,
    date TEXT,
    weight REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    exercise TEXT,
    sets INTEGER,
    reps INTEGER,
    weight REAL
)
""")

conn.commit()

# ---------------------------
# HASH PASSWORD
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- AI DIET ----------------
def generate_ai_diet(profile):
    prompt = f"""
    You are a professional Indian nutritionist.

    Create a detailed Indian diet plan for:
    Age: {profile['age']}
    Weight: {profile['weight']} kg
    Height: {profile['height']} cm
    Goal: {profile['goal']}
    Diet Type: {profile['diet']}

    Include:
    - Breakfast
    - Lunch
    - Dinner
    - Snacks
    - Calories (approx)
    """

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)
    return response.text
# ---------------------------
# SESSION
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------------------
# AUTH
# ---------------------------
def signup():
    st.subheader("📝 Create Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hash_password(password))
            )
            conn.commit()
            st.success("Account created!")
        except:
            st.error("Email already exists!")

def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, hash_password(password))
        )
        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.rerun()
        else:
            st.error("Invalid credentials")
# ---------------------------
# MAIN APP
# ---------------------------
def main_app():

    # ---------------- SIDEBAR ----------------
    st.sidebar.markdown("""
    <div style="
        padding: 20px;
        border-radius: 20px;
        background: rgba(0,0,0,0.15);
        backdrop-filter: blur(12px);
        text-align: center;
        margin-bottom: 10px;
    ">
        <h2 style="margin-bottom:5px;">🔥 FORGE 2.0</h2>
        <p style="font-size:14px;">Train Like a Beast 💪</p>
    </div>
    """, unsafe_allow_html=True)

    menu = st.sidebar.radio(
        "",
        [
            "🏠 Dashboard",
            "👤 Profile",
            "🏋️ Workout",
            "📊 History",
            "📈 Weight Graph",
            "🤖 AI Diet",
            "🚪 Logout"
        ]
    )

    # ---------------- DASHBOARD ----------------
    if menu == "🏠 Dashboard":

        cursor.execute("SELECT name FROM users WHERE id=?",
                       (st.session_state.user_id,))
        user_name = cursor.fetchone()[0]

        st.markdown(f"""
        <div class="glass">
            <h1>🔥 Welcome {user_name}</h1>
            <p>Stay consistent. Your progress matters 💪</p>
        </div>
        """, unsafe_allow_html=True)

        cursor.execute(
            "SELECT age, height, weight, goal FROM profile WHERE user_id=?",
            (st.session_state.user_id,)
        )
        profile = cursor.fetchone()

        if profile:
            age, height, weight, goal = profile

            height_m = height / 100
            bmi = weight / (height_m ** 2)
            calories = 2000

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"<div class='glass'><h3>Weight</h3><h2>{weight} kg</h2></div>", unsafe_allow_html=True)

            with col2:
                st.markdown(f"<div class='glass'><h3>BMI</h3><h2>{round(bmi,2)}</h2></div>", unsafe_allow_html=True)

            with col3:
                st.markdown(f"<div class='glass'><h3>Goal</h3><h2>{goal}</h2></div>", unsafe_allow_html=True)

            with col4:
                st.markdown(f"<div class='glass'><h3>Calories</h3><h2>{calories}</h2></div>", unsafe_allow_html=True)

        else:
            st.warning("Complete profile first")

    # ---------------- PROFILE ----------------
    elif menu == "👤 Profile":
        st.title("Profile")

        age = st.number_input("Age", 15, 60)
        height = st.number_input("Height")
        weight = st.number_input("Weight")
        goal = st.selectbox("Goal", ["Fat Loss", "Muscle Gain", "Maintenance"])

        if st.button("Save"):
            cursor.execute("DELETE FROM profile WHERE user_id=?", (st.session_state.user_id,))
            cursor.execute(
                "INSERT INTO profile VALUES (?, ?, ?, ?, ?)",
                (st.session_state.user_id, age, height, weight, goal)
            )
            conn.commit()
            st.success("Saved!")

    # ---------------- WORKOUT ----------------
    elif menu == "🏋️ Workout":
        st.title("Workout")

        ex = st.text_input("Exercise")
        sets = st.number_input("Sets", 1)
        reps = st.number_input("Reps", 1)

        if st.button("Save"):
            cursor.execute(
                "INSERT INTO workouts (user_id, date, exercise, sets, reps, weight) VALUES (?, ?, ?, ?, ?, ?)",
                (st.session_state.user_id, str(datetime.now()), ex, sets, reps, 0)
            )
            conn.commit()
            st.success("Saved")

    # ---------------- HISTORY ----------------
    elif menu == "📊 History":
        st.title("Workout History")

        cursor.execute(
            "SELECT * FROM workouts WHERE user_id=?",
            (st.session_state.user_id,)
        )
        data = cursor.fetchall()

        for row in data:
            st.write(row)

    # ---------------- WEIGHT GRAPH ----------------
    elif menu == "📈 Weight Graph":
        st.title("Progress")

        w = st.number_input("Weight")

        if st.button("Add"):
            cursor.execute(
                "INSERT INTO progress VALUES (?, ?, ?)",
                (st.session_state.user_id, str(datetime.now()), w)
            )
            conn.commit()

        cursor.execute(
            "SELECT weight FROM progress WHERE user_id=?",
            (st.session_state.user_id,)
        )
        data = [i[0] for i in cursor.fetchall()]

        if data:
            st.line_chart(data)

    
        # ---------------- AI DIET ----------------
    elif menu == "🤖 AI Diet":
        st.title("AI Diet")

        cursor.execute(
            "SELECT age, height, weight, goal FROM profile WHERE user_id=?",
            (st.session_state.user_id,)
        )
        data = cursor.fetchone()

        if not data:
            st.warning("⚠️ Please complete your profile first")
        else:
            age, height, weight, goal = data

            diet_type = st.selectbox(
                "Diet Type",
                ["Vegetarian", "Non-Vegetarian", "Vegan"]
            )

            if st.button("Generate Diet Plan"):

                profile = {
                    "age": age,
                    "height": height,
                    "weight": weight,
                    "goal": goal,
                    "diet": diet_type
                }

                with st.spinner("Generating your AI diet plan..."):
                    try:
                        result = generate_ai_diet(profile)
                        st.success("✅ Your Diet Plan")
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"Error: {e}")

    # ---------------- LOGOUT ----------------
    elif menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.rerun()

# ---------------------------
# FLOW
# ---------------------------
if not st.session_state.logged_in:
    opt = st.radio("Select", ["Login", "Signup"])
    if opt == "Login":
        login()
    else:
        signup()
else:
    main_app()