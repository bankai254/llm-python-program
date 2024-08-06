# localLLM.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from os import environ

from dotenv import load_dotenv

load_dotenv()

hf_access_token = environ["HF_TOKEN"]
class LocalLLM:
    def __init__(self):
        self.model_name = None
        self.tokenizer = None
        self.model = None
        self.conversation_history = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # Use GPU if available 

    def select_model(self, model = None):
        while True:
            if model == None: # Allow manual input of choice otherwise pass the selection from API server request
                print("Welcome to the LLM Chat Program!")
                print("Please select a model:")
                print("1. LLaMA 2")
                print("2. Mistral")

                choice = int(input("Enter the number of your choice (1 or 2): ").strip())
            else:
                choice = 1

            if choice == 1:
                self.model_name = "meta-llama/Llama-2-7b-chat-hf"
                break
            elif choice == 2:
                self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
                break
            else:
                print("Invalid choice. Please try again.")

        print(f"Loading {self.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, token=hf_access_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name, 
            torch_dtype=torch.float16, 
            low_cpu_mem_usage=True
        ).to(self.device)
        print(f"Model loaded successfully on {self.device}.")

    def generate_response(self, query):
        full_prompt = "\n".join(self.conversation_history + [f"You: {query}", "AI:"])
        inputs = self.tokenizer.encode(full_prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs, 
                max_length=2048, 
                temperature=0.7, 
                num_return_sequences=1,
                do_sample=True
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        ai_response = response.split("AI:")[-1].strip()
        
        self.conversation_history.append(f"You: {query}")
        self.conversation_history.append(f"AI: {ai_response}")
        
        return ai_response

    def chat(self, query):
        if query == None: # Not required if using
            print("Type 'exit' to end the conversation.")

        while True:
            query = input("You: ").strip()
            if query.lower() == 'exit':
                break
            response = self.generate_response(query)
            print("AI:", response)

def main():
    llm = LocalLLM()
    llm.select_model()
    llm.chat()
    

if __name__ == "__main__":
    main()