# 🧠 Secure Local Analyst (PandasAI + Ollama)

A **self-contained, privacy-first AI data analysis system** that combines the power of **PandasAI**, **Streamlit**, and **Ollama** to perform **offline natural-language statistical analysis** on structured and unstructured data.

---

## 🚀 Features

- 🔒 **100% Local Execution** — No cloud data transfer.  
- 🧠 **LLM-Powered Analysis** using [Ollama](https://ollama.ai) (`llama3.2:3b`).  
- 📂 **Multi-Format File Support** — CSV, XLSX, PDF, DOCX, TXT, Parquet, and more.  
- 🪶 **Auto-Fallback Sampling** for large datasets.  
- 📊 **Smart Visualization** using PandasAI & Streamlit.  
- 🧾 **Unstructured Data Parsing** via the `unstructured` library.  
- ⚙️ **Dynamic Error Handling** & **context-aware analysis**.

---

## 🏗️ Tech Stack

| Component | Purpose |
|------------|----------|
| **Streamlit** | Interactive data-driven interface |
| **PandasAI** | Natural-language DataFrame analysis |
| **Ollama (Llama 3.2)** | Local LLM inference |
| **LangChain Ollama** | LLM interface layer |
| **Unstructured** | Document parsing (PDF/DOCX/TXT) |
| **Matplotlib / Pandas** | Core analytics and visualization |

---

## 🖼️ UI Preview

![App Screenshot](screenshots/app_preview.png)

---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/secure-local-analyst.git
cd secure-local-analyst
