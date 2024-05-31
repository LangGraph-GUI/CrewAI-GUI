# main.py

import argparse
import os
import configparser
from WorkFlow import run_workflow_from_file
from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from Tee import Tee

def main():
    parser = argparse.ArgumentParser(description="Run workflow from a JSON graph definition.")
    parser.add_argument('--graph', required=True, help="Path to the JSON file defining the graph.")
    parser.add_argument('--keys', help="Path to the credentials file.")
    parser.add_argument('--tee', help="File to write the output log to.")
    parser.add_argument('--llm', help="use what llm")
    
    args = parser.parse_args()
    
    if args.tee:
        tee = Tee(args.tee)

    if args.keys:
        config = configparser.ConfigParser()
        config.read(args.keys)
        os.environ["OPENAI_API_KEY"] = config['OpenAI']['api_key']
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o")
    elif args.llm:
        os.environ["OPENAI_API_KEY"] = "sk-proj-not-use-it"
        llm = Ollama(model=args.llm)

    run_workflow_from_file(args.graph, llm)

    if args.tee:
        tee.close()

if __name__ == "__main__":
    main()
