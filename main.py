from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from langchain.callbacks.tracers import LangChainTracer
from langchain.callbacks.manager import collect_runs
from langsmith import Client

import uuid

from dotenv import load_dotenv
load_dotenv()

client = Client()

tracer = LangChainTracer(client)

output_parser = StrOutputParser()


# NOTE: tested with Claude 3 Haikue and mixtral-8x7b-32768 and neither work due to input/output formatting issues
# this works, and is faster and cheaper than GPT-4
llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")

# and this works, but slower and costs a bit
# llm = ChatOpenAI(model="gpt-4")

from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# Other agent_types: zero-shot-react-description, openai-tools (legacy - use tool-calling instead)
agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)

# Simulate user. For Langsmith tracing only.
user_id = str(uuid.uuid4())
print(f"User ID: {user_id}")

stop = False
while not stop:
    try:
        question = input("Enter a question (or 'x' to exit): ")
        if (question == "x"):
            stop = True
            continue
        
        with collect_runs() as runs_cb:
            response = agent_executor.invoke({"input": question},
                        config = {"tags": ["project-type", "sql-query"],
                        "metadata": {"user_id": user_id},
                        "run_name": "sql-query-agent"
                        }
                        #  config= {"callbacks": [tracer]}
                    )
            
            print("Langsmith run id:", runs_cb.traced_runs[0].id)
            
            print("Answer:", response["output"] + "\n")
            
            # Ratings could be any scale: 1-5, thumbs-up/down (1 or 0), number of stars, range of emojis... just have to translate to number or boolean.
            user_rating = int(input("Rate the response (1-5): "))
            user_comments = input("(Optional) Enter any comments for feedback: ")
            
            client.create_feedback(
                run_id=runs_cb.traced_runs[0].id,
                key="user-rating",
                score=user_rating,
                comment=user_comments
            )
        
    finally:
        wait_for_all_tracers()