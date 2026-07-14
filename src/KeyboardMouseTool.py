"""
Keyboard and mouse control tool for CrewAI agents.

WARNING: This tool can physically control the user's input devices.
Use only in controlled environments and with explicit user approval.
"""

import pyautogui
import time
from crewai.tools import BaseTool  # type: ignore[import-untyped]
from typing import Optional


class KeyboardMouseTool(BaseTool):
    """Control keyboard and mouse, and take screenshots.

    This tool requires **explicit user approval** before execution.
    It is disabled by default and must be enabled via the GUI.
    """

    name: str = "KeyboardMouseTool"
    description: str = (
        "A tool for keyboard and mouse control, as well as taking screenshots. "
        "IMPORTANT: This requires explicit user approval. "
        "Never use this without asking the user first."
    )

    # Flag to require user confirmation before any action.
    # Set to False only if you have explicitly confirmed with the user.
    _enabled: bool = False

    def _run(self, action: str, params: Optional[dict] = None) -> str:
        if not self._enabled:
            return (
                "KeyboardMouseTool is disabled by default for safety. "
                "Enable it in the agent settings if you trust the agent."
            )

        actions = {
            "type": self._do_type,
            "click": self._do_click,
            "move": self._do_move,
            "screenshot": self._do_screenshot,
        }

        handler = actions.get(action)
        if handler is None:
            return "Invalid action. Supported: type, click, move, screenshot."
        return handler(params or {})

    def _do_type(self, params: dict) -> str:
        text = params.get("text", "")
        pyautogui.typewrite(text)
        return f"Typed: {text}"

    def _do_click(self, params: dict) -> str:
        x = params.get("x")
        y = params.get("y")
        if x is not None and y is not None:
            pyautogui.click(x, y)
            return f"Clicked at ({x}, {y})"
        pyautogui.click()
        return "Clicked at current position"

    def _do_move(self, params: dict) -> str:
        x = params.get("x")
        y = params.get("y")
        if x is None or y is None:
            return "Error: x and y coordinates required."
        pyautogui.moveTo(x, y)
        return f"Moved to ({x}, {y})"

    def _do_screenshot(self, params: dict) -> str:
        filename = params.get("filename", "screenshot.png")
        folder = params.get("folder", ".")
        path = f"{folder}/{filename}"
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        return f"Screenshot saved as {path}"

    def _arun(self, action: str, params: Optional[dict] = None) -> str:
        """Async wrapper — adds a small delay, then calls ``_run``."""
        time.sleep(0.1)
        return self._run(action, params)
