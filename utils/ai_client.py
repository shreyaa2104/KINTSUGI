import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
 raise ValueError(
  "GROQ_API_KEY not found. Please add it to your .env file."
 )

llm=ChatGroq(
 model="llama-3.3-70b-versatile",
 temperature=0,
 api_key=api_key
)
