import streamlit as st
from langraph_backend_database import chatbot,retrive_all_thread
from langchain_core.messages import HumanMessage
import uuid
import os

# =========================
# Utility functions
# =========================

os.environ['LANGCHAIN_PROJECT']='chatbot'

def genrate_thread_id():
    # Generate a unique thread ID for each chat session.
    thread_id = uuid.uuid4()
    return thread_id


def add_thread(thread_id):
    # Add thread ID to sidebar list only if it is new.
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def reset_chat():
    # Create a new thread and clear current chat history.
    thread_id = genrate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []


def load_conversation(thread_id):
    state_snapshot = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    if not state_snapshot or not state_snapshot.values:
        return []
    return state_snapshot.values.get('messages', [])


# =========================
# Session state initialization
# =========================

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = genrate_thread_id()

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all_thread()

add_thread(st.session_state['thread_id'])

# CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}


CONFIG = {
    "configurable": {"thread_id": st.session_state["thread_id"]},
    "metadata": {
        "thread_id": st.session_state["thread_id"]
    },
    "run_name": "chat_turn",
}


# =========================
# Main chat window
# =========================

# Display chat history first.
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


# =========================
# Sidebar
# =========================

st.sidebar.title('MychatBot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('Myconversation')

for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']= thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]

        for message in messages:
            if  isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':message.content})
        
        st.session_state['message_history']=temp_messages



# =========================
# User input + assistant response
# =========================

user_input = st.chat_input("Type Here")

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    with st.chat_message('user'):
        st.text(user_input)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})