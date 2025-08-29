# Document AI Multi-Agent Assistant 🚀

A sophisticated document intelligence system that leverages multiple AI agents to automatically analyze, summarize, and interact with PDF documents. Built with Google Gemini API and Gradio for an intuitive web interface.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Gradio](https://img.shields.io/badge/gradio-latest-orange.svg)
![Google Gemini](https://img.shields.io/badge/gemini-1.5--flash-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Overview

This application transforms how you interact with documents by providing three specialized AI agents working in harmony:

- **Summarizer Agent**: Generates concise, intelligent summaries of document content
- **Metadata Extractor**: Automatically identifies titles, authors, dates, and keywords  
- **Question Agent**: Answers specific queries about document content with contextual understanding

The system processes PDF documents through an elegant web interface, making document analysis accessible to users without technical expertise while maintaining the power and flexibility needed for professional workflows.

## ✨ Key Features

**Intelligent Document Processing**
- Upload PDF files and receive instant AI-powered analysis
- Multi-agent architecture ensures specialized, high-quality outputs for each task
- Handles documents of varying lengths with smart text truncation strategies

**Interactive Question-Answering**
- Ask natural language questions about your documents
- Context-aware responses grounded in the actual document content
- Support for multiple question types: factual, analytical, and interpretive

**Metadata Management**
- Automatic extraction of document metadata including titles, authors, and publication dates
- Intelligent keyword identification from document content
- Export functionality for structured JSON metadata storage

**Professional Web Interface**
- Clean, intuitive Gradio-based interface requiring no technical setup
- Real-time processing feedback and document statistics
- Responsive design suitable for both desktop and mobile use

**Safety and Validation**
- Built-in content filtering and input validation
- Robust error handling with graceful failure recovery
- Secure API key management through environment variables

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev/))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/document-ai-assistant.git
   cd document-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Launch the application**
   ```bash
   python app.py
   ```

The application will automatically open in your browser at `http://localhost:7860`

## 📁 Project Structure

```
Document-Chat-MultiAgent-Gradio/
├── app.py                      # Main application and Gradio interface
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (API keys)
├── .gitignore                 # Git ignore rules
├── agents/
│   ├── summarizer_agent.py    # Document summarization logic
│   ├── question_agent.py      # Question-answering functionality
│   └── metadata_agent.py      # Metadata extraction with fallback
├── utils/
│   ├── gemini_client.py       # Google Gemini API client
│   └── validator.py           # Input/output validation
├── data/                      # Document storage (created automatically)
└── metadata_exports/          # Exported metadata files (created automatically)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Customization Options

**Agent Behavior**: Modify prompt templates in individual agent files to adjust output style and focus areas.

**Interface Styling**: Update the `custom_css` variable in `app.py` to customize the web interface appearance.

**Validation Rules**: Extend the validation logic in `utils/validator.py` to implement custom content filtering requirements.

## 📖 Usage Guide

### Basic Workflow

1. **Upload Document**: Select a PDF file using the upload interface
2. **Process**: Click "Process Document" to run all three AI agents automatically  
3. **Review Results**: Examine the generated summary and extracted metadata
4. **Ask Questions**: Use the interactive Q&A section for specific inquiries
5. **Export Data**: Save metadata as JSON for external use

### Advanced Features

**Batch Processing**: The modular architecture supports extension for batch document processing workflows.

**Custom Agents**: Add new specialized agents by following the existing agent patterns in the `agents/` directory.

**API Integration**: The core processing functions can be imported and used independently of the Gradio interface.

## 🔍 Technical Architecture

### Multi-Agent Design

Each agent maintains focused responsibilities:

- **Separation of Concerns**: Individual agents handle specific document analysis tasks
- **Independent Scaling**: Agents can be deployed and scaled independently
- **Specialized Prompting**: Each agent uses optimized prompts for its specific function

### Error Handling

The system implements comprehensive error handling:

- **Graceful Degradation**: Fallback methods ensure continued operation when primary approaches fail
- **User-Friendly Messages**: Technical errors are translated to understandable feedback
- **Logging**: Detailed error logging supports troubleshooting and system monitoring

### Performance Optimization

- **Smart Truncation**: Large documents are intelligently truncated to stay within API limits
- **Session Management**: User state is maintained efficiently without persistent storage
- **Responsive Interface**: Gradio provides automatic loading states and progress feedback

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository** and create a feature branch
2. **Make your changes** following the existing code style and patterns  
3. **Add tests** for new functionality where applicable
4. **Update documentation** to reflect your changes
5. **Submit a pull request** with a clear description of your improvements

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Add docstrings for new functions and classes
- Include error handling for external API calls
- Test with various document types and sizes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


**Ready to transform your document workflow?** Upload your first PDF and experience the power of AI-driven document intelligence!
