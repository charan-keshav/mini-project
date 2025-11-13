from google.adk.agents import LlmAgent
from agent.prompt import *
from agent.tools import *
from constants import AGENT_NAME, AGENT_DESCRIPTION, AGENT_MODEL

root_agent = LlmAgent(
    name=AGENT_NAME,
    model=AGENT_MODEL,
    description=AGENT_DESCRIPTION,
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        get_inventory,
        get_items_by_category,
        get_items_needing_reorder,
        check_item_stock,
        update_item_quantity,
        remove_item,
        add_sample_inventory_data,
        get_inventory_count,
        get_total_stock_value,
        get_top_supplier,
        get_last_updated_item,
        get_items_not_updated_6_months,
        get_category_highest_avg_price,
        create_supplier_model,
        get_supplier_lowest_reorder_frequency,
        get_supplier_highest_category_cost
    ]
)