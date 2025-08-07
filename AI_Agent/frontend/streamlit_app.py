import streamlit as st
import requests
import time

# Backend URLs (your FastAPI Gemini backend)
BACKEND_URL = "http://127.0.0.1:8000/chat"
TRANSCRIBE_URL = "http://127.0.0.1:8000/transcribe"

# Page config
st.set_page_config(page_title="AI Agent", layout="centered")
st.title("🤖 Gemini 2.5 Pro AI Assistant")
st.markdown("Chat with your AI assistant using **text or voice**. Powered by Gemini 2.5 Pro & ChromaDB.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a container for the chat input area
with st.container():
    # Use columns to place the mic button next to the chat input
    col1, col2 = st.columns([0.9, 0.1])
    
    # Accept user input via text
    with col1:
        user_input = st.chat_input("💬 Type your message...")
    
    # Voice recording button (placed beside the chat input)
    with col2:
        voice_button = st.button("🎤", key="voice_button")

# Handle voice input
if voice_button:
    with st.spinner("🎤 Recording... (5 seconds)"):
        try:
            response = requests.post(TRANSCRIBE_URL)
            if response.status_code == 200:
                transcription = response.json().get("text", "").strip()
                if transcription:
                    # Display user message in chat container
                    with st.chat_message("user"):
                        st.markdown(f"🎤 {transcription}")
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": f"🎤 {transcription}"})
                    
                    # Process with backend
                    with st.spinner("Thinking..."):
                        response = requests.post(BACKEND_URL, json={"message": transcription})
                        
                    if response.status_code == 200:
                        try:
                            ai_response = response.json()["response"]
                            # Display assistant response in chat container
                            with st.chat_message("assistant"):
                                st.markdown(ai_response)
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        except Exception as e:
                            st.error(f"❗ Error parsing response: {str(e)}")
                            st.error("The backend server might be experiencing issues.")
                    else:
                        st.error(f"❗ Server returned status code: {response.status_code}")
                        st.error("The backend server might be experiencing issues.")
                else:
                    st.warning("No speech detected. Please try again.")
            else:
                st.error(f"❗ Server returned status code: {response.status_code}")
                st.error("The backend server might be experiencing issues with voice transcription.")
        except requests.exceptions.ConnectionError:
            st.error("❗ Could not connect to the backend server. Make sure it's running.")
        except Exception as e:
            st.error(f"❗ Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# Handle text input
elif user_input:
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process with backend
    try:
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_URL, json={"message": user_input})
            
        if response.status_code == 200:
            try:
                ai_response = response.json()["response"]
                # Display assistant response in chat container
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"❗ Error parsing response: {str(e)}")
                st.error("The backend server might be experiencing issues.")
        else:
            st.error(f"❗ Server returned status code: {response.status_code}")
            st.error("The backend server might be experiencing issues.")
    except requests.exceptions.ConnectionError:
        st.error("❗ Could not connect to the backend server. Make sure it's running.")
    except Exception as e:
        st.error(f"❗ Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.caption("© 2023 AI Agent - Powered by Gemini 2.5 Pro with Voice Recognition")

# Add some CSS to make it look more like a chatbox
st.markdown("""
<style>
div.stChatMessage {
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 10px;
}
div.stChatMessage[data-testid="stChatMessage-user"] {
    background-color: #e6f7ff;
    border: 1px solid #91d5ff;
}
div.stChatMessage[data-testid="stChatMessage-assistant"] {
    background-color: #f6ffed;
    border: 1px solid #b7eb8f;
}
</style>
""", unsafe_allow_html=True)