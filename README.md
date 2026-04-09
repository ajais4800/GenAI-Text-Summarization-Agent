# 🧠 GenAI Text Summarization Agent

## 🚀 Overview

This project is a **multi-agent AI text summarization system** built as part of the **Google GenAI Academy APAC 2026**.

It uses a **sequential agent pipeline** to:

1. Generate a draft summary
2. Refine it using a quality-checking agent

The system is designed using **Google ADK (Agent Development Kit)** and deployed on **Google Cloud Run** with secure authentication via service accounts.

---

## 🛠️ Tech Stack

* Python
* Google ADK (Agent Framework)
* Gemini Models (`gemini-2.5-flash`)
* Google Cloud Run (Deployment)
* IAM Service Account Authentication

---

## ⚙️ Architecture

### 🔹 Agent Workflow

```
User Input → Root Agent → Summarizer Agent → Quality Checker Agent → Final Output
```

* **Root Agent**

  * Handles user interaction
  * Stores input using tool

* **Summarizer Agent**

  * Generates concise summary

* **Quality Checker Agent**

  * Refines and formats output

* **SequentialAgent**

  * Orchestrates multi-step workflow

---

## 📂 Project Structure

```
.
├── agent.py              # Main agent pipeline
├── requirements.txt     # Dependencies
├── .env                 # Local config (NOT pushed to GitHub)
├── .gitignore
```

---

## 🔐 Authentication (IMPORTANT)

This project uses **Google Cloud Service Account authentication** instead of API keys.

### In Cloud Run:

* Authentication is handled automatically via:

  * Attached **Service Account**
  * IAM roles & permissions

### Required IAM Role:

* Vertex AI User / Generative AI access

---

## ⚙️ Environment Variables

Used for configuration (non-sensitive):

```
PROJECT_ID=your_project_id
MODEL=gemini-2.5-flash
```

> ⚠️ Do NOT store secrets in `.env` when using Cloud Run.

---

## ▶️ Running Locally

### 1. Create virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Authenticate with Google Cloud

```
gcloud auth application-default login
```

### 4. Run the agent

```
python agent.py
```

---

## ☁️ Deployment

Deployed using **Google Cloud Run**:

* Containerized application
* Serverless execution
* Scalable architecture

---

## ✨ Features

* Multi-agent pipeline (Agentic AI)
* State sharing between agents
* Clean and structured output
* Cloud-native deployment

---

## 📌 Future Improvements

* Add FastAPI endpoint for external access
* Add UI (Streamlit / React)
* Integrate RAG (Retrieval-Augmented Generation)
* Support document uploads (PDF, DOCX)

---

## 👨‍💻 Author

Ajai S
