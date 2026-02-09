#!/usr/bin/env python3
"""
Serveur MCP STDIO pour Claude Desktop
Démo MCP secteur public - Annuaire Entreprises
Implémente le protocole JSON-RPC sur stdin/stdout
"""

import json
import sys
from typing import Dict, Any

class AnnuaireEntreprisesServer:
    def __init__(self):
        self.request_id = 0
        self.protocol_version = "2025-06-18"
        
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Répond à la demande d'initialisation"""
        return {
            "protocolVersion": self.protocol_version,
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "Annuaire Entreprises MCP",
                "version": "1.0.0"
            }
        }

    def handle_list_tools(self) -> Dict[str, Any]:
        """Liste les outils disponibles"""
        return {
            "tools": [
                {
                    "name": "trouver_entreprise",
                    "description": "Recherche une entreprise dans l'annuaire par son nom",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "nom": {
                                "type": "string",
                                "description": "Nom de l'entreprise à rechercher"
                            }
                        },
                        "required": ["nom"]
                    }
                }
            ]
        }

    def handle_call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Exécute un outil"""
        if name == "trouver_entreprise":
            nom = arguments.get("nom", "inconnu")
            result_text = f"✅ Entreprise '{nom}' trouvée ! SIRET: 12345678900012\n"
            result_text += "📍 Adresse: 1 Rue de la Paix, 91140 Viry-Châtillon"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": result_text
                    }
                ]
            }
        else:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Erreur: Outil inconnu '{name}'"
                    }
                ],
                "isError": True
            }

    def send_response(self, request_id: int, result: Dict[str, Any]):
        """Envoie une réponse JSON-RPC"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

    def send_error(self, request_id: int, code: int, message: str):
        """Envoie une erreur JSON-RPC"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

    def process_message(self, data: Dict[str, Any]):
        """Traite un message JSON-RPC reçu"""
        method = data.get("method")
        params = data.get("params", {})
        request_id = data.get("id")

        try:
            if method == "initialize":
                result = self.handle_initialize(params)
                self.send_response(request_id, result)
            
            elif method == "tools/list":
                result = self.handle_list_tools()
                self.send_response(request_id, result)
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.handle_call_tool(tool_name, arguments)
                self.send_response(request_id, result)
            
            else:
                if request_id is not None:
                    self.send_error(request_id, -32601, f"Méthode non trouvée: {method}")
        
        except Exception as e:
            if request_id is not None:
                self.send_error(request_id, -32603, f"Erreur interne: {str(e)}")

    def run(self):
        """Lance le serveur et traite les messages depuis stdin"""
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    self.process_message(data)
                except json.JSONDecodeError as e:
                    print(f"Erreur JSON: {e}", file=sys.stderr)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Erreur serveur: {e}", file=sys.stderr)


if __name__ == "__main__":
    server = AnnuaireEntreprisesServer()
    server.run()
