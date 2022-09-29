import requests
import streamlit as st

uploaded_file = st.file_uploader("Select file from your directory")
if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    st.audio(audio_bytes, format='audio/mp3')
UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPTION_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
api_key = "24cb91bdd2264679bf0f35e89430dab9"
headers = {"authorization": api_key, "content-type": "application/json"}
def read_file(filename):
    while True:
        data = filename.read(5242880)
        if not data:
            break
        yield data
upload_response = requests.post(UPLOAD_ENDPOINT, headers=headers, data=read_file(uploaded_file))
audio_url = upload_response.json()["upload_url"]
transcript_request = {'audio_url': audio_url,"speaker_labels": True}
transcript_response = requests.post(TRANSCRIPTION_ENDPOINT, json=transcript_request, headers=headers)
_id = transcript_response.json()["id"]
while True:
    polling_response = requests.get(TRANSCRIPTION_ENDPOINT + "/" + _id, headers=headers)

    if polling_response.json()['status'] == 'completed':
        st.header('Audio To Text Converter')
        break
    elif polling_response.json()['status'] == 'error':
        raise Exception("Transcription failed. Make sure a valid API key has been used.")
with open('readme.txt', 'w') as file:
    for speaker in polling_response.json()['utterances']:
        note=f'Speaker {speaker.get("speaker")} : {speaker.get("text")}'
        st.write(note)
        file.write(note)
        file.write('\n')
with open('readme.txt','r')as file:
    st.download_button('Download',file, 'readme')
