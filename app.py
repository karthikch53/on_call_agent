from fastapi import FastAPI, Request, Response, status
from agent import build_workflow
import uvicorn

app = FastAPI()

workflow = build_workflow()


@app.get("/health")
def health():
    return Response(status_code=status.HTTP_200_OK)


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    state = {
        "file": body.get("file", ""),
        "error": body.get("error", "")
    }
    result = workflow.invoke(state)
    return {"action_taken": result.get("action_taken")}


if __name__ == "__main__":
    uvicorn.run("workflow:app", host="0.0.0.0", port=8000, reload=True)
