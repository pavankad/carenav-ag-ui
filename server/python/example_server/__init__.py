"""
Example server for the AG-UI protocol.
"""

import os
import uvicorn
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from ag_ui.core import (
    RunAgentInput,
    EventType,
    RunStartedEvent,
    RunFinishedEvent,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
)
from ag_ui.encoder import EventEncoder

# MCP
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI, AzureChatOpenAI, OpenAI
from langgraph.prebuilt import create_react_agent
import asyncio
import pdb

app = FastAPI(title="AG-UI Endpoint")


# from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# # Get Azure token
# default_credential = DefaultAzureCredential()
# access_token = default_credential.get_token("https://cognitiveservices.azure.com/.default")

# # Set API key from the access token
# os.environ['OPENAI_API_KEY'] = access_token.token
# os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://api.uhg.com/api/cloud/api-management/ai-gateway/1.0'
# # Define the MCP server URL
# MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"

# # Initialize model with Azure-specific parameters
# model = AzureChatOpenAI(
#     azure_deployment="gpt-4o_2024-05-13",  # The deployment name in Azure
#     api_version="2025-01-01-preview",  # Azure API version
#     default_headers={
#         "projectId": "f440d3f1-df7a-45fb-a62f-5953aaf6bd55",
#         "x-idp": "azuread"
#     }
# )
os.environ['OPENAI_API_KEY'] = ""
model = ChatOpenAI(api_key=os.environ['OPENAI_API_KEY'], model_name="gpt-4o", temperature=0.7)


@app.post("/")
async def agentic_chat_endpoint(input_data: RunAgentInput, request: Request):
    """Agentic chat endpoint"""
    # Get the accept header from the request
    accept_header = request.headers.get("accept")
    pdb.set_trace()

    # Create an event encoder to properly format SSE events
    encoder = EventEncoder(accept=accept_header)

    async def event_generator():

        # Send run started event
        yield encoder.encode(
          RunStartedEvent(
            type=EventType.RUN_STARTED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id
          ),
        )

        message_id = str(uuid.uuid4())

        yield encoder.encode(
            TextMessageStartEvent(
                type=EventType.TEXT_MESSAGE_START,
                message_id=message_id,
                role="assistant"
            )
        )

        """Main function to process queries using the MCP client."""
        async def mcp_query(query):
            client = MultiServerMCPClient({
                "mcpstore": {
                    "url": "http://127.0.0.1:8001/mcp",  # Replace with the remote server's URL
                    "transport": "streamable_http"
                }
            })
            tools = await client.get_tools()
            pdb.set_trace()
            agent = create_react_agent(model, tools)
            response = await agent.ainvoke({"messages": input_data.messages[1].content})
            return response

        result = await mcp_query(input_data.messages)

        yield encoder.encode(
            TextMessageContentEvent(
                type=EventType.TEXT_MESSAGE_CONTENT,
                message_id=message_id,
                delta=result
            )
        )

        yield encoder.encode(
            TextMessageEndEvent(
                type=EventType.TEXT_MESSAGE_END,
                message_id=message_id
            )
        )

        # Send run finished event
        yield encoder.encode(
          RunFinishedEvent(
            type=EventType.RUN_FINISHED,
            thread_id=input_data.thread_id,
            run_id=input_data.run_id
          ),
        )

    return StreamingResponse(
        event_generator(),
        media_type=encoder.get_content_type()
    )

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "example_server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
