"""Tests for backend modules that don't require a Qt display."""

import json
import os
import tempfile
import pytest
from NodeData import NodeData
from AdditionalTools import WebRequestTool, FileOperationTool, SystemCommandTool

# ── NodeData ─────────────────────────────────────────────────────────────────

class TestNodeData:
    def test_defaults(self):
        n = NodeData()
        assert n.type == ""
        assert n.tools == []
        assert n.width == 200.0
        assert n.height == 200.0

    def test_to_dict_roundtrip(self):
        n = NodeData(
            type="Agent",
            uniq_id="abc123",
            name="test-agent",
            role="Helper",
            goal="Help",
            backstory="A helpful agent",
            tools=["WebRequestTool"],
        )
        d = n.to_dict()
        assert d["type"] == "Agent"
        assert d["name"] == "test-agent"
        assert d["tools"] == ["WebRequestTool"]

        restored = NodeData.from_dict(d)
        assert restored.type == "Agent"
        assert restored.name == "test-agent"
        assert restored.uniq_id == "abc123"
        assert restored.tools == ["WebRequestTool"]
        assert restored.role == "Helper"

    def test_position(self):
        n = NodeData(pos_x=42.5, pos_y=13.7)
        assert n.pos_x == 42.5
        assert n.pos_y == 13.7

    def test_nexts_prevs(self):
        n = NodeData(nexts=["b", "c"], prevs=["a"])
        assert n.nexts == ["b", "c"]
        assert n.prevs == ["a"]

    def test_from_dict_full(self):
        raw = {
            "type": "Task",
            "uniq_id": "task1",
            "name": "My Task",
            "description": "Do the thing",
            "expected_output": "Done",
            "agent": "helper-agent",
            "tools": [],
            "nexts": [],
            "prevs": [],
            "pos_x": 100.0,
            "pos_y": 200.0,
            "width": 250.0,
            "height": 180.0,
        }
        n = NodeData.from_dict(raw)
        assert n.type == "Task"
        assert n.description == "Do the thing"
        assert n.expected_output == "Done"
        assert n.width == 250.0
        assert n.height == 180.0


# ── WorkFlow helpers ─────────────────────────────────────────────────────────

from WorkFlow import load_nodes_from_json, find_nodes_by_type, find_node_by_type

