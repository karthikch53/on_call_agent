import requests

from tools.knowledge_base import KnowledgeBaseTool
from tools.runbook_search import RunbookSearchTool


class LLMTool:

    def __init__(self):
        self.runbook_tool = RunbookSearchTool()
        self.knowledge_tool = KnowledgeBaseTool()

    def decide_next_steps(self, state) -> str:
        url = "http://localhost:11434/api/generate"

        runbook_hits = self.runbook_tool.search_runbooks(state['error'])

        for rb in runbook_hits:
            print(rb)

        kb_hits = self.knowledge_tool.knowledge_base_search(state['error'])

        for kb in kb_hits:
            print(kb)

        prompt = f"""
        You are an on-call AI assistant. Here's an error:

        ```
        Error: {state['error']}
        
        Top Runbook Matches:
        {runbook_hits or 'None'}

        Top Knowledge Base Matches:
        {kb_hits or 'None'}
        
        ```

        Based on the error and file `{state['file']}`, decide what to do:
        - Return route if this clearly belongs to a specific code owner
        - Return runbook if it looks like a known issue with remediation steps
        - Return knowledge if it needs deeper investigation or past incident context
        
        Return your response in the following format:
        
        <decision> | <brief explanation>
        
        Where:
        - <decision> is one of route or runbook or knowledge 
        - <brief explanation> is 1-2 sentences explaining why you chose that action
        
        """

        payload = {
            "stream": False,
            "model": "gemma3:12b",
            "prompt": prompt
        }

        api_response = requests.post(url, json=payload)
        api_response_json = api_response.json()
        chat_response = api_response_json['response']
        chat_response_parts = chat_response.split("|")
        default_decision = "knowledge"
        if len(chat_response_parts) > 1:
            default_decision = chat_response_parts[0].strip()
        return default_decision


if __name__ == '__main__':
    llm = LLMTool()
    decision, reason = llm.decide_next_steps("KeyError: \'Michael\'")
