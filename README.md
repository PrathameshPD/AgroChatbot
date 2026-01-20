# 🌾 AgroChatbot: AI-Powered Agricultural Assistant Chatbot

AgroChatbot is an advanced AI assistant designed to help farmers and agricultural researchers with crop management, disease diagnosis, and data-driven decision-making. Built using a Retrieval-Augmented Generation (RAG) architecture, it leverages specialized knowledge on rice crops to provide accurate and actionable advice.

---

## 🚀 Key Features

- **🤖 AI Agentic Chat**: Interact with a sophisticated AI agent that understands context and retrieves relevant information from a curated knowledge base.
- **📚 Rice Crop Expertise**: Specialized support for rice varieties, disease identification, and management practices (based on scientific data).
- **📊 Automated Report Generation**: Generate detailed PDF reports for specific locations and years, summarizing soil health and crop yields.
- **✨ Modern UI/UX**: A responsive, premium interface built with React, featuring smooth animations and a dark-themed aesthetic.
- **🔍 RAG Architecture**: Uses Supabase Vector Store and Google Gemini for high-quality, data-backed responses.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: [React](https://reactjs.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Icons**: [Lucide React](https://lucide.dev/)

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Orchestration**: [LangChain](https://www.langchain.com/)
- **LLM**: [Google Gemini (Flash-1.5)](https://ai.google.dev/)
- **Database**: [Supabase](https://supabase.com/) (Vector Store & PostgreSQL)

---

## 📁 Project Structure

```bash
AgroChatbot/
├── backend/            # FastAPI application & RAG logic
│   ├── agentic_rag.py  # Core AI agent & tools
│   ├── ingest_in_db.py # Script to process data into Supabase
│   └── main.py         # API endpoints
├── frontend/           # React frontend application
├── Data/               # Raw datasets (PDFs, Excel)
├── requirements.txt    # Python dependencies
└── run_app.bat         # Batch script to run both apps
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js & npm
- [Supabase](https://supabase.com/) project (with `pgvector` enabled)
- [Google AI Studio](https://aistudio.google.com/) API Key

### 1. Clone the Repository
```bash
git clone https://github.com/PrathameshPD/AgroChatbot.git
cd AgroChatbot
```

### 2. Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Environment Variables:
   Create a `.env` file in the `backend/` directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_SERVICE_KEY=your_supabase_key
   GOOGLE_API_KEY=your_google_gemini_key
   API_BASE_URL=http://127.0.0.1:8000
   ```

### 3. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   ```

---

## 🏃 Running the Application

### Option A: Using the Batch Script (Windows)
Simply run the included batch script from the root directory:
```bash
./run_app.bat
```

### Option B: Manual Start
**Start Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Start Frontend:**
```bash
cd frontend
npm start
```

---

## 🛠️ Data Ingestion
To populate the vector database with your documents, run the ingestion script:
```bash
cd backend
python ingest_in_db.py
```
*Make sure your documents (PDF/Excel) are placed in the `backend/documents/` folder.*

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
