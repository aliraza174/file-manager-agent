# 📁 LLM-Powered File Management Agent (CLI)

A fully intelligent, conversational file management agent built using **LangChain**, **Groq Llama 3-70B**, and Python. This CLI tool leverages an LLM’s reasoning power to understand natural language instructions for managing files, directories, running terminal commands, reviewing content, analyzing file data, and generating text — all through a clean command-line interface.

---

## ✨ Features

- ✅ Create, delete, move, and write files
- 📄 Read and review file content using LLM reasoning
- 📊 Analyze file and folder contents for summaries, topics, and suggestions
- 🖥️ Run terminal commands safely from any directory
- 💬 Generate text using AI-powered completions
- 🤖 Fully natural-language controlled — no rigid command formats
- 🔄 Conversation memory via LangChain’s buffer memory
- 📝 Clean, readable responses and logs

---

## 📦 Tools Included

| Tool Name      | Purpose                                                           |
|:---------------|:------------------------------------------------------------------|
| `create_file`   | Create a file at a given path                                     |
| `write_file`    | Write content to a file (format: `<path>|||<content>`)            |
| `delete_file`   | Delete a file                                                     |
| `move_file`     | Move a file from one location to another                          |
| `read_file`     | Read and display content of a file                                |
| `review_file`   | Use LLM to review content for issues, suggestions, and formatting |
| `terminal_tool` | Run a terminal command inside a specified directory               |
| `analyze_path`  | Summarize, extract topics, and suggest improvements for files     |
| `generate_text` | Generate AI-powered text from a prompt                            |

---

## 🚀 How It Works

- User enters natural language instructions via the command line.
- The agent uses **LangChain ZERO_SHOT_REACT_DESCRIPTION agent** type to reason about the intent.
- Relevant tool functions are registered and executed based on the LLM's response.
- All conversational context is preserved via **ConversationBufferMemory**.
- The agent automatically handles parsing errors gracefully.

---

## 🛠️ Setup Instructions

1. **Install dependencies**

```bash
pip install -r requirements.txt
