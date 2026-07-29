# 🎓 SchoolAssist AI

> AI-powered School Analytics & Intelligent Assistant for K-12 Schools

SchoolAssist AI is an intelligent school management platform that combines
analytics, dashboards, Retrieval-Augmented Generation (RAG), and Large Language Models
to help schools automate communication, monitor performance, and make better decisions.

---

## ✨ Key Features

### 🤖 AI Assistant
- Answer parent queries instantly
- School policy search
- Admission guidance
- Homework lookup
- Circular search
- Intelligent FAQ

### 📊 Analytics Dashboard *(In Progress)*
- Student Performance Dashboard
- Attendance Analytics
- Fee Collection Dashboard
- Teacher Performance
- School KPI Dashboard
- AI-generated Insights

### 📚 Knowledge Base
- PDF ingestion
- School circular indexing
- Vector search using FAISS
- Semantic search

### 📄 Report Generation
- Parent meeting summary
- Student report comments
- Attendance reports
- AI-generated recommendations

---

## 🏗 Architecture

```
                +----------------------+
                |      Web Client      |
                +----------+-----------+
                           |
                           v
                  FastAPI Backend
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
   FAISS Vector DB                     SQLite Database
        |                                     |
        +------------------+------------------+
                           |
                           v
                      OpenAI / Ollama
                           |
                           v
                      AI Response
```

---

## 🛠 Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | Next.js (Planned) |
| Backend | FastAPI |
| Database | SQLite |
| Vector Store | FAISS |
| AI | OpenAI GPT |
| Language | Python |
| Deployment | Docker |

---

## 📁 Project Structure

```
Schoolassist-ai/

backend/

frontend/

data/

docs/

screenshots/

architecture/

requirements.txt

README.md
```

---

## 🚀 Roadmap

- [x] FastAPI backend
- [x] RAG pipeline
- [x] PDF ingestion
- [x] OpenAI integration
- [ ] School Analytics Dashboard
- [ ] Student Management
- [ ] Attendance Dashboard
- [ ] Fee Analytics
- [ ] Teacher Dashboard
- [ ] AI Report Generation
- [ ] Role-based Authentication
- [ ] Docker Deployment

---

## 📸 Screenshots

Coming Soon

---

## ⚡ Future Enhancements

- Multi-school support
- Mobile application
- Voice Assistant
- WhatsApp integration
- Parent Portal
- Teacher Portal
- Predictive Analytics
- AI Attendance Insights

---

## 👨‍💻 Author

Praveenkumar

IT Consultant | Data Analytics | AI Applications

Building intelligent software using Python, FastAPI, SQL, Power BI and Generative AI.
