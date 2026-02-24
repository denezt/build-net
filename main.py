import asyncio
import os
import sys
from ollama import AsyncClient
import spacy

# Load a specific language model
nlp = spacy.load("en_core_web_sm")  # or "en_core_web_lg"
model_name = os.getenv("MODEL_NAME", "llama3.2:3b")  # Default to "llama3.2:3b" if not set

def summarize_text(text, summary_length=3):    
    nlp.max_length = len(text) + 1000 # Set max_length to be slightly larger than the input text
    # Process the text into a doc object
    doc = nlp(text)    
    # Generate abstracts for different length summaries
    if summary_length == 1:
        return [doc.text[:2000]]  # First 100 characters
    elif summary_length == 2:
        return [f"{doc.text[:50]}...\n{doc.text[-50:] if len(doc.text) > 50 else doc.text}"]  # First 50, last 50, joined with "..."
    else:  # Summary length >=3
        sentences = [str(sent) for sent in doc.sents]
        # Join first few and last few sentences
        summary = f"{sentences[:summary_length-1][0]}...\n{sentences[-summary_length+1:][-1]}" if len(sentences) > summary_length else sentences[0][:100]  # Keep only the first sentence
    return [summary]

def process_text(text):
    nlp.max_length = len(text) + 1000 # Set max_length to be slightly larger than the input text
    doc = nlp(text)    
    print(f"Text: {text}")
    print(f"Length of document: {len(doc)}")
    
    return {
        'sentence_count': len(list(doc.sents)),
        'word_count': sum(len(sent.text.split()) for sent in doc.sents),
        'avg_word_length': sum(len(sent.text) for sent in doc.sents)/sum(len(text.split()) for text in [sent.text for sent in doc.sents]),
    }

async def chat(prompt: str):
    message = {
        'system': 'You are a helpful assistant that analyzes data and provides insights.',
        'role': 'user', 
        'content': prompt
    }
    response = await AsyncClient().chat(model=model_name, messages=[message])
    print("Response from model:")
    print(response['message']['content'])

def parse_logs():
    print("Running build-net log parser!")
    log_directory = "/var/log"
    for filename in os.listdir(log_directory):        
        if filename.endswith(".log"):
            filepath = os.path.join(log_directory, filename)
            log_data = []
            with open(filepath, 'r') as file:
                print(f"Checking log file {filename}:")
                for line in file:
                    log_data.append(line.strip())
            summary = summarize_text(" ".join(log_data[:500]), summary_length=2)
            print(f"Summary for {filename}: {summary}")
            asyncio.run(chat(" ".join(summary)))

def main():
    parse_logs()    

if __name__ == "__main__":
    main()