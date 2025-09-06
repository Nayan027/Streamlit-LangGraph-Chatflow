from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import InMemorySaver
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langchain_perplexity import ChatPerplexity

from dotenv import load_dotenv
load_dotenv()



model = ChatPerplexity()                 # LLModel instance 

checkpointer = InMemorySaver()           # Memory saver object

class ChatState(TypedDict):              # Defining state
    messages: Annotated[list[BaseMessage], add_messages]




def chat_node(state:ChatState):         # Define the only task
    messages = state['messages']

    llm_response = model.invoke(messages)

    return {"messages": llm_response}




graph = StateGraph(ChatState)           # Graph - workflow

graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)