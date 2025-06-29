import streamlit as st 
from dotenv import load_dotenv, find_dotenv
import os

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain

load_dotenv(find_dotenv())

# Setting up envs
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "AI-COURSE-CHATBOT"

# Prompt Template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a very experienced AI Developer and Mentor. Your job is to mentor a person named Senthil (A Microsoft Azure Solutions Architect). He is currently learning about AI and LLMs. You are to help him understand the concepts and help him with his projects."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "Question: {input}"),
    ]
)

# Model
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

# Output Parser
output_parser = StrOutputParser()

# Memory - Fixed: Set return_messages=True for MessagesPlaceholder compatibility
memory = ConversationBufferWindowMemory(
    k=5, 
    memory_key="history", 
    return_messages=True  # This is the key fix
)

# Chain
chain = ConversationChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory
)

# Creating a function to generate response
def generate_response(question):
    response = chain.predict(input=question)
    return response

# Test the function
if __name__ == "__main__":
    response = generate_response("Hello, how are you?")
    print(response)