# AI Storyteller Narrator using OpenAI + ElevenLabs

import openai
import os
import requests
import streamlit as st

# --- Setup ---
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


def generate_story(prompt, max_tokens=500):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": f"Tell me a short story about: {prompt}"}
        ],
        max_tokens=max_tokens,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()


def convert_text_to_speech(text, voice_id="Rachel"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open("story.mp3", "wb") as f:
            f.write(response.content)
        return "story.mp3"
    else:
        raise Exception(f"Text-to-Speech Error: {response.text}")


# --- Streamlit UI ---
st.set_page_config(page_title="AI Storyteller Narrator")
st.title("📖 AI Storyteller + Narrator")

story_prompt = st.text_input("Enter a story prompt:", "A curious cat exploring space")
voice_option = st.selectbox("Choose Voice", ["Rachel", "Bella", "Antoni", "Elli"], index=0)

if st.button("Generate & Narrate Story"):
    if story_prompt:
        with st.spinner("Generating story..."):
            story = generate_story(story_prompt)
            st.subheader("Generated Story")
            st.write(story)

        with st.spinner("Generating narration with ElevenLabs..."):
            try:
                audio_file = convert_text_to_speech(story, voice_id=voice_option)
                st.audio(audio_file, format='audio/mp3')
                st.success("🎉 Story narrated and saved as story.mp3")
            except Exception as e:
                st.error(str(e))
    else:
        st.warning("Please enter a prompt to generate a story.")
