from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI  # type: ignore

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

email_agent = Agent(
    role="Email Analyzer",
    goal="Categorize emails as subscription, coupon, free trial, deal, or other",
    backstory="Expert in analyzing marketing and subscription emails",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

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
