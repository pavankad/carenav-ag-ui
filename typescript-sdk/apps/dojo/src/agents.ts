import "server-only";
import { AgentIntegrationConfig } from "./types/integration";
import { OpenAIServerAgent } from "@ag-ui/openai-server";

export const agentsIntegrations: AgentIntegrationConfig[] = [
  {
    id: "openai-server",
    agents: async () => {
      return {
        agentic_chat: new OpenAIServerAgent(
        {url:"http://localhost:8000/"}
        )
      }
    },
  },
];
