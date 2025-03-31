
# Eddie-Core

**Eddie** is a modular, local-first AI personal assistant built for flexibility, privacy, and power. Designed to run seamlessly across devices, it routes requests through local models by default, using cloud LLMs only when necessary.

---

## 🚀 Features

- 🧠 Local-first LLM routing (quantized, GPU, or cloud fallback)
- 🔐 Secure user authentication (JWT + roles)
- ⚙️ Modular architecture for intent detection, memory, vector DB, and more
- 📡 FastAPI backend with role-based access
- 🧑‍💻 CLI for user management
- 🧠 Uses `llama-cpp` for local inference

---

## 🧱 Architecture Overview

```
eddie-core/
├── api_module/         # FastAPI app and routes
├── auth_module/        # JWT auth, bcrypt, user DB
├── core_logic/         # Intent handling, model routing
├── models/             # GGUF model files (e.g. TinyLLaMA)
├── run.py              # Dev entry point
├── service.py          # Production entry point
├── requirements.txt
└── eddie_core_summary.txt
```

---

## 🌐 API Endpoints

| Method | Path              | Description                         |
|--------|-------------------|-------------------------------------|
| POST   | `/api/v1/token`   | Get JWT access token                |
| GET    | `/api/v1/me`      | Info about current user/token       |
| POST   | `/api/v1/process` | Process user input with routed LLM  |

---

## 🧠 Model Routing via LLaMA (llm_router)

Uses a quantized LLaMA model via `llama-cpp-python` to classify the complexity of a user input and decide:

- `QUANTIZED_LLAMA`: For simple/yes-no/local stuff
- `LLAMA_GPU`: General-purpose responses
- `CLOUD_GPT`: Advanced logic, math, or creativity

Prompt is **dynamically generated** based on available models.

---

## 🔐 Auth & Roles

- Admin users can:
  - Use debug mode
  - Override model selection
- Regular users receive filtered responses
- Users stored in `auth_module/eddie_users.db`
- CLI supports:
  - `--init-db`
  - `--add-user`
  - `--remove-user`

---

## 🧪 Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run in dev mode
python run.py

# Run in production
python service.py
```

---

## 📅 Planned Modules

- `eddie-ui`: ChatGPT-style web frontend
- `eddie-voice`: Use Alexa devices as clients
- `eddie-store`: Vector DB, memory + data management

---

Built for privacy. Designed for power
