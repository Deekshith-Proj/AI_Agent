import os
import time
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import VectorStoreRetrieverMemory
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Gemini Embeddings for memory
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Vector store for long-term memory
vectorstore = Chroma(
    collection_name="memory",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
memory = VectorStoreRetrieverMemory(retriever=retriever)

conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

def chat_with_memory(user_input: str) -> str:
    try:
        return conversation.run(user_input)
    except ResourceExhausted as e:
        # Handle quota exceeded error
        return "I'm sorry, but the Gemini API quota has been exceeded. Please try again later or check your API quota limits."
    except Exception as e:
        # Handle other errors
        print(f"Error in chat_with_memory: {str(e)}")
        return f"I'm sorry, but an error occurred: {str(e)}"