# CareNova — Backend

## 📋 Overview

This is the **backend** for CareNova — an empathetic AI healthcare chatbot. It uses a **RAG (Retrieval-Augmented Generation)** pipeline to provide preliminary health guidance based on user-reported symptoms.

> ⚠️ This is the **backend only**. You must also run the [CareNova Frontend](https://github.com/esha1104/frontend-carenova) to use the full application.

---

## 🏗️ System Architecture

```
User Symptoms
      ↓
Follow-up Questions (adaptive_questions.py + Llama 3.2)
      ↓
RAG Pipeline (rag.py)
  ├── Embed query (nomic-embed-text)
  ├── Search ChromaDB vector store
  └── Retrieve relevant medical documents
      ↓
LLM Response Generation (Llama 3.2 via Ollama)
      ↓
Structured JSON Response
  ├── Possible conditions
  ├── Explanation
  ├── Home care tips
  ├── When to see a doctor
  └── Disclaimer
```

---

## 🗂️ File Structure

```
CHATBOT_LLM/
├── main.py                    # FastAPI entry point
├── rag.py                     # RAG pipeline
├── llm.py                     # Ollama LLM setup
├── chatbot.py                 # Analysis logic
├── adaptive_questions.py      # Follow-up question generation
├── ingest.py                  # Build ChromaDB vector store
├── prompts.py                 # System prompts
├── app.py                     # Streamlit app (alternative UI)
├── routes/
│   ├── auth.py                # Firebase token verification
│   ├── chat.py                # Chat endpoint (/api/chat/message)
│   ├── followup.py            # Follow-up questions (/api/followup/questions)
│   └── __init__.py
├── medical_knowledge/         # Medical documents (markdown files)
│   ├── cardiovascular/
│   ├── respiratory/
│   ├── infectious/
│   ├── neurological/
│   ├── metabolic/
│   ├── gastrointestinal/
│   └── immune/
├── chroma_db/                 # Vector database (auto-generated)
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Prerequisites

- [ ] Python 3.10 or higher
- [ ] [Ollama](https://ollama.com) installed
- [ ] At least 4GB RAM (for Llama 3.2)

---

## 🚀 Setup & Installation

### Step 1 — Clone this repository
```bash
git clone https://github.com/esha1104/backend-carenova.git
cd backend-carenova
```

### Step 2 — Create and activate virtual environment
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Pull required Ollama models
```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

### Step 5 — Build the vector database (run once)
```bash
python ingest.py
```
You should see:
```
✅ Vector database created successfully!
```

---

## ▶️ Running the Backend

You need **two terminals** running simultaneously:

**Terminal 1 — Start Ollama:**
```bash
ollama serve
```

**Terminal 2 — Start FastAPI (inside venv):**
```bash
uvicorn main:app --reload --port 8000
```

You should see:
```
✅ Uvicorn running on http://127.0.0.1:8000
✅ Application startup complete.
```

Verify it's working by opening: `http://127.0.0.1:8000/docs`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check |
| `POST` | `/api/auth/verify-token` | Verify Firebase ID token |
| `POST` | `/api/followup/questions` | Get 3 follow-up questions for symptoms |
| `POST` | `/api/chat/message` | Run RAG analysis and get health guidance |
| `GET`  | `/api/chat/health` | Chat service health check |

### Example request — `/api/chat/message`
```json
{
  "message": "fever, headache, fatigue | 3 days | getting worse | yes",
  "conversation_history": []
}
```

### Example response
```json
{
  "possible_conditions": ["Influenza", "COVID-19"],
  "explanation": ["Fever and fatigue together with worsening symptoms suggest viral infection"],
  "home_care_tips": ["Rest", "Stay hydrated", "Take paracetamol for fever"],
  "when_to_see_doctor": ["If fever exceeds 103°F", "If breathing becomes difficult"],
  "disclaimer": "This is not a medical diagnosis. Consult a healthcare professional."
}
```

---

## 🔐 Authentication

CareNova uses **Firebase Authentication** with magic links.

For **production**: Place your `firebase_service_account.json` in the root folder.

For **testing/demo**: The backend automatically runs in demo mode if the service account file is not found. Demo tokens starting with `demo_token_` are accepted without Firebase verification.

---

## 🧠 Medical Knowledge Base

The `medical_knowledge/` folder contains markdown files organized by category:

| Category | Diseases Covered |
|----------|-----------------|
| Respiratory | Asthma, Pneumonia, Bronchitis, COPD |
| Infectious | Influenza, COVID-19, Dengue, Malaria |
| Cardiovascular | Hypertension, Heart Disease |
| Neurological | Migraine, Epilepsy |
| Metabolic | Diabetes, Thyroid disorders |
| Gastrointestinal | GERD, IBS, Food poisoning |
| Immune | Allergies, Autoimmune conditions |

To add new diseases, create a `.md` file in the relevant folder and re-run `python ingest.py`.

---

## 🤝 Related Repositories

- 🔗 **Frontend**: [frontend-carenova](https://github.com/esha1104/frontend-carenova)

---

## ⚕️ Disclaimer

CareNova provides **preliminary guidance only** and is **not a substitute** for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

