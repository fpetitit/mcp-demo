from fastapi import FastAPI

app = FastAPI(title="MCP Demo")

@app.get("/")
async def root():
    return {"message": "MCP fonctionne sur Vercel!"}

@app.get("/health")
async def health():
    return {"status": "OK"}
