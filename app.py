import os
import json
import gradio as gr
import webbrowser
import threading
import time
from datetime import datetime
from PyPDF2 import PdfReader
from agents.summarizer_agent import summarize
from agents.question_agent import answer
from agents.metadata_agent import extract_metadata
from utils.validator import validate_input, validate_output

# Crea cartelle necessarie
os.makedirs("metadata_exports", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# CSS personalizzato per l'interfaccia
custom_css = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.feature-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 1rem;
    border-left: 4px solid #667eea;
}

.stats-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
    margin: 0.5rem;
}

.upload-area {
    border: 2px dashed #667eea;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    background: #f8f9ff;
}

.question-area {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
}
"""

def load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = "\n".join(p.extract_text() for p in reader.pages)
        return text, len(reader.pages)
    except Exception as e:
        return f"Error loading PDF: {str(e)}", 0

def get_file_stats(text, num_pages):
    """Calculate document statistics"""
    if isinstance(text, str) and not text.startswith("Error"):
        words = len(text.split())
        chars = len(text)
        return {
            "pages": num_pages,
            "words": words,
            "characters": chars,
            "reading_time": max(1, words // 200)  # ~200 words per minute
        }
    return {"pages": 0, "words": 0, "characters": 0, "reading_time": 0}

def process_file(pdf_file):
    if pdf_file is None:
        return "No file uploaded", {}, "", "", "Upload a PDF first", {}
    
    try:
        # Loading PDF
        text, num_pages = load_pdf(pdf_file.name)
        
        if text.startswith("Error"):
            return text, {}, "", "", text, {}
        
        # Document statistics
        stats = get_file_stats(text, num_pages)
        
        # Processing with agents
        summary = summarize(text)
        metadata = extract_metadata(text)
        
        # Output formatting
        stats_display = f"""📊 **Document Statistics**
