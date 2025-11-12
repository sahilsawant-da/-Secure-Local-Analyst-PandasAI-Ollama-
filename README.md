# 🧠 Secure Local Analyst (PandasAI + Ollama)

A **self-contained, privacy-first AI data analysis system** that combines the power of **PandasAI**, **Streamlit**, and **Ollama** to perform **offline, natural-language statistical analysis** on structured and unstructured data.

---

## 🚀 Features

- 🔒 **100% Local Execution** — Your data never leaves your machine.
- 🧠 **LLM-Powered Analysis** using [Ollama](https://ollama.ai) (`llama3.2:3b`).
- 📂 **Multi-Format File Support** — Analyze CSV, XLSX, PDF, DOCX, TXT, and Parquet files.
- 🪶 **Auto-Fallback Sampling** for large datasets (ensures smooth performance).
- 📊 **Smart Visualization** powered by PandasAI & Streamlit.
- 🧾 **Unstructured Data Parsing** via the `unstructured` library.
- ⚙️ **Dynamic Error Handling** & **Context-Aware Analysis** for robust operation.

---

## 🏗️ Tech Stack

| Component | Purpose |
|------------|----------|
| **Streamlit** | Interactive and responsive data interface |
| **PandasAI** | Natural-language DataFrame analysis |
| **Ollama (Llama 3.2)** | Local LLM for secure, offline inference |
| **LangChain + Ollama** | Integration layer between LLM and data |
| **Unstructured** | Document text extraction (PDF/DOCX/TXT) |
| **Matplotlib / Pandas** | Statistical computing & visualization |

---

## 🖼️ UI Preview

<p align="center">
  <img src="screenshots/app_preview.png" alt="Biostatistics Analysis System UI" width="800" style="border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.2);">
</p>

<p align="center">
  <em>📊 A modern, privacy-first Biostatistics Analysis System built with Streamlit &amp; PandasAI.</em>
</p>

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sahilsawant-da/Secure-Local-Analyst-PandasAI-Ollama.git
cd Secure-Local-Analyst-PandasAI-Ollama
