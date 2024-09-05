import os
import json
import configparser
from typing import Dict, List
from NodeData import NodeData
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOpenAI
from crewai_tools import FileReadTool, BaseTool
import networkx as nx
from KeyboardMouseTool import KeyboardMouseTool
from AdditionalTools import WebRequestTool, FileOperationTool, SystemCommandTool

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
    for tool_name in node.tools:
        if tool_name == "KeyboardMouseTool":
            tools.append(KeyboardMouseTool())
        elif tool_name == "WebRequestTool":
            tools.append(WebRequestTool())
        elif tool_name == "FileOperationTool":
            tools.append(FileOperationTool())
        elif tool_name == "SystemCommandTool":
            tools.append(SystemCommandTool())
    
    return Agent(
        role=node.role,
        goal=node.goal,
        backstory=node.backstory,
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=tools
    )

def create_task(node: NodeData, agent: Agent, node_map: Dict[str, NodeData], task_map: Dict[str, Task]) -> Task:
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
    
    # Resolve dependencies with actual Task instances
    dependencies = [task_map[dep_id] for dep_id in node.prevs if dep_id in task_map]

    return Task(
        description=node.description,
        expected_output=node.expected_output,
        agent=agent,
        steps=steps,
        dependencies=dependencies
    )

def topological_sort_tasks(task_nodes: List[NodeData]) -> List[NodeData]:
    graph = nx.DiGraph()

    # Add nodes to the graph
    for node in task_nodes:
        graph.add_node(node.uniq_id)

    # Add edges to the graph
    for node in task_nodes:
        for prev_id in node.prevs:
            if prev_id in graph:
                graph.add_edge(prev_id, node.uniq_id)
    
    # Perform topological sort
    sorted_ids = list(nx.topological_sort(graph))
    
    # Return nodes in sorted order
    id_to_node = {node.uniq_id: node for node in task_nodes}
    sorted_tasks = [id_to_node[node_id] for node_id in sorted_ids]
    
    return sorted_tasks

def RunWorkFlow(node: NodeData, node_map: Dict[str, NodeData], llm):
    print(f"Start root ID: {node.uniq_id}")

    # from root find team
    sub_node_map = {next_id: node_map[next_id] for next_id in node.nexts}
    team_node = find_node_by_type(sub_node_map, "Team")
    if not team_node:
        print("No Team node found")
        return

    print(f"Processing Team {team_node.name} ID: {team_node.uniq_id}")

    # from team find agents
    agent_map = {next_id: node_map[next_id] for next_id in team_node.nexts}
    agent_nodes = find_nodes_by_type(node_map, "Agent")
    agents = {agent_node.name: create_agent(agent_node, llm) for agent_node in agent_nodes}
    for agent_node in agent_nodes:
        print(f"Agent {agent_node.name} ID: {agent_node.uniq_id}")

    # Use BFS to collect all task nodes
    task_nodes = []
    queue = find_nodes_by_type(sub_node_map, "Task")
    
    while queue:
        current_node = queue.pop(0)
        if current_node not in task_nodes:
            print(f"Processing task_node ID: {current_node.uniq_id}")
            task_nodes.append(current_node)
            next_sub_node_map = {next_id: node_map[next_id] for next_id in current_node.nexts}
            queue.extend(find_nodes_by_type(next_sub_node_map, "Task"))

    # Sort tasks topologically to respect dependencies
    sorted_task_nodes = topological_sort_tasks(task_nodes)

    tasks = []
    task_map = {}
    
    # Create tasks with dependencies resolved
    for task_node in sorted_task_nodes:
        if task_node:
            print(f"Processing task_node ID: {task_node.description}")
            agent = agents[task_node.agent]
            task = create_task(task_node, agent, node_map, task_map)
            tasks.append(task)
            task_map[task_node.uniq_id] = task
        else:
            print("No task_node found")
            return

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=2
    )
    
    result = crew.kickoff()
    print("######################")
    print(result)

def run_workflow_from_file(filename: str, llm):
    node_map = load_nodes_from_json(filename)
    start_nodes = find_nodes_by_type(node_map, "Start")
    for start_node in start_nodes:
        RunWorkFlow(start_node, node_map, llm)

















# ... (rest of the file remains the same)