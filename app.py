import streamlit as st
from dotenv import load_dotenv
from data_connector import get_conn, init_db, create_chat, get_chats, get_messages, add_message
from llm_utils import build_chain, format_history
from chathistory_sidebar import group_chats_by_time

load_dotenv()

# Streamlit UI

st.set_page_config(page_title="AI Stock Recommender - POC")
st.title("💬 Investment Recommender")

# Init DB
init_db()

# Radio (frontend control)
mode = st.sidebar.radio(
    "Assistant mode",
    ["General", "Industry"],
    index=0,
)

# Decide current chat once
if "current_chat_id" not in st.session_state:
    chats = get_chats()
    if chats:
        st.session_state.current_chat_id = chats[0][0]  # most recent
    else:
        st.session_state.current_chat_id = create_chat("Chat 1")

current_chat_id = st.session_state.current_chat_id

# New chat button
if st.sidebar.button("🆕 New chat", use_container_width=True):
    new_id = create_chat(f"Chat {len(get_chats()) + 1}")
    st.session_state.current_chat_id = new_id
    st.rerun()

# Fetch all chats and group them
chats = get_chats()  # [(id, name, created_at), ...]
grouped = group_chats_by_time(chats)

st.sidebar.markdown("### Conversations")

# This automatically becomes scrollable when tall enough
for section_name in ["Today", "This week", "This month", "Older"]:
    section_chats = grouped[section_name]
    if not section_chats:
        continue

    st.sidebar.markdown(f"**{section_name}**")

    for chat_id, name, created_dt in section_chats:
        # Label can be more advanced later; for now, use name
        label = name or created_dt.strftime("%H:%M")

        # Mark the active chat visually
        if chat_id == current_chat_id:
            label_display = f"• {label}"
        else:
            label_display = label

        if st.sidebar.button(
            label_display,
            key=f"chat-{chat_id}",
            use_container_width=True,
        ):
            st.session_state.current_chat_id = chat_id
            st.rerun()

current_chat_id = st.session_state.current_chat_id

# Load messages for current chat from DB
messages = get_messages(current_chat_id)
st.session_state.messages = messages

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message")

if user_input:
    # Save user message
    add_message(current_chat_id, "user", user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # History text for model
    history_text = format_history(st.session_state.messages)

    # Build chain and call LLM
    chain = build_chain(mode)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")
        response = chain.invoke(
            {"history": history_text, "user_input": user_input}
        )
        placeholder.markdown(response)

    # Save assistant message
    add_message(current_chat_id, "assistant", response)
    st.session_state.messages.append({"role": "assistant", "content": response})