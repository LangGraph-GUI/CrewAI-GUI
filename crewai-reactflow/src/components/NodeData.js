// nodeData.js
class NodeData {
    constructor(
      uniq_id,
      type = "",
      pos_x = 0.0,
      pos_y = 0.0,
      width = 200.0,
      height = 200.0,
      name = "",
      role = "",
      goal = "",
      backstory = "",
      agent = "",
      description = "",
      expected_output = "",
      tool = "",
      arg = "",
      output_var = "",
      nexts = [],
      prevs = []
    ) {
      this.uniq_id = uniq_id;
      this.type = type;
      this.pos_x = pos_x;
      this.pos_y = pos_y;
      this.width = width;
      this.height = height;
      this.name = name;
      this.role = role;
      this.goal = goal;
      this.backstory = backstory;
      this.agent = agent;
      this.description = description;
      this.expected_output = expected_output;
      this.tool = tool;
      this.arg = arg;
      this.output_var = output_var;
      this.nexts = nexts;
      this.prevs = prevs;
    }
  
    toDict() {
      return { ...this };
    }
  
    static fromDict(data) {
      return new NodeData(
        data.uniq_id,
        data.type,
        data.pos_x,
        data.pos_y,
        data.width,
        data.height,
        data.name,
        data.role,
        data.goal,
        data.backstory,
        data.agent,
        data.description,
        data.expected_output,
        data.tool,
        data.arg,
        data.output_var,
        data.nexts,
        data.prevs
      );
    }
  }
  
  export default NodeData;
  