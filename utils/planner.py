from langchain_core.prompts import ChatPromptTemplate

from utils.ai_client import llm
from utils.agent_prompt import SYSTEM_PROMPT
from utils.schemas import AgentPlan

planner = llm.with_structured_output(AgentPlan)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            """Dataset Information:
        {dataset_context}

        Working Memory:
        {ai_memory}

        Previous Conversation:
        {chat_memory}

        User Request:
        {question}"""
        )
    ]
)


def create_plan(
    question: str,
    dataset_context: str,
    chat_memory: str = "" ,
    ai_memory: str =""
) -> AgentPlan:
    
    chain = prompt | planner

    return chain.invoke(
        {
            "question": question,
            "dataset_context": dataset_context,
            "chat_memory": chat_memory, 
            "ai_memory": ai_memory,
        }
    )  