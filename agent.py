from langgraph.graph import StateGraph
from tools.route_tool import RouteTool
from tools.runbook_search import RunbookSearchTool
from tools.knowledge_base import KnowledgeBaseTool
from tools.llm_tool import LLMTool
from typing import TypedDict


class AgentState(TypedDict):
    error: str
    file: str
    action_taken: str


class OnCallSupportAgent:

    def __init__(self):
        self.route_tool = RouteTool()
        self.runbook_tool = RunbookSearchTool()
        self.knowledge_tool = KnowledgeBaseTool()
        self.llm_tool = LLMTool()

    def decide_action(self, state):
        print(f"Entering decide_action router. State: {state}")
        decision = self.llm_tool.decide_next_steps(state)
        new_state = {**state, "decision": decision}
        print(f"Exiting decide_action router. State: {new_state}")
        return new_state

    def route_to_codeowners(self, state):
        print(f"Entering route_to_codeowners tool. State: {state}")
        file = state["file"]
        code_owner = self.route_tool.get_code_owner(file)
        new_state = {**state, "action_taken": f"Routed to {code_owner}"}
        print(f"Exiting route_to_codeowners tool. State: {new_state}")
        return new_state

    def search_runbooks(self, state):
        print(f"Entering search_runbooks tool. State: {state}")
        result = self.runbook_tool.search_runbooks(state["error"])
        new_state = {**state, "action_taken": result}
        print(f"Exiting search_runbooks tool. State: {new_state}")
        return new_state

    def search_kb(self, state):
        print(f"Entering search_kb tool. State: {state}")
        result = self.knowledge_tool.knowledge_base_search(state["error"])
        new_state = {**state, "action_taken": result}
        print(f"Exiting search_kb tool. State: {new_state}")
        return new_state


def build_workflow():
    agent = OnCallSupportAgent()
    builder = StateGraph(state_schema=AgentState)
    builder.add_node("router", agent.decide_action)
    builder.add_node("route", agent.route_to_codeowners)
    builder.add_node("runbook", agent.search_runbooks)
    builder.add_node("knowledge", agent.search_kb)
    builder.set_entry_point("router")
    builder.add_conditional_edges("router", lambda state: state["decision"], {
        "route": "route",
        "runbook": "runbook",
        "knowledge": "knowledge"
    })
    builder.set_finish_point("route")
    builder.set_finish_point("runbook")
    builder.set_finish_point("knowledge")
    app = builder.compile()

    return app
