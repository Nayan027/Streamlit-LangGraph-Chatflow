import streamlit as st
from langchain_core.messages import HumanMessage

from backend import chatbot                           # importing out chatbot we made

CONFIG = {"configurable":{"thread_id":"1"}}



st.title("Your Personalized Chatbot powered by Perplexity")

if "msg_history" not in st.session_state:
    st.session_state["msg_history"] = []             # a session i.e. a dictionary created, key - msg_history
                                                    
# this list will consist of dicts in form of:
#                    {"role": 'user', "content": 'user query'}
#                    {"role": 'assistant', "content": 'llm response to query'}


for msg in st.session_state['msg_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])




user_input = st.chat_input("Ask your chatbot")

if user_input:                                                           # meaning when user hits "Enter" button.
    st.session_state["msg_history"].append({"role":"user",               # adding the user message to message_history
                                            "content":user_input})
    with st.chat_message("user"):                                        # opens a chat bubble for user test
        st.text(user_input)                                              # the actual text is filled in that chat-bubble




    streamed_response = chatbot.stream(
                {"messages": HumanMessage(user_input)},
                config = CONFIG,
                stream_mode = "messages"
            )

    with st.chat_message("assistant"):
        chatbot_response = st.write_stream(                                # streaming handles the display.
            chunk.content for chunk, metadata in streamed_response         # Collect chunks as they are streamed
            )

    st.session_state["msg_history"].append({"role":"assistant",            # add the ai message to message_history
                                           "content":chatbot_response})
    


# NOTE: st.write_stream() expects a  Generator/LangChain Stream/etc. 