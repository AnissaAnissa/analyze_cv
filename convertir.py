import base64
import fitz  
import spacy
nlp = spacy.load("en_core_web_lg")

with open("cv_anissa.pdf", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")
    print(encoded)

text = ""
with fitz.open("cv_anissa.pdf") as doc:
    for page in doc:
        text += page.get_text()

doc = nlp(text)
for ent in doc.ents:
    print(f"{ent.text}-->{ent.label_}")

