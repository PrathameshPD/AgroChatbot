import os
import sys

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    print("Attempting to import langchain.agents...")
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    print("Success.")
except Exception as e:
    print(f"FAILED: {e}")

try:
    print("Attempting to import langchain_community.vectorstores...")
    from langchain_community.vectorstores import SupabaseVectorStore
    print("Success.")
except Exception as e:
    print(f"FAILED: {e}")

try:
    print("Attempting to import langchain_google_genai...")
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    print("Success.")
except Exception as e:
    print(f"FAILED: {e}")

try:
    print("Attempting to import numpy...")
    import numpy
    print(f"Success. NumPy version: {numpy.__version__}")
except Exception as e:
    print(f"FAILED numpy: {e}")

try:
    print("Attempting to import langchain (hub)...")
    from langchain import hub
    print("Success.")
except Exception as e:
    print(f"FAILED langchain: {e}")

try:
    print("Attempting to import langchain_core...")
    from langchain_core.tools import tool
    print("Success.")
except Exception as e:
    print(f"FAILED langchain_core: {e}")

try:
    print("Attempting to import supabase...")
    from supabase.client import Client, create_client
    print("Success.")
except Exception as e:
    print(f"FAILED: {e}")
