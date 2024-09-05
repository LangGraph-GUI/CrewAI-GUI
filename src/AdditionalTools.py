import os
import requests
import subprocess
from crewai_tools import BaseTool
from typing import Optional

class WebRequestTool(BaseTool):
    name: str = "WebRequestTool"
    description: str = "A tool for making web requests and fetching content from URLs."

    def _run(self, url: str, method: str = "GET", params: Optional[dict] = None) -> str:
        try:
            response = requests.request(method, url, params=params)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"Error making request: {str(e)}"

class FileOperationTool(BaseTool):
    name: str = "FileOperationTool"
    description: str = "A tool for reading from and writing to files."

    def _run(self, action: str, path: str, content: Optional[str] = None) -> str:
        if action == "read":
            try:
                with open(path, 'r') as file:
                    return file.read()
            except IOError as e:
                return f"Error reading file: {str(e)}"
        elif action == "write":
            try:
                with open(path, 'w') as file:
                    file.write(content)
                return f"Successfully wrote to {path}"
            except IOError as e:
                return f"Error writing to file: {str(e)}"
        else:
            return "Invalid action. Supported actions are 'read' and 'write'."

class SystemCommandTool(BaseTool):
    name: str = "SystemCommandTool"
    description: str = "A tool for executing system commands."

    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {str(e)}"