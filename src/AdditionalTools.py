"""
Potentially dangerous tool wrappers for CrewAI.

These tools can interact with the local system. Use with care.
"""

import os
import requests
import subprocess
import logging
from crewai.tools import BaseTool  # type: ignore[import-untyped]
from typing import Optional

logger = logging.getLogger(__name__)

# Commands that are NEVER allowed regardless of context.
DENIED_COMMANDS = [
    "rm -rf /",
    "rm -rf ~",
    "dd if=",
    "mkfs.",
    "fdisk",
    "> /dev/",
    "chmod 777 /",
    "wget ",  # remote downloads — handled by restricted network
    "curl ",  # same
]

# Allowed command prefixes for ``SystemCommandTool``.
SAFE_PREFIXES = [
    "ls",
    "cat",
    "echo",
    "head",
    "tail",
    "grep",
    "wc",
    "find",
    "pwd",
    "whoami",
    "date",
    "uname",
    "df",
    "du",
    "ps aux",
    "which",
    "python3 --version",
    "pip list",
]


class WebRequestTool(BaseTool):
    """Make HTTP requests to external URLs."""

    name: str = "WebRequestTool"
    description: str = (
        "A tool for making web requests and fetching content from URLs. "
        "Only accessible to admin-level agents."
    )

    def _run(self, url: str, method: str = "GET", params: Optional[dict] = None) -> str:
        try:
            response = requests.request(method, url, params=params, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            return f"Error making request: {str(e)}"


class FileOperationTool(BaseTool):
    """Read from and write to local files."""

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
                # Safety: prevent write outside project directory
                allowed = os.path.abspath(path).startswith(os.getcwd())
                if not allowed:
                    return "Error: writing to paths outside the working directory is not allowed."
                with open(path, 'w') as file:
                    if content is not None:
                        file.write(content)
                return f"Successfully wrote to {path}"
            except IOError as e:
                return f"Error writing to file: {str(e)}"
        else:
            return "Invalid action. Supported actions are 'read' and 'write'."


class SystemCommandTool(BaseTool):
    """Execute safe system commands. Denied and unknown commands are blocked."""

    name: str = "SystemCommandTool"
    description: str = (
        "A tool for executing safe system commands. "
        "Only read-only commands are allowed (ls, cat, echo, pwd, etc.). "
        "Destructive or unknown commands are blocked."
    )

    @staticmethod
    def _is_safe(command: str) -> bool:
        stripped = command.strip()
        # Block denied patterns first
        for denied in DENIED_COMMANDS:
            if denied in stripped:
                return False
        # Allow only known safe prefixes
        for prefix in SAFE_PREFIXES:
            if stripped.startswith(prefix):
                return True
        return False

    def _run(self, command: str) -> str:
        if not self._is_safe(command):
            logger.warning("Blocked unsafe command: %s", command)
            return (
                f"Error: command '{command}' is not in the allowed list. "
                f"Allowed: {', '.join(SAFE_PREFIXES)}"
            )
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {str(e)}"
        except subprocess.TimeoutExpired:
            return "Error: command timed out after 30 seconds"
