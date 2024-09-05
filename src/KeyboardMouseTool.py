import pyautogui
import time
from crewai_tools import BaseTool
from typing import Optional

class KeyboardMouseTool(BaseTool):
    name: str = "KeyboardMouseTool"
    description: str = "A tool for keyboard and mouse control, as well as taking screenshots."

    def _run(self, action: str, params: Optional[dict] = None) -> str:
        if action == "type":
            text = params.get("text", "")
            pyautogui.typewrite(text)
            return f"Typed: {text}"
        elif action == "click":
            x = params.get("x")
            y = params.get("y")
            if x is not None and y is not None:
                pyautogui.click(x, y)
                return f"Clicked at ({x}, {y})"
            else:
                pyautogui.click()
                return "Clicked at current position"
        elif action == "move":
            x = params.get("x")
            y = params.get("y")
            pyautogui.moveTo(x, y)
            return f"Moved to ({x}, {y})"
        elif action == "screenshot":
            filename = params.get("filename", "screenshot.png")
            folder = params.get("folder", ".")
            path = f"{folder}/{filename}"
            screenshot = pyautogui.screenshot()
            screenshot.save(path)
            return f"Screenshot saved as {path}"
        else:
            return "Invalid action. Supported actions are 'type', 'click', 'move', and 'screenshot'."

    def _arun(self, action: str, params: Optional[dict] = None) -> str:
        # For async operations, you might want to add a small delay
        time.sleep(0.1)
        return self._run(action, params)