- 📄 Pages: {stats['pages']}
- 📝 Words: {stats['words']:,}
- 📏 Characters: {stats['characters']:,}  
- ⏱️ Reading time: ~{stats['reading_time']} min"""
        
        return (
            summary, 
            metadata, 
            json.dumps(metadata, indent=2, ensure_ascii=False),
            text,
            stats_display,
            stats
        )
        
    except Exception as e:
        error_msg = f"Error during processing: {str(e)}"
        return error_msg, {}, "", "", error_msg, {}

def ask_question(context, question):
    if not question.strip():
        return "⚠️ Please enter a question to continue."
    
    if not context or not context.strip():
        return "⚠️ Please upload and process a PDF document first."
    
    try:
        validated_question = validate_input(question)
        response = answer(context, validated_question)
        validated_answer = validate_output(response)
        
        return f"🤖 **Answer:**\n\n{validated_answer}"
        
    except ValueError as e:
        return f"❌ Validation error: {str(e)}"
    except Exception as e:
        return f"❌ Error during response: {str(e)}"

def save_metadata(metadata_str, stats):
    if not metadata_str.strip():
        return "❌ No metadata to save."
    
    try:
        metadata = json.loads(metadata_str)
        
        # Add statistics to metadata
        metadata["document_stats"] = stats
        metadata["export_timestamp"] = datetime.now().isoformat()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metadata_{timestamp}.json"
        filepath = os.path.join("metadata_exports", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return f"✅ Metadata saved successfully!\n📁 File: {filename}\n📂 Path: {filepath}"
        
    except json.JSONDecodeError:
        return "❌ Invalid JSON format."
    except Exception as e:
        return f"❌ Error during save: {str(e)}"

def clear_all():
    """Clear all fields"""
    return (
        None,          # pdf_input
        "",            # summary
        {},            # metadata display
        "",            # metadata raw
        "",            # stats
        "",            # question
        "",            # answer
        "",            # save status
        ""             # context
    )

# Creazione dell'interfaccia Gradio
with gr.Blocks(css=custom_css, title="📄 Document AI Assistant", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.HTML("""
    <div class="main-header">
        <h1>🚀 Document AI Multi-Agent Assistant</h1>
        <p>Upload a PDF, get automatic summary and metadata, then ask intelligent questions about the content</p>
    </div>
    """)
    
    # Upload and processing section
    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML('<div class="feature-card"><h3>📤 Document Upload</h3></div>')
            pdf_input = gr.File(
                label="Select your PDF", 
                file_types=[".pdf"],
                file_count="single"
            )
            
            with gr.Row():
                process_btn = gr.Button("🔄 Process Document", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear All", variant="secondary")
        
        with gr.Column(scale=1):
            gr.HTML('<div class="feature-card"><h3>📈 Statistics</h3></div>')
            stats_output = gr.Markdown(value="📊 Upload a PDF to see statistics")
    
    # Processing results
    with gr.Row():
        with gr.Column():
            gr.HTML('<div class="feature-card"><h3>📋 Automatic Summary</h3></div>')
            summary_output = gr.Textbox(
                label="Document summary",
                lines=6,
                interactive=False,
                placeholder="Summary will appear here after processing..."
            )
        
        with gr.Column():
            gr.HTML('<div class="feature-card"><h3>🏷️ Extracted Metadata</h3></div>')
            metadata_output = gr.JSON(label="Structured metadata")
    
    # Metadata saving
    with gr.Row():
        with gr.Column(scale=3):
            save_btn = gr.Button("💾 Save Metadata as JSON", variant="secondary")
        with gr.Column(scale=2):
            save_status = gr.Textbox(
                label="Save status", 
                interactive=False,
                placeholder="Save status..."
            )
    
    # Q&A section
    gr.HTML("""
    <div class="question-area">
        <h2>🤔 Ask Questions About the Document</h2>
        <p>Use AI to get precise answers based on the document content</p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            question_input = gr.Textbox(
                label="Your question",
                placeholder="e.g., What is the main theme of the document? Who is the author? When was it published?",
                lines=2
            )
        with gr.Column(scale=1):
            answer_btn = gr.Button("🎯 Ask", variant="primary", size="lg")
    
    answer_output = gr.Textbox(
        label="AI Answer",
        lines=5,
        interactive=False,
        placeholder="Answer will appear here..."
    )
    
    # State variables
    context_state = gr.State()
    metadata_raw = gr.State()
    stats_state = gr.State()
    
    # Event handlers
    def _process(pdf):
        if pdf is None:
            return ("Select a PDF file", {}, "", "", "No file selected", {})
        
        summary, metadata, meta_str, text, stats_display, stats = process_file(pdf)
        return summary, metadata, meta_str, text, stats_display, stats
    
    process_btn.click(
        _process,
        inputs=[pdf_input],
        outputs=[summary_output, metadata_output, metadata_raw, context_state, stats_output, stats_state]
    )
    
    answer_btn.click(
        ask_question,
        inputs=[context_state, question_input],
        outputs=[answer_output]
    )
    
    save_btn.click(
        save_metadata,
        inputs=[metadata_raw, stats_state],
        outputs=[save_status]
    )
    
    clear_btn.click(
        clear_all,
        outputs=[pdf_input, summary_output, metadata_output, metadata_raw, stats_output, 
                question_input, answer_output, save_status, context_state]
    )
    
    # Informative footer
    gr.HTML("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
        <p><strong>🔧 Features:</strong> Automatic summary • Metadata extraction • Intelligent Q&A • JSON export</p>
        <p><strong>📊 Supports:</strong> PDF files • Multilingual analysis • Input/output validation</p>
    </div>
    """)

def open_browser(url, delay=1.5):
    """Opens browser after a brief delay to ensure server is active"""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 Browser opened automatically: {url}")
        except Exception as e:
            print(f"⚠️ Unable to open browser automatically: {e}")
            print(f"💡 Open manually: {url}")
    
    threading.Thread(target=_open, daemon=True).start()

if __name__ == "__main__":
    # Server configuration
    server_name = "127.0.0.1"  # localhost for security
    server_port = 7860
    
    # Complete application URL
    app_url = f"http://{server_name}:{server_port}"
    
    print("🚀 Starting Document AI Multi-Agent Assistant...")
    print(f"🔗 URL: {app_url}")
    print("⏳ Preparing interface...")
    
    # Start thread to open browser
    open_browser(app_url, delay=2)
    
    # Launch Gradio application
    demo.launch(
        share=False,
        server_name=server_name,
        server_port=server_port,
        show_error=True,
        quiet=False,  # Show startup logs
        inbrowser=True  # Gradio native attempt to open browser
    )