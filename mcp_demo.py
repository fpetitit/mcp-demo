from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Dict, Any, List
import json

app = FastAPI(title="MCP Demo Viry")

class ToolSchema(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPSchema(BaseModel):
    name: str = "Viry Entreprises MCP"
    description: str = "Démo MCP secteur public"
    tools: List[ToolSchema] = []

@app.get("/.well-known/mcp.json")
async def mcp_schema():
    return MCPSchema(
        tools=[
            ToolSchema(
                name="trouver_entreprise",
                description="Recherche entreprise à Viry-Châtillon",
                inputSchema={
                    "type": "object",
                    "properties": {"nom": {"type": "string", "description": "Nom entreprise"}},
                    "required": ["nom"]
                }
            )
        ]
    )

@app.post("/tools/trouver_entreprise")
async def trouver_entreprise(body: Dict = Body(...)):
    nom = body.get("nom", "inconnu")
    return {
        "result": f"✅ Entreprise '{nom}' trouvée ! SIRET: 12345678900012",
        "adresse": "1 Rue de la Paix, 91140 Viry-Châtillon"
    }

@app.get("/")
async def root():
    return {"message": "🚀 Serveur MCP prêt ! Testez /.well-known/mcp.json"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
