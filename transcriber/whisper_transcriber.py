# telegram_video_summary_bot/transcriber/whisper_transcriber.py
import whisper
from moviepy.editor import VideoFileClip  # Adicione esta linha para importar VideoFileClip

class WhisperTranscriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)

    def transcribe_video(self, video_path):
        audio_path = self._extract_audio(video_path)
        result = self.model.transcribe(audio_path)
        return result['text']

    def _extract_audio(self, video_path):
        audio_path = "audio_extracted.mp3"
        video = VideoFileClip(video_path)  # Certifique-se de que VideoFileClip seja reconhecido agora
        video.audio.write_audiofile(audio_path)
        return audio_path
