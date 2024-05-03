# SQL Query Agent with Langsmith Tracing

This project is an AI-powered SQL query agent that can answer natural language questions by querying a SQLite database. It utilizes the LangChain library and various language models, such as ChatGroq and ChatOpenAI, to generate SQL queries and provide responses. Additionally, it integrates with Langsmith for tracing and feedback collection.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

**Prerequisites**
- Python 3.7 or higher
- SQLite client

1. **Create API keys for your desired LLM and also for Langsmith.**:
   Create your LLM keys for the desired language model of your choice. 

   Create your Langsmith API key by signing up for a free account at https://langsmith.com/signup.

2. **Clone the repository**
    ```
    git clone https://github.com/your-repo/sql-query-agent.git
    cd sql-query-agent
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
- Rename the `.env_example` file to `.env`
- Fill in the required API keys and configuration values in the `.env` file

5. Create the Chinook.db database
    ```
    sqlite3 Chinook.db

    SQLite version 3.44.0 2023-11-01 11:23:50
    Enter ".help" for usage hints.
    sqlite>.read Chinook_Sqlite.sql
    ```

## Usage

1. **Run the project**
```python main.py```


2. **Enter a question**
When prompted, enter a natural language question related to the SQLite database.

3. **Rate the response**
After receiving the answer, rate the response on a scale of 1-5.

4. **Provide feedback (optional)**
You can optionally provide comments or feedback for the response.

The project will trace the execution using Langsmith and collect feedback for future improvements.