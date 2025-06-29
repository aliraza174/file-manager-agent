import os
import shutil
import time
import subprocess
from langchain.tools import Tool
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# === Initialize Groq LLM ===
llm = ChatGroq(
    temperature=0.2,
    api_key=groq_api_key,
    model_name="llama3-70b-8192"
)

# === Helper to clean newlines ===
def clean_newlines(text: str) -> str:
    """Replace any escaped '\\n' with real line breaks and tidy up text."""
    return text.replace("\\n", "\n")

# === File and Terminal Functions ===

def create_file(full_path: str) -> str:
    path, filename = os.path.split(full_path)
    if not path or not filename:
        return "Missing path or filename."
    if not os.path.exists(path):
        return f"Path does not exist: {path}"
    if filename in os.listdir(path):
        return f"File '{filename}' already exists in {path}"
    try:
        with open(os.path.join(path, filename), 'w'):
            pass
        return f"File '{filename}' created at {path}"
    except Exception as e:
        return f"Failed to create file: {e}"

def write_file(path_and_content: str) -> str:
    try:
        full_path, content = path_and_content.split('|||', 1)
        content = clean_newlines(content)  # Clean newlines before writing
        path, filename = os.path.split(full_path)
        if not os.path.isdir(path):
            return f"Path does not exist: {path}"
        with open(os.path.join(path, filename), 'w') as file:
            file.write(content)
        return f"Wrote content to '{filename}' in {path}"
    except ValueError:
        return "Invalid input format. Expected: <full_path>|||<content>"
    except Exception as e:
        return f"Failed to write to file: {e}"

def delete_file(full_path: str) -> str:
    if not os.path.isfile(full_path):
        return "File does not exist."
    try:
        os.remove(full_path)
        return f"Deleted file at {full_path}"
    except Exception as e:
        return f"Failed to delete file: {e}"

def create_dir(full_path: str) -> str:
    if os.path.exists(full_path):
        return "Directory already exists."
    try:
        os.makedirs(full_path)
        return f"Directory created at {full_path}"
    except Exception as e:
        return f"Error creating directory: {e}"

def delete_dir(full_path: str) -> str:
    if not os.path.isdir(full_path):
        return "Directory does not exist."
    try:
        shutil.rmtree(full_path)
        return f"Deleted directory {full_path}"
    except Exception as e:
        return f"Error deleting directory: {e}"

def move_file(src_and_dest: str) -> str:
    try:
        src, dest = src_and_dest.split('|||')
        if not os.path.isfile(src):
            return "Source file not found."
        shutil.move(src, dest)
        return f"Moved file from {src} to {dest}"
    except Exception as e:
        return f"Failed to move file: {e}"

def terminal_tool(path_and_command: str) -> str:
    try:
        path, command = path_and_command.split('|||')
        if not os.path.isdir(path):
            return "Directory does not exist."
        result = subprocess.check_output(command, cwd=path, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except Exception as e:
        return f"Command failed: {e}"

# === LLM-Powered Text Generation Function ===
def generate_text(prompt: str) -> str:
    try:
        result = llm.invoke(prompt)
        clean_text = clean_newlines(result.content)
        return clean_text
    except Exception as e:
        return f"Failed to generate text: {e}"

# === Register LangChain Tools ===
tools = [
    Tool.from_function(create_file, name="create_file", description="Create a file at a full path."),
    Tool.from_function(write_file, name="write_file", description="Write content to a file. Format: <full_path>|||<content>"),
    Tool.from_function(delete_file, name="delete_file", description="Delete a file by full path."),
    Tool.from_function(create_dir, name="create_dir", description="Create a directory by full path."),
    Tool.from_function(delete_dir, name="delete_dir", description="Delete a directory by full path."),
    Tool.from_function(move_file, name="move_file", description="Move a file. Format: <source_path>|||<destination_path>"),
    Tool.from_function(terminal_tool, name="terminal_tool", description="Run terminal command in a given directory. Format: <path>|||<command>"),
    Tool.from_function(generate_text, name="generate_text", description="Generate text based on a given prompt like poem, code, or explanation.")
]

# === Conversation Memory ===
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# === LangChain Agent Setup ===
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# === Main Chat Loop ===
print("💬 File Agent is running. Type 'exit' to quit.")

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        break

    response = agent.invoke({"input": user_input})
    if isinstance(response, str):
        print(f"\n🤖 Agent: {response}\n")
    elif hasattr(response, 'content'):
        # LLM message response
        print(f"\n🤖 Agent:\n{clean_newlines(response.content)}\n")
    else:
        print(f"\n🤖 Agent: {response}\n")
