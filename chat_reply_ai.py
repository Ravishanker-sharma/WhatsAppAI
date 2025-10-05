import asyncio
from langgraph.graph import StateGraph, add_messages
from typing import Annotated, TypedDict
from langgraph.prebuilt import tools_condition, ToolNode
from scraper import get_data
from langchain.agents import Tool
from langgraph.checkpoint.memory import MemorySaver
from config import llm

memory = MemorySaver()

class Agent_state(TypedDict):
    messages: Annotated[list, add_messages]


async def build_app():
    # Local tools
    tools = [
        Tool(
            name="GetData",
            func=get_data,
            description="Performs a websearch on basis of input and return data."
        )
    ]

    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)

    def chat_bot(state: Agent_state):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph = StateGraph(Agent_state)
    graph.add_node("bot", chat_bot)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("bot")
    graph.add_conditional_edges("bot", tools_condition)
    graph.add_edge("tools", "bot")

    app = graph.compile(checkpointer=memory)
    return app

intialized_threads = set()


async def bot(app, message, thread_id="1"):
    if thread_id not in intialized_threads:
        prompt = '''
        You are a Whatsapp AI assistant , you have to reply on behalf of me.
        '''
        msg = {"messages": [{"role": "system", "content": prompt},
                            {"role": "user", "content": message}]}
        intialized_threads.add(thread_id)
    else:
        msg = {"messages": [{"role": "user", "content": message}]}

    config1 = {"configurable": {"thread_id": thread_id}}
    output = app.invoke(msg, config=config1)
    return output['messages'][-1].content


async def main():
    app = await build_app()
    response = await bot(app, "get me details about my calander , use my primary id only ")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
