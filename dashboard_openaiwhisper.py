import streamlit as st
import openai
from openai import OpenAI
import json
import firebase_admin
from firebase_admin import firestore
import pytz
from datetime import datetime
import time
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# Import your existing functions
from calendar_assistant import (
    get_calendar_service, 
    run_assistant_conversation, 
    execute_tool_call, 
    store_thread_id,
    store_message_in_thread
)

class AudioRecorder:
    """Handle audio recording and transcription"""
    @staticmethod
    def record_audio(duration: int = 5) -> Tuple[np.ndarray, int]:
        """Record audio from microphone"""
        sample_rate = 44100
        recording = sd.rec(
            int(duration * sample_rate), 
            samplerate=sample_rate, 
            channels=1, 
            dtype='float32'
        )
        sd.wait()
        return recording, sample_rate

    @staticmethod
    def transcribe_audio(audio_path: str) -> str:
        """Transcribe audio using Whisper API"""
        client = OpenAI()
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text

def load_existing_thread_messages(thread_id: str, user_id: str) -> None:
    """Load and display existing messages for a thread"""
    try:
        db = firestore.client()
        thread_ref = db.collection('Users').document(user_id).collection('Threads').document(thread_id)
        thread_data = thread_ref.get().to_dict()
        
        if thread_data and 'messages' in thread_data:
            for msg in thread_data['messages']:
                st.chat_message(msg['role']).write(msg['content'])
                
    except Exception as e:
        st.error(f"Error loading thread messages: {str(e)}")

def handle_tool_calls(
    run_status: Any, 
    thread_id: str, 
    client: OpenAI,
    calendar_service: Any
) -> None:
    """Handle assistant tool calls"""
    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        try:
            result = execute_tool_call(calendar_service, function_name, function_args)
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(result)
            })
        except Exception as e:
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps({"error": str(e)})
            })
    
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_status.id,
        tool_outputs=tool_outputs
    )

def calendar_assistant_dashboard(user_id: str) -> None:
    """Main dashboard for calendar assistant"""
    st.title("📅 Calendar Assistant")
    
    # Initialize services
    client = OpenAI()
    calendar_service = get_calendar_service()
    
    # Assistant configuration
    assistant_id = "asst_iMA6Il8rSDQl7hsGTO3R0OJY"
    
    # Initialize session state for transcribed text
    if 'transcribed_text' not in st.session_state:
        st.session_state.transcribed_text = ""
    
    # Load existing thread if selected
    if 'current_thread_id' in st.session_state and st.session_state.current_thread_id:
        load_existing_thread_messages(st.session_state.current_thread_id, user_id)
    
    # Create input layout
    input_col, mic_col = st.columns([6, 1])
    
    with input_col:
        # Use transcribed text as initial value if available
        initial_value = st.session_state.transcribed_text if st.session_state.transcribed_text else ""
        user_input = st.text_input(
            "Type your message",
            value=initial_value,
            key="message_input",
            placeholder="Press Enter to send, Shift+Enter for new line"
        )
        # Clear transcribed text after it's used
        st.session_state.transcribed_text = ""
    
    with mic_col:
        if st.button("🎤", help="Click to record voice input"):
            with st.spinner("Recording... Speak now"):
                try:
                    # Record and transcribe audio
                    recorder = AudioRecorder()
                    recording, sample_rate = recorder.record_audio()
                    
                    # Save to temp file
                    temp_dir = Path(tempfile.gettempdir())
                    temp_audio_path = temp_dir / "temp_recording.wav"
                    
                    sf.write(temp_audio_path, recording, sample_rate)
                    transcribed_text = recorder.transcribe_audio(str(temp_audio_path))
                    
                    # Store transcribed text in session state
                    st.session_state.transcribed_text = transcribed_text
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error recording audio: {str(e)}")
    
    # Process input when Enter is pressed or when there's input
    if user_input:
        start_time = time.time()
        
        try:
            # Create or use existing thread
            if 'current_thread_id' not in st.session_state or not st.session_state.current_thread_id:
                thread = client.beta.threads.create()
                st.session_state.current_thread_id = thread.id
                store_thread_id(user_id, thread.id)
            
            # Store message
            store_message_in_thread(
                user_id=user_id,
                thread_id=st.session_state.current_thread_id,
                role="user",
                content=user_input,
                timestamp=datetime.now(pytz.timezone('Asia/Kolkata'))
            )
            
            # Display user message
            st.chat_message("user").write(user_input)
            
            # Add message to OpenAI thread
            client.beta.threads.messages.create(
                thread_id=st.session_state.current_thread_id,
                role="user",
                content=user_input
            )
            
            # Run assistant
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.current_thread_id,
                assistant_id=assistant_id
            )
            
            # Process run
            with st.spinner("Processing your request..."):
                while True:
                    run_status = client.beta.threads.runs.retrieve(
                        thread_id=st.session_state.current_thread_id,
                        run_id=run.id
                    )
                    
                    if run_status.status == 'completed':
                        break
                    elif run_status.status == 'requires_action':
                        handle_tool_calls(
                            run_status,
                            st.session_state.current_thread_id,
                            client,
                            calendar_service
                        )
                    elif run_status.status in ['failed', 'cancelled', 'expired']:
                        st.error(f"Run failed with status: {run_status.status}")
                        break
                    
                    time.sleep(0.5)
            
            # Get and display assistant's response
            messages = client.beta.threads.messages.list(thread_id=st.session_state.current_thread_id)
            for message in messages.data:
                if message.role == "assistant" and message.run_id == run.id:
                    for content in message.content:
                        if content.type == 'text':
                            response_time = time.time() - start_time
                            
                            # Store assistant message
                            store_message_in_thread(
                                user_id=user_id,
                                thread_id=st.session_state.current_thread_id,
                                role="assistant",
                                content=content.text.value,
                                timestamp=datetime.now(pytz.timezone('Asia/Kolkata'))
                            )
                            
                            # Display assistant response with response time
                            with st.chat_message("assistant"):
                                st.write(content.text.value)
                                st.caption(f"Response time: {response_time:.2f} seconds")
            
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")

if __name__ == "__main__":
    # For testing
    if 'user_id' in st.session_state:
        calendar_assistant_dashboard(st.session_state['user_id'])
    else:
        st.error("Please log in first")