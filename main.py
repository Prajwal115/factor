from fastapi import FastAPI, Form
from fastapi import UploadFile
from pathlib import Path
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import mysql.connector
import os
import re
import time

import google.generativeai as genai

import subprocess
import tempfile
import whisper

# Set your API key
genai.configure(api_key="API_KEY")

# Initialize Gemini threads for BP format
gemini_model = genai.GenerativeModel("gemini-2.0-flash")
opening_govt_thread = gemini_model.start_chat(history=[])
closing_govt_thread = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])
opening_opp_thread = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])
closing_opp_thread = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])
judge_thread = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])

onevsone_thread = genai.GenerativeModel("gemini-2.0-flash").start_chat(history=[])

ai_threads = {
    "opening govt": opening_govt_thread,
    "closing govt": closing_govt_thread,
    "opening opp": opening_opp_thread,
    "closing opp": closing_opp_thread
}

ai_threads_1v1 = {
    "debator 01": onevsone_thread,
    "debator 02": onevsone_thread
}

last_replies = {
    "opening govt": "",
    "opening opp": "",
    "closing govt": "",
    "closing opp": ""
}

app = FastAPI()

# Allow requests from browser (JS fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount current dir for static assets (JS/CSS if needed)
app.mount("/static", StaticFiles(directory="."), name="static")
app.mount("/CSS", StaticFiles(directory="CSS"), name="css")
app.mount("/IMG", StaticFiles(directory="IMG"), name="img")

# MySQL connection
conn = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    port=3306,  # MAMP default MySQL port
    user="sql12791599",
    password="PASSWORD",
    database="sql12791599"
)
cursor = conn.cursor()

# Serve index page
@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("index.html")

# Serve login page
@app.get("/login", response_class=FileResponse)
async def serve_login():
    return FileResponse("login.html")

# Handle login
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print("Login attempt:", username, password)
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username.strip().lower(), password))
    result = cursor.fetchone()
    if result:
        return RedirectResponse(url="/home", status_code=302)
    else:
        return JSONResponse({"success": False, "message": "Invalid credentials"})

# Serve register page
@app.get("/register", response_class=FileResponse)
async def serve_register():
    return FileResponse("register.html")

# Handle registration
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    print("Register attempt:", username, password)
    check_query = "SELECT * FROM users WHERE username=%s"
    cursor.execute(check_query, (username.strip().lower(),))
    if cursor.fetchone():
        return JSONResponse({"success": False, "message": "Username already exists"})

    insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (username.strip().lower(), password))
    conn.commit()

    # Sanitize the username for safe directory naming
    safe_username = re.sub(r'[^a-zA-Z0-9_\-]', '', username.strip().lower())

    # Create user directory structure
    base_path = os.path.join("users", safe_username)
    sessions_path = os.path.join(base_path, "sessions")
    notes_path = os.path.join(base_path, "notes")

    os.makedirs(sessions_path, exist_ok=True)
    os.makedirs(notes_path, exist_ok=True)

    return RedirectResponse(url="/home", status_code=302)

# Serve home page
@app.get("/home", response_class=FileResponse)
async def serve_home():
    return FileResponse("home.html")

# Serve logout page
@app.get("/logout", response_class=FileResponse)
async def serve_logout():
    return FileResponse("logout.html")

# Serve newsession page
@app.get("/newsession", response_class=FileResponse)
async def serve_newsession():
    return FileResponse("newsession.html")

# Serve pre_session page
@app.get("/pre_session", response_class=FileResponse)
async def serve_pre_session():
    return FileResponse("pre_session.html")

# Serve launch page
@app.get("/launch", response_class=FileResponse)
async def serve_launch():
    return FileResponse("launch.html")

# Serve session page
@app.get("/session", response_class=FileResponse)
async def serve_session():
    return FileResponse("session.html")

# Serve session_bp page
@app.get("/session_bp", response_class=FileResponse)
async def serve_session_bp():
    return FileResponse("session_bp.html")

# Serve session_ap page
@app.get("/session_ap", response_class=FileResponse)
async def serve_session_ap():
    return FileResponse("session_ap.html")

# Serve session_1v1 page
@app.get("/session_1v1", response_class=FileResponse)
async def serve_session_1v1():
    return FileResponse("session_1v1.html")

# Serve judge page
@app.get("/judge", response_class=FileResponse)
async def serve_judge():
    return FileResponse("judge.html")

# Serve pastsessions page
@app.get("/pastsessions", response_class=FileResponse)
async def serve_pastsessions():
    return FileResponse("pastsessions.html")

