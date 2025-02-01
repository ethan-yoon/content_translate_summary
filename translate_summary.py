from youtube_transcript_api import YouTubeTranscriptApi
import requests

# Enter the ID of the YouTube video
video_id = 'VIDEO_ID_HERE'


# Ollama API endpoint (if you are running locally)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def fetch_transcript(video_id):
    try:
        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])  # ex. ko means Korean subtitles.
        # Collect all the transcripts into a single string.
        full_transcript = " ".join([line['text'] for line in transcript])
        return full_transcript
    except Exception as e:
        print(f"An error occurred while fetching subtitles: {e}")
        return None

def summarize_with_deepseek(text, model_name="deepseek-r1:1.5b"):
    try:
        # Send a request to the Ollama API.
        payload = {
            "model": model_name,
            "prompt": f"please summarize in 50 words\n{text}",
            "stream": False
        }
        # "prompt": f"Please summarize the following text:\n{text}",
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception if an HTTP error
        result = response.json()
        return result.get("response", "Summary failed.")
    except Exception as e:
        print(f"An error occurred while requesting Ollama API: {e}")
        return None

def main():
    # Get the transcript of a YouTube video.
    transcript = fetch_transcript(video_id)
    if transcript:
        print("Original transcript:\n", transcript)
        
        # Summarize the transcript using a DeepSeek model.
        summary = summarize_with_deepseek(transcript)
        if summary:
            print("\nSummary result:\n", summary)
    else:
        print("Failed to fetch the transcript.")

if __name__ == "__main__":
    main()
