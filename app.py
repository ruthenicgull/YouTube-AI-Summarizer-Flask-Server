from flask import Flask, request, jsonify
from flask_cors import CORS 
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)
CORS(app)

prompt = """
You are Yotube video summarizer. You will be given the transcript text of a YouTube video. 
You are supposed to summarize the entire video in points (either numbered or bulleted) and optionally subpoints within 250 words. 
Please summarize the transcript here: 
"""

@app.route('/api/summary', methods=['GET', 'POST'])
def get_response():
    link = request.json.get('data')
    try: 
        transcript = extract_transcript_details(link)
        summary = generate_gemini_content(transcript, prompt)
        return jsonify({
            'summary': summary,
        })
    except:
        return jsonify({
            'summary': 'Error'
        })


def get_youtube_video_id(url):
    
    return url.split('=')[1]

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=get_youtube_video_id(youtube_video_url)
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    print(response.text)
    return response.text

if __name__ == '__main__':
    app.run(debug=True)
