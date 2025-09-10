from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI  # type: ignore
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Error handling if key is missing
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the environment. Please check your .env file.")

# Initialize the LLM with the API key
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=api_key
)

# Define the email categorization agent
email_agent = Agent(
    role="Email Analyzer",
    goal="Categorize emails as subscription, coupon, free trial, deal, or other",
    backstory="Expert in analyzing marketing and subscription emails",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Main function to run categorization
def get_email_category(subject: str, snippet: str) -> str:
    task = Task(
        description=f"""Categorize this email into one of:
        ["subscription", "coupon", "free trial", "deal", "other"].

        Subject: {subject}
        Snippet: {snippet}

        Only respond with the category name (exact match, all lowercase).""",
        expected_output="One of the following words: subscription, coupon, free trial, deal, or other.",
        agent=email_agent
    )

    crew = Crew(
        agents=[email_agent],
        tasks=[task],
        verbose=True,
        process=Process.sequential
    )

    result = crew.kickoff()
    return str(result).strip().lower()
