# Podcast_Summarisation

## Approach
- First I tried to read and perform analysis using librosa 
- Performed on audio: VMP4732384152 <br>
- Converted to smaller chunks of the audion whenever silence was encountered
- Wrote the transcript for it using recognize_google API
- Joined the chunks
- Then performed the text summarization using spacy based on the frequency of the words encountered
- The assumption is compared to regular words the keywords repitition would be higher

## Steps to run it
- upload the files in data dir
- run the data.py from src and enter the audio file's path
- Output gets print in the terminal itself

