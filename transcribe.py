import sys
import os
import json
import tempfile
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from tqdm import tqdm

def transcribe_video(path):
    output = []

    clip = mp.VideoFileClip(path)
    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_file = os.path.join(tmp_dir, 'audio.wav')
        clip.audio.write_audiofile(audio_file, verbose=False, logger=None)
        audio = AudioSegment.from_wav(audio_file)
        chunks = split_on_silence(
            audio, silence_thresh=audio.dBFS-8, min_silence_len=250, keep_silence=250)
        time_from_0 = 0
        for index, chunk in enumerate(tqdm(chunks)):
            chunk_name = os.path.join(
                tmp_dir, 'chunk{index}.wav'.format(index=index))
            chunk.export(chunk_name, format='wav', codec='wav')
            recognizer = sr.Recognizer()
            with sr.AudioFile(chunk_name) as source:
                audio_listened = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio_listened)
                    output.append({'text': transcription, 'time': time_from_0})
                except Exception as e:
                    pass
                time_from_0 += len(chunk)
    return output


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python main.py input_video output_json_file.json')

    result = transcribe_video(sys.argv[1])
    with open(sys.argv[2], 'w') as f:
        f.write(json.dumps(result))
