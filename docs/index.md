# On-Call Support Agent Workflow


```mermaid
graph TD
  router([Decide Action])
  route([Route to Codeowners])
  runbook([Search Runbooks])
  knowledge([Search Knowledge Base])
  router -->|route| route
  router -->|runbook| runbook
  router -->|knowledge| knowledge
