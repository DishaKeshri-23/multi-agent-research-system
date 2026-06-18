🔍 ResearchMind - Multi-Agent Research System

ResearchMind is an AI-powered Multi-Agent Research System that automates web research and report generation using specialized AI agents. The system leverages Google Gemini 2.5 Flash, LangChain, Tavily Search, and BeautifulSoup to gather, analyze, and synthesize information from multiple online sources into structured research reports.

🚀 Features

- Multi-Agent Architecture using LangChain
- Search Agent for discovering relevant web sources
- Reader Agent for extracting and analyzing content from webpages
- Automated Research Report Generation
- Powered by Google Gemini 2.5 Flash
- Web Search Integration with Tavily
- Web Scraping using BeautifulSoup
- Interactive Streamlit User Interface
- Structured and Detailed Research Outputs

🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini 2.5 Flash
- Tavily Search API
- BeautifulSoup
- Requests
- Python Dotenv

⚙️ Workflow

1. User enters a research topic.
2. Search Agent collects relevant sources from the web.
3. Reader Agent extracts and analyzes webpage content.
4. Writer Chain synthesizes gathered information.
5. The system generates a detailed and structured research report.

📂 Project Structure

multi-agent-research-system/
│
├── app.py              # Streamlit application
├── agents.py           # Search and Reader agents
├── pipeline.py         # Research workflow pipeline
├── tools.py            # Search and scraping tools
├── requirements.txt    # Dependencies
├── .gitignore
└── README.md


🔑 Environment Variables

Create a .env file and add:

GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key


📦 Installation

bash
git clone https://github.com/DishaKeshri-23/multi-agent-research-system.git

cd multi-agent-research-system

pip install -r requirements.txt


▶️ Run Locally

bash
streamlit run app.py

⭐ If you found this project useful, consider giving it a star!
