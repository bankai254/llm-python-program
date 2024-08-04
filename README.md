# LLM Python Program

This project is a Python program that is used to load and query LLM's. It provides the ability to query the LLM via CLI or via a HTTP server.

## Components

-  **LocalLLM**: This is a class and also executable that is responsible for loading a selected LLM, processing a query and returning the response. It maintains a conversation history per session. The conversation history is cleared once the application is closed.
-  **HTTP Server**: This is the main application which is comprised of a simple HTTP server with a custom handler. The custom handler takes the query and model requests and passes to LocalLLM for processing and returns the response to the client.

## Prerequisites

-  **Python**: >= 3.9.x
-  **LLMs**: LLaMA 2 (Llama-2-7b-chat-hf) and Mistral (Mistral-7B-Instruct-v0.1)

## Installation

 1. **Clone the repository:**

	    git clone https://github.com/bankai254/llm-python-program
	    cd llm-python-program

 2. **Setup Virtual Environment**

	    python -m venv llms
	    
	    Run the following on Windows -> llms\Scripts\activate
	    Run the following on Linux/Mac -> source llms/bin/activate

 3. **Get access to LLM's via Hugging Face:**
		This is optional if you already have access to the listed LLMs.
	 - Go to https://huggingface.co/ and sign up
	 - Go to https://huggingface.co/meta-llama/Llama-2-7b-chat-hf and request for access
	 - Go to https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1 and request for access
	 - Check your email for access status. It usually takes less than 10 minutes. 

 - **Install Packages:**

	    pip install -r requirements.txt

 - **Start the server :**

	    docker-compose up --build

 - **Using the CLI (optional or testing the LLM):**

	    python localLLM.py   
