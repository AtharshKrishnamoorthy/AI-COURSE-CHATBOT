import streamlit as st
import requests
import json
import time


st.set_page_config(
    page_title="AI Mentor Chatbot",
    page_icon="🤖",
    layout="centered"
)


with st.sidebar:
    st.info("This is a simple chatbot application that uses a backend API to generate responses.")
    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


st.header("AI Mentor Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- API Call ---
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # The URL for the FastAPI endpoint
                api_url = "https://ai-course-chatbot.onrender.com/chat"
                
                # The data to be sent in the POST request
                payload = {"question": prompt}
                
                # Sending the POST request
                response = requests.post(api_url, json=payload)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                api_response_data = response.json()

                if "response" in api_response_data:
                    full_response = api_response_data["response"]
                else:
                    full_response = "Sorry, I couldn't find the response in the expected format."

            except requests.exceptions.RequestException as e:
                full_response = f"Error: Could not connect to the API. {e}"
            except json.JSONDecodeError:
                full_response = "Error: Failed to decode the API response."
            except Exception as e:
                full_response = f"An unexpected error occurred: {e}"

        # Function to generate response word by word
        def stream_response(text):
            for word in text.split(" "):
                yield word + " "
                time.sleep(0.05)

        # Use st.write_stream to display the response with a typewriter effect
        st.write_stream(stream_response(full_response))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
