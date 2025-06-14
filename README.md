# ClariGPT

A research assistant chatbot that helps users analyze and summarize academic papers from arXiv using AI-powered tools and a conversational interface.

## Features

- **Research Paper Analysis**: Fetch and analyze papers directly from arXiv using paper IDs
- **PDF Processing**: Extract and parse content from research papers
- **AI-Powered Summarization**: Get intelligent summaries and analysis of academic content
- **Interactive Chat Interface**: Web-based chat interface for seamless interaction
- **Multi-Tool Agent System**: Modular tool system for different research tasks

## Architecture

ClariGPT uses a ReACT (Reasoning and Acting) agent framework with the following components:

- **Agent**: Core reasoning engine that orchestrates tool usage
- **Tools**: Specialized functions for different tasks:
  - `FetchPaper`: Downloads papers from arXiv
  - `Parse`: Extracts text from PDF files
  - `AskExpert`: Provides AI-powered analysis and summaries
  - `Finish`: Returns final results
- **Web Interface**: Flask-based chat application

## Installation

### Using Conda (Recommended)

```bash
# Create environment from environment.yml
conda env create -f environment.yml
conda activate agent
```

### Using pip

```bash
pip install -r requirements.txt
```

## Configuration

1. Set up your Groq API key:
   ```python
   # In chat.py and Tools.py, replace with your API key
   os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
   ```

## Usage

### Web Interface

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Start chatting with ClariGPT! You can ask questions like:
   - "Summarize the paper with arxiv id 2411.05886"
   - "What are the main contributions of paper 2411.05886?"
   - "Explain the methodology in paper [arxiv_id]"

### Jupyter Notebook

You can also use ClariGPT directly in a Jupyter notebook by running `demo.ipynb`.

## Project Structure

```
ClariGPT/
├── app.py              # Flask web application
├── chat.py             # Agent configuration for web interface
├── Agent.py            # Core agent implementation
├── Tools.py            # Tool implementations
├── prompts.py          # System and user prompts
├── demo.ipynb          # Jupyter notebook demo
├── templates/
│   └── chat.html       # Web chat interface
├── static/
│   └── style.css       # Web interface styling
├── Memory/             # Directory for downloaded papers
├── logs.txt            # Agent execution logs
├── requirements.txt    # Python dependencies
└── environment.yml     # Conda environment specification
```

## How It Works

1. **User Input**: User submits a query through the web interface
2. **Agent Processing**: The ReACT agent analyzes the query and determines the appropriate sequence of actions
3. **Tool Execution**: The agent uses various tools:
   - Fetches papers from arXiv
   - Parses PDF content
   - Analyzes content using AI
4. **Response Generation**: The agent provides a comprehensive response based on the analysis

## Dependencies

Key dependencies include:
- **Flask**: Web framework
- **Groq**: AI model API
- **PyMuPDF**: PDF processing
- **Instructor**: Structured AI outputs
- **Pydantic**: Data validation
- **Requests**: HTTP requests for paper fetching

## Example Usage

```python
# Example query
"Summarize the paper with arxiv id 2411.05886"

# The agent will:
# 1. Fetch the paper from arXiv
# 2. Parse the PDF content
# 3. Extract key information
# 4. Generate a comprehensive summary
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source. Please check individual dependencies for their respective licenses.

## Notes

- The system currently processes only the first page of PDFs for efficiency
- API rate limits may apply depending on your Groq subscription
- Downloaded papers are stored locally in the `Memory` directory
- Logs are maintained in `logs.txt` for debugging purposes
