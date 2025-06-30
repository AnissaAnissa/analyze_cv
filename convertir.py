import base64
import fitz  
import spacy
nlp = spacy.load("en_core_web_lg")

with open("cv_test5.pdf", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")
    print(encoded)
    print("cv test3")


