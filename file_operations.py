# file_operations.py

import json
from PySide6.QtWidgets import QFileDialog
from Node import Node
from Edge import Edge
from NodeData import NodeData

def save(scene):
    filename, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON Files (*.json)")
    if filename:
        data = {
            "nodes": [],
            "node_counter": scene.node_counter
        }

        for item in scene.items():
            if isinstance(item, Node):
                node_dict = item.data.to_dict()
                data["nodes"].append(node_dict)

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

def load(scene):
    filename, _ = QFileDialog.getOpenFileName(None, "Load File", "", "JSON Files (*.json)")
    if filename:
        with open(filename, 'r') as file:
            data = json.load(file)

            node_map = {}

            # Load the node counter
            scene.node_counter = data.get("node_counter", 1)

            # First create all nodes
            for node_data in data["nodes"]:
                node_data_obj = NodeData.from_dict(node_data)
                node = Node(node_data_obj)
                scene.addItem(node)
                node_map[node_data_obj.uniq_id] = node

            # Then create edges based on `nexts`
            edge_set = set()  # To track created edges and avoid duplicates
            for node_data in data["nodes"]:
                source_node = node_map[node_data["uniq_id"]]
                for next_id in node_data["nexts"]:
                    if next_id in node_map:
                        destination_node = node_map[next_id]
                        edge_tuple = (source_node.data.uniq_id, destination_node.data.uniq_id)
                        if edge_tuple not in edge_set:
                            edge = Edge(source_node.output_port)
                            edge.set_destination(destination_node.input_port)
                            scene.addItem(edge)
                            source_node.output_port.edges.append(edge)
                            destination_node.input_port.edges.append(edge)
                            edge_set.add(edge_tuple)

            # Ensure edges are properly connected and update their positions
            for node in node_map.values():
                for edge in node.input_port.edges + node.output_port.edges:
                    edge.update_position()
