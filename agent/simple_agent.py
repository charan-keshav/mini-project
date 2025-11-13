from google.adk.agents import LlmAgent
from agent.simple_tools import get_inventory, count_items, check_stock
from constants import AGENT_NAME, AGENT_DESCRIPTION, AGENT_MODEL

simple_agent = LlmAgent(
    name=AGENT_NAME,
    model=AGENT_MODEL,
    description=AGENT_DESCRIPTION,
    instruction="You are an inventory assistant. Help users with inventory queries.",
    tools=[get_inventory, count_items, check_stock]
)