from fastapi import Request

# Handle session creation
@app.post("/session")
async def create_session(
    request: Request
):
    form = await request.form()
    username = form.get("username", "").strip().lower()
    session_title = form.get("session_title", "")
    format = form.get("format", "")

    print("Received session creation request:")
    print("Username:", username)
    print("Session Title:", session_title)
    print("Format:", format)

    if not username or not session_title or not format:
        print("Missing required fields")
        return JSONResponse({"success": False, "message": "Missing required fields"}, status_code=400)

    insert_query = "INSERT INTO sessions (username, session_title, format) VALUES (%s, %s, %s)"
    try:
        cursor.execute(insert_query, (username, session_title, format))
        conn.commit()
        print("Session inserted successfully into database.")
        session_id = cursor.lastrowid  # Get the inserted session ID
        print("Session ID:", session_id)
        
    except Exception as e:
        print("Insert error:", e)
        return JSONResponse({"success": False, "message": "DB insert failed"}, status_code=500)

    return RedirectResponse(url=f"/session?session_id={session_id}", status_code=302)



from fastapi import Request
from fastapi.responses import JSONResponse

@app.post("/start-session")
async def start_session(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    format = data.get("format", "bp").lower()

    if format == "1v1":
        prompt_1v1 = f"""
You are participating in a One vs One Debate.

🧠 Debate Topic: {topic}

🎭 Roles:
Debator 01: FOR the motion
Debator 02: AGAINST the motion

Respond only when your role is active.
"""
        onevsone_thread.send_message(prompt_1v1)

    else:
        base_prompt = lambda team: f"""
You are the {team.title()} team in a British Parliamentary debate.
You will speak as two speakers. Stay within your team’s ideological line.
Respond only when asked. The topic is:
"{topic}"
"""
        for team, thread in ai_threads.items():
            thread.send_message(base_prompt(team))


    return JSONResponse({"status": "session initialized"})


# Audio upload endpoint
from fastapi import Form

@app.post("/upload-audio")
async def upload_audio(
    audio: UploadFile,
    session_id: str = Form(...),
    username: str = Form(...),
    role: str = Form(...)
):
    # Create a session-specific directory under users/<username>/sessions/<session_id>
    safe_username = re.sub(r'[^a-zA-Z0-9_\-]', '', username.strip().lower())
    base_path = Path("users") / safe_username / "sessions" / session_id
    base_path.mkdir(parents=True, exist_ok=True)

    role_order = {
        "prime minister": "01",
        "leader of opposition": "02",
        "deputy prime minister": "03",
        "deputy leader of opposition": "04",
        "member of government": "05",
        "member of opposition": "06",
        "government whip": "07",
        "opposition whip": "08"
    }

    file_number = role_order.get(role.strip().lower(), "99")
    timestamp = int(time.time())
    file_path = base_path / f"{file_number}_{timestamp}.webm"

    with open(file_path, "wb") as f:
        content = await audio.read()
        f.write(content)

    # Convert webm to mp3 using ffmpeg
    mp3_path = str(file_path.with_suffix('.mp3'))
    subprocess.run([
        "ffmpeg", "-i", str(file_path), "-ar", "16000", "-ac", "1", mp3_path
    ], check=True)

    # Transcribe using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(mp3_path)
    transcript = result["text"].strip()

    return JSONResponse({"status": "success", "file": str(file_path), "transcript": transcript})

from pydantic import BaseModel

class GeminiPayload(BaseModel):
    transcript: str
    session_id: str
    username: str
    topic: str
    side: str
    speaker_team: str
    difficulty: str
    pep_talk: dict
    role: str

@app.post("/send-to-gemini")
async def send_to_gemini(payload: GeminiPayload):
    role_to_team = {
        "prime minister": "opening govt",
        "deputy prime minister": "opening govt",
        "member of government": "closing govt",
        "government whip": "closing govt",
        "leader of opposition": "opening opp",
        "deputy leader of opp.": "opening opp",
        "member of opp.": "closing opp",
        "opposition whip": "closing opp"
    }

    role = payload.role.strip().lower()
    # Detect format, fallback to "bp" if not present
    format = getattr(payload, "format", None)
    if not format:
        # Try to infer from speaker_team or role
        if role in ["debator 01", "debator 02"]:
            format = "1v1"
        else:
            format = "bp"
    else:
        format = format.strip().lower()

    # 1v1 role/format logic
    if role in ["debator 01", "debator 02"]:
        # Use exact match for role assignment
        current_team = "debator 01" if role == "debator 01" else "debator 02"
        thread = ai_threads_1v1[current_team]
        last_replies[current_team] = ""
        actual_role = current_team
    else:
        current_team = role_to_team.get(role, "opening opp")
        thread = ai_threads[current_team]

    # Get last Gemini reply if no new transcript provided (for AI-to-AI flow)
    if not payload.transcript.strip():
        transcript = last_replies.get(current_team, "")
        if transcript.strip() == last_replies.get(current_team, "").strip():
            print("Duplicate AI response attempt — skipping")
            return JSONResponse({"reply": "SKIPPED_DUPLICATE_AI"})
    else:
        transcript = payload.transcript.strip()

    # Build the full prompt, handle 1v1 separately
    if format == "1v1" or role in ["debator 01", "debator 02"]:
        full_prompt = f"""
You are responding as {payload.role.title()} in a One vs One Debate.

🧠 Debate Topic: {payload.topic}
📚 Difficulty: {payload.difficulty}
🧑 Speaker Identity: {payload.role}
📝 Pep Talk:

Avoid: {payload.pep_talk.get('avoid')}


🎤 Last Speaker Said:
\"\"\"
{transcript}
\"\"\"

Now generate a strong response for {payload.role.title()}. Give short and consice answers. Please don't use any special symbols like * in your conversation.
"""
    else:
        full_prompt = f"""
You are responding as the {current_team.title()} in a British Parliamentary Debate.

🧠 Debate Topic: {payload.topic}
📚 Difficulty: {payload.difficulty}
🗣️ Current Speaker Role: {payload.role}
🧑‍🤝‍🧑 Current Speaker Team: {payload.speaker_team}
🧑 Speaker Identity: {payload.role}

📝 Pep Talk:
Main Argument: {payload.pep_talk.get('main_argument')}
Key Points: {payload.pep_talk.get('key_points')}
Avoid: {payload.pep_talk.get('avoid')}
Other Notes: {payload.pep_talk.get('other')}

🎤 Last Speaker Said:
\"\"\"
{transcript}
\"\"\"

Now generate a strong and structured response based on your role. Please don't use any special symbols like * in your conversation.
"""

    gemini_response = thread.send_message(full_prompt)
    # Ensure correct role logging for 1v1
    # actual_role is already set above if 1v1, otherwise use payload.role
    if 'actual_role' not in locals():
        actual_role = payload.role.strip().lower()
    role_clean = actual_role.title()

    # Save conversation to debate.txt
    conversation_path = Path("users") / payload.username.strip().lower() / "sessions" / payload.session_id / "debate.txt"
    conversation_path.parent.mkdir(parents=True, exist_ok=True)
    with open(conversation_path, "a", encoding="utf-8") as f:
        role_upper = payload.role.strip().title()
        # Write for both BP and 1v1 formats
        if format == "1v1" or actual_role in ["debator 01", "debator 02"]:
            f.write(f"{actual_role.title()}: {transcript}\n")
            f.write(f"{actual_role.title()} (Gemini): {gemini_response.text}\n")
        else:
            f.write(f"\n{role_upper}: {transcript}\n")
            f.write(f"{role_upper}: {gemini_response.text}\n")

    # Store the last reply for this team for AI chaining
    last_replies[current_team] = gemini_response.text

    return {"reply": gemini_response.text}


from gtts import gTTS
app.mount("/users", StaticFiles(directory="users"), name="users")

@app.post("/text-to-speech")
async def text_to_speech(request: Request):
    data = await request.json()
    text = data.get("text", "")
    session_id = data.get("session_id", "temp")
    username = data.get("username", "unknown")

    # Insert text length validation
    if not text or len(text.strip()) < 20:
        print(f"Skipped TTS: too short → \"{text}\"")
        return JSONResponse({"error": "Text too short for TTS", "audio_path": None}, status_code=400)

    safe_username = re.sub(r'[^a-zA-Z0-9_\-]', '', username.strip().lower())
    audio_dir = Path("users") / safe_username / "sessions" / session_id
    audio_dir.mkdir(parents=True, exist_ok=True)

    import time
    from datetime import datetime

    # Create unique filename based on timestamp and role (if available)
    role = data.get("role", "reply").strip().lower().replace(" ", "_")
    timestamp = int(time.time())
    audio_filename = f"tts_reply_{role}_{timestamp}.mp3"
    audio_path = audio_dir / audio_filename

    try:
        tts = gTTS(text)
        tts.save(str(audio_path))
    except Exception as e:
        print(f"TTS generation failed: {e}")
        return JSONResponse({"error": "TTS failed", "audio_path": None}, status_code=500)

    return JSONResponse({"audio_path": f"users/{safe_username}/sessions/{session_id}/{audio_filename}"})


from pydantic import BaseModel

class TranscriptLog(BaseModel):
    role: str
    transcript: str
    session_id: str
    username: str

@app.post("/log-transcript")
async def log_transcript(data: TranscriptLog):
    folder = Path("users") / data.username.strip().lower() / "sessions" / data.session_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "debate.txt"
    
    role_title = data.role.strip().title()

    # Format-aware handling to avoid duplicate logging for 1v1 format
    # If role is Debator 01 or Debator 02, use single newline
    with open(path, "a", encoding="utf-8") as f:
        if role_title.lower() in ["debator 01", "debator 02"]:
            f.write(f"{role_title}: {data.transcript.strip()}\n")
        else:
            f.write(f"{role_title}: {data.transcript.strip()}\n\n")

    return {"status": "logged"}


# Debate evaluation endpoint
class JudgeRequest(BaseModel):
    username: str
    session_id: str
    topic: str
    difficulty: str

@app.post("/evaluate-debate")
async def evaluate_debate(data: JudgeRequest):
    debate_file = Path("users") / data.username.strip().lower() / "sessions" / data.session_id / "debate.txt"
    if not debate_file.exists():
        return JSONResponse({"error": "Transcript not found"}, status_code=404)

    with open(debate_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Determine debate format
    if "debator 01" in transcript.lower() or "debator 02" in transcript.lower():
        evaluation_prompt = f"""
You are the Judge in a One vs One Debate.

🧠 Debate Topic: {data.topic}
📚 Difficulty: {data.difficulty}

📝 Transcript of Debate:
\"\"\"
{transcript}
\"\"\"

🎯 Your Task:
Evaluate the debate between Debator 01 (FOR) and Debator 02 (AGAINST). Provide individual scores out of 100 for each speaker. Then summarize who performed better and why in 3 lines using judging criteria like clarity, rebuttal strength, and persuasiveness.
Be straightforward and direct.
"""
    else:
        evaluation_prompt = f"""
You are the Judge in a British Parliamentary Debate.

🧠 Debate Topic: {data.topic}
📚 Difficulty: {data.difficulty}

📝 Transcript of Debate:
\"\"\"
{transcript}
\"\"\"

🎯 Your Task:
Evaluate each pair of duels (PM vs LO, DPM vs DLO, MG vs MO, GW vs OW). Provide a brief score (out of 100) for each speaker with reasoning. Then at the end, summarize your decision in 3 lines, stating which side/team won and why, using judging criteria like clarity, impact, rebuttal strength, and structure.

Return the entire evaluation as a readable paragraph.
"""

    response = judge_thread.send_message(evaluation_prompt)
    return {"evaluation": response.text}



@app.post("/check-sessions")
async def check_sessions(request: Request):
    data = await request.json()
    username = data.get("username", "").strip().lower()
    if not username:
        return JSONResponse({"exists": False})

    user_path = Path("users") / username / "sessions"
    if not user_path.exists() or not any(user_path.iterdir()):
        return JSONResponse({"exists": False})

    return JSONResponse({"exists": True})


# List all sessions for a user
@app.get("/list-sessions")
async def list_sessions(username: str):
    username = username.strip().lower()
    sessions_path = Path("users") / username / "sessions"
    if not sessions_path.exists():
        return JSONResponse([])

    cursor.execute("SELECT session_id, session_title, created_at, format FROM sessions WHERE username = %s", (username,))
    rows = cursor.fetchall()

    result = []
    for session_id, session_title, created_at, format in rows:
        folder = sessions_path / str(session_id)
        if folder.exists():
            result.append({
                "session_id": str(session_id),
                "session_title": session_title,
                "format": format,
                "created_at": str(created_at)
            })

    return JSONResponse(result)


# Get transcript for a specific session
@app.get("/transcript")
async def get_transcript(username: str, session_id: str):
    username = username.strip().lower()

    if not username or not session_id:
        return JSONResponse({"error": "Missing username or session_id"}, status_code=400)

    transcript_path = f"users/{username}/sessions/{session_id}/debate.txt"

    format_path = f"users/{username}/sessions/{session_id}/meta.txt"

    if not os.path.exists(transcript_path):
        return JSONResponse({"error": "Transcript not found"}, status_code=404)

    with open(transcript_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try to get the format (optional)
    format = ""
    if os.path.exists(format_path):
        with open(format_path, 'r') as f:
            format = f.read().strip()

    return JSONResponse({
        "format": format,
        "transcript": content
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
