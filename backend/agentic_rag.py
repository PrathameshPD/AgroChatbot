import os
from dotenv import load_dotenv

# Load environment variabless
# Load environment variabless
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

try:
    from langchain.agents import AgentExecutor, create_tool_calling_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
    from langchain_community.vectorstores import SupabaseVectorStore
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    from langchain import hub
    from langchain_core.tools import tool
    from supabase.client import Client, create_client
    
    IMPORTS_SUCCESS = True
except ImportError as e:
    with open("debug_error.log", "w") as f:
        import sys
        f.write(f"Executable: {sys.executable}\n")
        f.write(f"ImportError: {e}")
    print(f"Critical Import Error in agentic_rag: {e}")
    IMPORTS_SUCCESS = False
except Exception as e:
    with open("debug_error.log", "w") as f:
        f.write(f"Exception: {e}")
    print(f"Critical Error in agentic_rag: {e}")
    IMPORTS_SUCCESS = False

if IMPORTS_SUCCESS:
    try:
        # Initiate Supabase database
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        supabase: Client = create_client(supabase_url, supabase_key)

        # Initiate Google Generative AI embeddings
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )

        # Initiate vector store connection
        vector_store = SupabaseVectorStore(
            embedding=embeddings,
            client=supabase,
            table_name="documents",
            query_name="match_documents",
        )

        # Use Google Generative AI model
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-flash-latest",   
            temperature=1,
            max_output_tokens=8192,
            top_p=1,
            google_api_key=GOOGLE_API_KEY
        )

        # Fetch the base prompt from the LangChain Hub and modify it
        prompt = hub.pull("hwchase17/openai-functions-agent")
        
        # Add our custom instructions to the system message
        custom_instructions = (
            "\n\nIMPORTANT: Always keep your responses concise, strictly between 2 to 4 lines. "
            "If you use the 'generate_report' tool, you MUST show the download link exactly as returned by the tool."
        )
        if hasattr(prompt.messages[0], 'prompt'):
            prompt.messages[0].prompt.template += custom_instructions
        else:
            prompt.messages[0].content += custom_instructions

        # Create a retrieval tool
        @tool
        def retrieve(query: str):
            """Retrieve information related to a query."""
            retrieved_docs = vector_store.similarity_search(query, k=2)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized

        # Create a report generation tool
        @tool
        def generate_report(year: str, location: str):
            """Generate a PDF report for rice crop data based on year and location.
            Args:
                year (str): The sampled year (e.g., '2022', '2023').
                location (str): The name of the village or location.
            """
            try:
                import pandas as pd
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas
                from reportlab.lib import colors
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet
                
                # Load data
                data_path = os.path.join(os.path.dirname(__file__), "documents", "Cleaned_Data.xlsx")
                if not os.path.exists(data_path):
                    return "Error: Data file not found."
                    
                df = pd.read_excel(data_path)
                
                # Normalize data for filtering
                try:
                    df['Sampled Year'] = df['Sampled Year'].astype(int)
                    year_int = int(year)
                except ValueError:
                    year_int = year 
                
                # Filter data
                filtered_df = df[
                    (df['Sampled Year'] == year_int) & 
                    (df['Name of Village'].astype(str).str.contains(location, case=False, na=False))
                ]
                
                if filtered_df.empty:
                    return f"No data found for Year: {year} and Location: {location}."
                
                report_filename = f"Rice_Crop_Report_{location}_{year}.pdf"
                report_dir = os.path.join(os.path.dirname(__file__), "reports")
                os.makedirs(report_dir, exist_ok=True)
                report_path = os.path.join(report_dir, report_filename)
                
                doc = SimpleDocTemplate(report_path, pagesize=letter)
                elements = []
                styles = getSampleStyleSheet()
                
                elements.append(Paragraph(f"Rice Crop Report - {location} ({year})", styles['Title']))
                elements.append(Spacer(1, 12))
                elements.append(Paragraph(f"This report summarizes rice crop samples for {location} in {year}.", styles['Normal']))
                elements.append(Spacer(1, 12))
                
                columns_to_show = ['Name of Village', 'Crop Name', 'pH', 'P', 'K', 'Fertilizer Used', 'Yield Returns']
                available_cols = [c for c in columns_to_show if c in filtered_df.columns]
                table_data = [available_cols] + filtered_df[available_cols].astype(str).values.tolist()
                
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BottomPadding', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                ]))
                elements.append(t)
                doc.build(elements)
                
                base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
                download_link = f"{base_url}/reports/{report_filename}"
                return f"Report generated successfully. You can download it here: [{report_filename}]({download_link})"
                
            except Exception as e:
                return f"Error generating report: {str(e)}"

        # Persistent Agent Initialization
        tools = [retrieve, generate_report]
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Memory Setup
        from langchain_community.chat_message_histories import ChatMessageHistory
        from langchain_core.runnables.history import RunnableWithMessageHistory

        store = {}

        def get_session_history(session_id: str):
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        def get_response(query: str, session_id: str = "default"):
            print(f"Debug: Received query: {query} for session: {session_id}")
            try:
                response = agent_with_chat_history.invoke(
                    {"input": query},
                    config={"configurable": {"session_id": session_id}},
                )
                print(f"Debug: Response from agent: {response}")
                return response["output"]
            except Exception as e:
                print(f"Error executing agent: {e}")
                return f"Error: {str(e)}"

    except Exception as e:
        with open("debug_error.log", "w") as f:
            f.write(f"InitializationError: {e}")
        print(f"Critical Initialization Error in agentic_rag: {e}")
        IMPORTS_SUCCESS = False

if not IMPORTS_SUCCESS:
    def get_response(query: str, session_id: str = "default"):
        return "System Error: The backend encountered a critical dependency issue. Please check the logs."