class TestWorkFlow:
    def test_load_nodes_from_json(self):
        data = {
            "nodes": [
                {
                    "type": "Start",
                    "uniq_id": "start1",
                    "name": "Start",
                    "tools": [],
                    "nexts": ["team1"],
                    "prevs": [],
                    "pos_x": 0.0,
                    "pos_y": 0.0,
                    "width": 200.0,
                    "height": 200.0,
                },
                {
                    "type": "Team",
                    "uniq_id": "team1",
                    "name": "MyTeam",
                    "tools": [],
                    "nexts": [],
                    "prevs": ["start1"],
                    "pos_x": 300.0,
                    "pos_y": 0.0,
                    "width": 200.0,
                    "height": 200.0,
                },
            ]
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name
        try:
            node_map = load_nodes_from_json(path)
            assert len(node_map) == 2
            assert "start1" in node_map
            assert "team1" in node_map
            assert node_map["start1"].type == "Start"
            assert node_map["team1"].name == "MyTeam"
        finally:
            os.unlink(path)

    def test_find_nodes_by_type(self):
        n1 = NodeData(type="Agent", uniq_id="a1", name="Alpha")
        n2 = NodeData(type="Task", uniq_id="t1", name="Task1")
        n3 = NodeData(type="Agent", uniq_id="a2", name="Beta")
        node_map = {"a1": n1, "t1": n2, "a2": n3}
        agents = find_nodes_by_type(node_map, "Agent")
        assert len(agents) == 2
        assert agents[0].name == "Alpha"
        assert agents[1].name == "Beta"

    def test_find_node_by_type(self):
        n1 = NodeData(type="Start", uniq_id="s1")
        n2 = NodeData(type="Team", uniq_id="tm1")
        node_map = {"s1": n1, "tm1": n2}
        team = find_node_by_type(node_map, "Team")
        assert team is not None
        assert team.uniq_id == "tm1"
        not_found = find_node_by_type(node_map, "Agent")
        assert not_found is None


# ── Topological sort ─────────────────────────────────────────────────────────

from WorkFlow import topological_sort_tasks

class TestTopologicalSort:
    def test_simple_chain(self):
        t1 = NodeData(uniq_id="t1", prevs=[], nexts=["t2"], type="Task", name="1")
        t2 = NodeData(uniq_id="t2", prevs=["t1"], nexts=["t3"], type="Task", name="2")
        t3 = NodeData(uniq_id="t3", prevs=["t2"], nexts=[], type="Task", name="3")
        ids = [n.uniq_id for n in topological_sort_tasks([t3, t1, t2])]
        assert ids == ["t1", "t2", "t3"], f"got {ids}"

    def test_diamond(self):
        t1 = NodeData(uniq_id="s", prevs=[], nexts=["a", "b"], type="Task")
        ta = NodeData(uniq_id="a", prevs=["s"], nexts=["e"], type="Task")
        tb = NodeData(uniq_id="b", prevs=["s"], nexts=["e"], type="Task")
        te = NodeData(uniq_id="e", prevs=["a", "b"], nexts=[], type="Task")
        sorted_ids = [n.uniq_id for n in topological_sort_tasks([te, tb, ta, t1])]
        assert sorted_ids[0] == "s"
        assert sorted_ids[-1] == "e"
        # a and b order doesn't matter, but both must come before e
        assert sorted_ids.index("a") < sorted_ids.index("e")
        assert sorted_ids.index("b") < sorted_ids.index("e")

    def test_single_node(self):
        n = NodeData(uniq_id="only", prevs=[], nexts=[], type="Task")
        assert [n.uniq_id for n in topological_sort_tasks([n])] == ["only"]


# ── SystemCommandTool safety ─────────────────────────────────────────────────

class TestSystemCommandTool:
    def setup_method(self):
        self.tool = SystemCommandTool()

    def test_safe_ls(self):
        result = self.tool._run("ls")
        # should succeed or return "Error: ..." (varies by env)
        assert not result.startswith("Error: command 'ls' is not in the allowed list")

    def test_safe_echo(self):
        result = self.tool._run("echo hello")
        assert "hello" in result

    def test_blocked_rm_rf(self):
        result = self.tool._run("rm -rf /")
        assert "not in the allowed list" in result

    def test_blocked_dd(self):
        result = self.tool._run("dd if=/dev/zero of=/dev/null")
        assert "not in the allowed list" in result

    def test_unknown_command_blocked(self):
        result = self.tool._run("some_evil_script.sh")
        assert "not in the allowed list" in result


# ── FileOperationTool path safety ────────────────────────────────────────────

class TestFileOperationTool:
    def setup_method(self):
        self.tool = FileOperationTool()

    def test_write_read_roundtrip(self):
        path = f"{os.getcwd()}/_test_write.txt"
        try:
            write = self.tool._run("write", path, content="hello world")
            assert "Successfully" in write
            read = self.tool._run("read", path)
            assert read == "hello world"
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_block_outside_cwd(self):
        result = self.tool._run("write", "/tmp/evil.txt", content="bad")
        assert "not allowed" in result

    def test_invalid_action(self):
        result = self.tool._run("delete", "/tmp/x")
        assert "Invalid action" in result


# ── WebRequestTool ───────────────────────────────────────────────────────────

class TestWebRequestTool:
    def setup_method(self):
        self.tool = WebRequestTool()

    def test_bad_url_returns_error(self):
        result = self.tool._run("https://nonexistent.example.test/foo")
        assert result.startswith("Error")
