import streamlit as st
import pandas as pd
import tempfile
import os
from io import BytesIO, StringIO
import csv
import warnings

from pandasai import SmartDataframe
# Import context explicitly for clarity, though ResponseParser already handles it
from pandasai.responses.response_parser import ResponseParser 

# ⚡ LLM Setup
from langchain_ollama import OllamaLLM as Ollama 
from unstructured.partition.auto import partition 

# --- WARNING SUPPRESSION (For a clean Streamlit UI) ---
warnings.filterwarnings(
    "ignore", 
    category=FutureWarning, 
    module='pandas'
) 
warnings.filterwarnings(
    "ignore", 
    category=DeprecationWarning, 
    module='langchain'
) 

# --- Configuration ---
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_HOST = "http://127.0.0.1:11435"
MAX_IN_MEMORY_SIZE = 50 * 1024 * 1024 # 50 MB limit for full in-memory load
LLM_SAMPLING_RATE = 0.05 

st.set_page_config(layout="wide", page_title="Secure Multi-Format Local Data Analyst")

# --- Custom Response Parser (FIXED - Handles Streamlit Output) ---
class StreamlitResponse(ResponseParser):
    # 💡 CRITICAL FIX: Correctly accept 'context' and 'kwargs' passed by PandasAI
    def __init__(self, context, **kwargs): 
        super().__init__(context, **kwargs)
    
    # Ensures plots are handled by st.pyplot
    def format_plot(self, result):
        st.pyplot(result)
        return "Plot successfully generated and displayed above."

    # Ensures DataFrames are handled by st.dataframe
    def format_dataframe(self, result):
        st.subheader("Generated DataFrame/Table")
        st.dataframe(result, use_container_width=True)
        return "Resulting DataFrame is displayed above."
        
    # Handles the final textual or numerical answer
    def format_json(self, result):
        if 'answer' in result and result['answer']:
            # The LLM's final text answer
            return result['answer']
        elif 'value' in result:
             # If the LLM returned a number, format it nicely
            if isinstance(result['value'], (int, float)):
                return f"The calculated result is: {result['value']:,}"
            # If the LLM returned a dataframe object (should be caught by format_dataframe but as a fallback)
            elif isinstance(result['value'], pd.DataFrame):
                 st.dataframe(result['value'], use_container_width=True)
                 return "Resulting DataFrame is displayed above."
        
        return "Analysis code executed successfully, but a definitive final answer was not parsed."

# --- Global State Initialization ---
if 'llm' not in st.session_state:
    try:
        st.session_state.llm = Ollama(
            model=OLLAMA_MODEL, 
            base_url=OLLAMA_HOST, 
            temperature=0.3, 
            mirostat=0,       
            num_ctx=2048,     
            num_gpu=99
        )
        st.session_state.llm_connected = True
    except Exception:
        st.session_state.llm = None
        st.session_state.llm_connected = False

# --- Helper Function for Robust Multi-Format Loading ---

@st.cache_data(show_spinner="Loading and preparing file...")
def load_and_process_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    file_bytes = uploaded_file.getvalue()
    file_size_bytes = len(file_bytes)
    is_large_file = file_size_bytes > MAX_IN_MEMORY_SIZE
    
    if ext in ['.csv', '.xlsx', '.xls', '.parquet']:
        try:
            if ext == '.csv':
                data_string = StringIO(file_bytes.decode('utf-8'))
                dialect = csv.Sniffer().sniff(data_string.read(1024))
                data_string.seek(0)
                df = pd.read_csv(data_string, sep=dialect.delimiter)
                
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(BytesIO(file_bytes))
            elif ext == '.parquet':
                df = pd.read_parquet(BytesIO(file_bytes))
            
            # FIX: Force Numeric Conversion
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception:
                    pass 

            # Sampling Logic for Large Files
            if is_large_file:
                sample_n = max(500, int(len(df) * LLM_SAMPLING_RATE))
                df = df.sample(n=sample_n, random_state=42)
                st.warning(f"File size ({file_size_bytes / 1024**3:.2f} GB) exceeded limit. LLM analysis will use a **{sample_n} row sample** for speed and stability.")
            else:
                 st.success(f"Structured file loaded. DataFrame has {len(df)} rows and {len(df.columns)} columns.")
                
            return df, "DataFrame"
            
        except Exception as e:
            st.error(f"Error loading structured file: {e}")
            return None, "Error"

    # 2. Handle Unstructured Data (PDF, DOCX, etc.)
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_file_path = tmp_file.name
        
        try:
            elements = partition(filename=tmp_file_path)
            full_text = "\n\n".join([str(el) for el in elements])
            st.success(f"Unstructured file loaded. Extracted {len(full_text.split())} words.")
            return full_text, "Text"
        except Exception as e:
            st.error(f"Error partitioning file with 'unstructured': {e}")
            return None, "Error"
        finally:
            os.unlink(tmp_file_path)

# --- Streamlit UI ---

st.title(f"🧠 Secure Local Analyst (PandasAI + {OLLAMA_MODEL})")
st.caption(f"LLM: **{OLLAMA_MODEL}** (local, optimized). Supports CSV, XLSX, PDF, DOCX, etc.")

if not st.session_state.llm_connected:
    st.error(f"🛑 Ollama Connection Failed. Ensure 'ollama serve' is running and you have pulled the '{OLLAMA_MODEL}' model.")

st.sidebar.header("Data Uploader")
uploaded_file = st.sidebar.file_uploader(
    "Upload any file (CSV, XLSX, PDF, DOCX, etc.)", 
    type=["csv", "xlsx", "xls", "pdf", "docx", "pptx", "txt", "parquet"]
)

if uploaded_file is not None and st.session_state.llm_connected:
    loaded_data, data_type = load_and_process_file(uploaded_file)
    
    if loaded_data is not None:
        
        st.subheader("Ask Your Data Anything")
        prompt = st.text_area("Enter your analytical, mathematical, or plotting prompt:")
        
        if st.button("Generate Analysis 🚀"):
            if not prompt:
                st.warning("Please enter a prompt!")
            else:
                with st.spinner("Analyzing and Computing..."):
                    
                    if data_type == "DataFrame":
                        sdf = SmartDataframe(
                            df=loaded_data, 
                            config={
                                "llm": st.session_state.llm,
                                "verbose": True, 
                                "response_parser": StreamlitResponse,
                                "enable_advanced_processing": True 
                            }
                        )
                        
                        response = sdf.chat(prompt) 
                        
                        st.write("---") 
                        st.subheader("Final Answer")
                        st.write(response)
                        st.info("The agent successfully used PandasAI to execute the analysis.")
                        
                    elif data_type == "Text":
                        context_prompt = (
                            f"Analyze the following document content and answer the question: '{prompt}'.\n\n"
                            f"Document Content:\n---\n{loaded_data[:4096]}...\n---"
                        )
                        response = st.session_state.llm.invoke(context_prompt)
                        st.subheader("Final Answer")
                        st.write(response)
                        st.info("The agent performed text-based analysis.")
                        
                    else:
                         st.subheader("Final Answer")
                         st.write("Could not process data for analysis.")

    else:
        st.error("Could not load file. Please check file integrity and type.")
        
else:
    st.info("Waiting for file upload and valid Ollama connection.")
