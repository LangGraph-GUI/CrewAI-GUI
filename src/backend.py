import argparse
import os
import configparser
from WorkFlow import run_workflow_from_file
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from Tee import Tee

def get_openai_api_key(config_path=None):
    # First, try to get the API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # If not found in environment, try to get from config file
    if not api_key and config_path:
        config = configparser.ConfigParser()
        config.read(config_path)
        if 'OpenAI' in config and 'api_key' in config['OpenAI']:
            api_key = config['OpenAI']['api_key']
    
    return api_key

def main():
    parser = argparse.ArgumentParser(description="Run workflow from a JSON graph definition.")
    parser.add_argument('--graph', required=True, help="Path to the JSON file defining the graph.")
    parser.add_argument('--keys', help="Path to the credentials file.")
    parser.add_argument('--tee', help="File to write the output log to.")
    parser.add_argument('--llm', help="Specify which LLM to use")
    
    args = parser.parse_args()
    
    if args.tee:
        tee = Tee(args.tee)

    api_key = get_openai_api_key(args.keys)

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
    elif args.llm:
        llm = Ollama(model=args.llm)
    else:
        raise ValueError("No OpenAI API key found and no alternative LLM specified.")

    run_workflow_from_file(args.graph, llm)

    if args.tee:
        tee.close()

if __name__ == "__main__":
    main()