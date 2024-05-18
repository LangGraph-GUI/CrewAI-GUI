# main.py

import os
import json
import configparser
from typing import Dict, List
from NodeData import NodeData
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from langchain.chat_models import ChatOpenAI
from crewai_tools import FileReadTool, BaseTool

def load_nodes_from_json(filename: str) -> Dict[str, NodeData]:
    with open(filename, 'r') as file:
        data = json.load(file)
        node_map = {}
        for node_data in data["nodes"]:
            node = NodeData.from_dict(node_data)
            node_map[node.uniq_id] = node
        return node_map

def find_nodes_by_type(node_map: Dict[str, NodeData], node_type: str) -> List[NodeData]:
    return [node for node in node_map.values() if node.type == node_type]

def find_node_by_type(node_map: Dict[str, NodeData], node_type: str) -> NodeData:
    for node in node_map.values():
        if node.type == node_type:
            return node
    return None

class FileWriterTool(BaseTool):
    name: str = "FileWriter"
    description: str = "Writes given content to a specified file."

    def _run(self, filename: str, content: str) -> str:
        with open(filename, 'w') as file:
            file.write(content)
        return f"Content successfully written to {filename}"

def create_agent(node: NodeData, llm) -> Agent:
    tools = []
    tools.append(FileWriterTool())
    tools.append(FileReadTool())
    
    return Agent(
        role=node.role,
        goal=node.goal,
        backstory=node.backstory,
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=tools
    )

def create_task(node: NodeData, agent: Agent, node_map: Dict[str, NodeData]) -> Task:
    steps = []
    for step_id in node.nexts:
        step_node = node_map[step_id]
        tool_instance = None
        if step_node.tool == "FileWriterTool()":
            tool_instance = FileWriterTool()
        elif step_node.tool == "FileReadTool()":
            tool_instance = FileReadTool()
        step = {
            'tool': tool_instance,
            'args': step_node.arg,
            'output_var': step_node.output_var
        }
        steps.append(step)
    return Task(
        description=node.description,
        expected_output=node.expected_output,
        agent=agent,
        steps=steps
    )

def RunWorkFlow(node: NodeData, node_map: Dict[str, NodeData], llm):
    print(f"Start root ID: {node.uniq_id}")

    sub_node_map = {next_id: node_map[next_id] for next_id in node.nexts}

    team_node = find_node_by_type(sub_node_map, "Team")
    if not team_node:
        print("No Team node found")
        return

    print(f"Processing Team {team_node.name} ID: {team_node.uniq_id}")

    agent_map = {next_id: node_map[next_id] for next_id in team_node.nexts}
    agent_nodes = find_nodes_by_type(node_map, "Agent")
    agents = {agent_node.name: create_agent(agent_node, llm) for agent_node in agent_nodes}
    for agent_node in agent_nodes:
        print(f"Agent {agent_node.name} ID: {agent_node.uniq_id}")

    task_nodes = []
    temp_node = find_node_by_type(sub_node_map, "Task")
    if temp_node:
        task_nodes.append(temp_node)
    while temp_node and len(temp_node.nexts) > 0:
        temp_node_map = {next_id: node_map[next_id] for next_id in temp_node.nexts}
        temp_node = find_node_by_type(temp_node_map, "Task")
        if temp_node:
            task_nodes.append(temp_node)
        else:
            break

    tasks = []
    for task_node in task_nodes:
        if task_node:
            print(f"Processing task_node ID: {task_node.uniq_id}")
            task = create_task(task_node, agents[task_node.agent], node_map)
            tasks.append(task)
        else:
            print("No task_node node found")
            return

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=2
    )
    
    result = crew.kickoff()
    print("######################")
    print(result)

# Usage example
def main():
    filename = 'example.json'
    node_map = load_nodes_from_json(filename)

    config = configparser.ConfigParser()
    config.read('credentials.ini')
    os.environ["OPENAI_API_KEY"] = config['OpenAI']['api_key']

    gpt4o = ChatOpenAI(temperature=0.7, model_name="gpt-4o")
    phi3 = Ollama(model='phi3')
    llm = gpt4o
    llm = phi3

    start_nodes = find_nodes_by_type(node_map, "Start")
    for start_node in start_nodes:
        RunWorkFlow(start_node, node_map, llm)

if __name__ == "__main__":
    main()
