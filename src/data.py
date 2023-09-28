import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from string import punctuation
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest
from collections import defaultdict

# Create a speech recognition object
r = sr.Recognizer()

def transcribe_large_audio(path):
    """Split audio into chunks and apply speech recognition"""
    sound = AudioSegment.from_mp3(os.path.abspath(path))

    # Split audio based on silence
    chunks = split_on_silence(sound)
    
    # Folder to store chunks
    folder_name = "chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    
    whole_text = ""
    # Processsing, exporting and removing each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
                text = f"{text.capitalize()}. "
                whole_text += text
            except sr.UnknownValueError as e:
                continue
        os.remove(chunk_filename) 

    # Return text for all chunks
    return whole_text


def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    def empty():
        return 0
    word_frequencies=defaultdict(empty)
    for word in tokens:
        if (len(word)) and (word.lower() not in list(STOP_WORDS)) and (word.lower() not in punctuation):
            word_frequencies[word] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = defaultdict(empty)
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary


filename = input("Enter the filepath relative to src folder:")
result = transcribe_large_audio(filename)
print(summarize(result, 0.005))