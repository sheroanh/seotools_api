from googletrans import Translator
from transformers import pipeline

GENERATE = pipeline('text-generation', model='gpt2')
TRANSLATOR = Translator()

def translate(text, src, dest):
    return TRANSLATOR.translate(text, src = src, dest = dest).text

def generateText(keyword, numOfWord = 200, n = 1):
    enKeyword = translate(keyword, "vi", "en")
    enDoc = GENERATE(enKeyword, max_length = numOfWord, num_return_sequences = n, do_sample = False)[0]["generated_text"]
    viDoc = translate(enDoc, "en", "vi")
    return viDoc