# 💬 Chat Frontend (Streamlit)

This is the **frontend UI** for the Chat App, built with **Streamlit**.  
It connects to the **FastAPI backend** for authentication, chatting with personas, history management, and analytics.

🌐 Live App → [https://chat-frontend-f2hs.streamlit.app/](https://chat-frontend-f2hs.streamlit.app/)

---

## 🚀 Features

- **Authentication**
  - Login with email/password
  - JWT-based secure API calls

- **Chat System**
  - Multiple personas (Default, Tutor, Therapist)
  - Adjustable temperature slider
  - Clean bubble-based UI
  - History persistence per persona
  - Option to download chat history (per persona)

- **Analytics**
  - View number of chats
  - Most used persona
  - Top prompts (charts & table)

- **Deployment**
  - Hosted on **Streamlit Cloud**
  - Connects to backend (Railway/Render)

---

## 📂 Project Structure

```
CHAT-FRONTEND/
│── .devcontainer/            # Dev container settings (VS Code Remote Containers)
│
│── .streamlit/               # Streamlit configuration
│   ├── config.toml           # Streamlit UI & theme settings
│   └── secrets.toml          # API keys / secrets (not in Git)
│
│── .venv/                    # Python virtual environment (ignored in Git)
│── .vscode/                  # VS Code workspace configs
│
│── streamlit_app/            # Auto-generated cache from Streamlit
│   └── __pycache__/          # Compiled Python bytecode
│
│── core/                     # Core application logic
│   ├── __init__.py
│   ├── api.py                # Handles requests to backend API
│   ├── config.py             # Global configs (API base URL, personas)
│   └── state.py              # Session state management
│
│── ui/                       # UI rendering components/pages
│   ├── __init__.py
│   ├── analytics_page.py     # Analytics dashboard page
│   ├── auth.py               # Login & authentication UI
│   ├── chat_page.py          # Chat interface (bubbles, messages)
│   ├── components.py         # Reusable UI components
│   └── sidebar.py            # Sidebar navigation / persona switcher
│
│── app.py                    # Main entry point for Streamlit app
│── .env                      # Environment variables (backend URL etc.)
│── .gitignore                # Ignored files for Git
│── Dockerfile                # Containerization for frontend
│── README.md                 # Documentation
│── requirements.txt          # Python dependencies

```

---

## 🛠️ Installation & Running Locally

### 1. Clone repository

```bash
git clone https://github.com/yourusername/chat-frontend.git
cd chat-frontend
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run Streamlit app

```bash
streamlit run app.py
```

Now visit 👉 [http://localhost:8501](http://localhost:8501)

---

## 🔑 Configuration

The app reads configuration from **Streamlit secrets** or environment variables.

Example `.streamlit/secrets.toml`:

```toml
API_BASE_URL = "https://chat-backend-production-bbdf.up.railway.app/api/v1"
PERSONAS = "Default,Tutor,Therapist"
DEFAULT_PERSONA = "Default"
DEFAULT_TEMPERATURE = 0.7
```

---

## 🔐 Authentication

* Login with test credentials (from backend):

```txt
Email: test@example.com
Password: password123
```

---

## 💬 Chat Flow

1. Choose persona in sidebar  
2. Adjust temperature (creativity)  
3. Start chatting!  
4. History is stored per persona  
5. Download chat history anytime  

---

## 📊 Analytics Dashboard

Accessible via sidebar → **Analytics**:

- Total chats  
- Most used persona  
- Top prompts (charts + table)

---

## ☁️ Deployment

### Streamlit Cloud

1. Push repo to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Create new app → Connect your GitHub repo
4. Set secrets (`API_BASE_URL`, `PERSONAS`, etc.)
5. Deploy 🎉

---

## ✅ Tech Stack

- [Streamlit](https://streamlit.io) → UI
- [FastAPI Backend](https://fastapi.tiangolo.com) → API
- [Railway/Render](https://railway.app / https://render.com) → Backend hosting
- [Streamlit Cloud](https://streamlit.io/cloud) → Frontend hosting

---

## 📌 Notes

- Requires backend to be deployed & accessible
- If API returns 401, re-check backend URL & login credentials
- Default personas:  
  * **Default** → Helpful assistant  
  * **Tutor** → Step-by-step explanations  
  * **Therapist** → Empathetic, supportive coach  
