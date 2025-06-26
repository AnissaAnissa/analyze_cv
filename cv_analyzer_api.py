from fastapi import FastAPI
from pydantic import BaseModel
import base64
import fitz  
import spacy
import tempfile
import json
import os
import string

nlp = spacy.load("en_core_web_lg")
app = FastAPI()
class CVFile(BaseModel):
    file_base64: str
RESULTS_FILE = "all_cvs.json"

if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

skills_list = [
    "python", "java", "sql",
    "machine learning", "deep learning",
    "teamwork", "communication",
    "natural language processing"
]

@app.post("/analyze-cv")
def analyze_cv(data: CVFile):
    try:
        pdf_bytes = base64.b64decode(data.file_base64)

        tmp_file= tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") 
        tmp_file.write(pdf_bytes)
        tmp_file.close()

        pdf_path = tmp_file.name


        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()

        doc = nlp(text)

        person = ""

        for ent in doc.ents:
            if ent.label_ == "PERSON" and not person:
                person = ent.text

        text_clean = text.lower()
        text_clean = ''.join(char for char in text_clean if char not in string.punctuation)
        '''text_cleaned=""
        for char in text_clean:
            if char not in string.punctuation:
                text_cleaned+=char
        text_clean=text_cleaned
'''
        tokens = [token.text for token in nlp(text_clean)]

        skills_found = []

        for token in tokens:
            if token in skills_list:
                skills_found.append(token)

        for i in range(len(tokens) - 1):
            two_words = tokens[i] + " " + tokens[i + 1]
            if two_words in skills_list:
                skills_found.append(two_words)

        for i in range(len(tokens) - 2):
            three_words = tokens[i] + " " + tokens[i + 1] + " " + tokens[i + 2]
            if three_words in skills_list:
                skills_found.append(three_words)

        result = {
                "person": person or "Non spécifié",
                "skills": list(skills_found)

            }
        
        data_list = []
        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data_list = json.load(f)
        data_list.append(result)

        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)

        return result

    except Exception as e:
        return {"error": str(e)}
