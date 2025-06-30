from fastapi import FastAPI
from pydantic import BaseModel
import base64
import fitz  
import spacy
import tempfile
import json
import os
import string

app = FastAPI()
nlp = spacy.load("en_core_web_trf")

class CVFile(BaseModel):
    file_base64: str

RESULTS_FILE = "all_cvs.json"
if not os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

raw_skills = [
    "python", "java", "sql",
    "machine learning", "ml",
    "deep learning", "dl",
    "teamwork", "communication",
    "natural language processing", "nlp"
]

def clean_text(text):
    text = text.lower()
    text = ''.join(c if c not in string.punctuation else ' ' for c in text)
    return ' '.join(text.split())

skills_list = [clean_text(skill) for skill in raw_skills]

@app.post("/analyze-cv")
def analyze_cv(data: CVFile):
    pdf_path = None
    try:
        pdf_bytes = base64.b64decode(data.file_base64)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
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
            if ent.label_ == "PERSON" and 1 < len(ent.text.split()) < 4:
                person = ent.text
                break

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        spacy_sents = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        sentences = []
        for s in lines + spacy_sents:
            if s not in sentences:
                sentences.append(s)

        skill_scores, matched_sentences = analyze_skills_with_similarity(sentences, skills_list)

        for match in matched_sentences:
            print(f"{match['skill']}: {match['sentence']} --> confidence={match['confidence']}")

        result = {
            "person": person or "Non spécifié",
            "skills": list(skill_scores.keys()),
            "skills_score": skill_scores,
        }

        with open(RESULTS_FILE, "r", encoding="utf-8") as f:
            data_list = json.load(f)
        data_list.append(result)
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)

        return result

    except Exception as e:
        return {"error": str(e)}

    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)

def extract_skills(sentence, skills_list):
    sentence = clean_text(sentence)
    found = []
    for skill in skills_list:
        if skill in sentence and skill not in found:
            found.append(skill)
    return found

def analyze_skills_with_similarity(sentences, skills_list):
    skill_scores = {}
    matched_sentences = []

    for sentence in sentences:
        found_skills = extract_skills(sentence, skills_list)
        for skill in found_skills:
            doc_used = nlp(f"I used {skill} in my projects")
            doc_not_used = nlp(f"I have no experience with {skill}")
            sentence_doc = nlp(sentence)

            sim_used = sentence_doc.similarity(doc_used)
            sim_not_used = sentence_doc.similarity(doc_not_used)

            diff = sim_used - sim_not_used

            confidence = (diff + 1) / 2

            if confidence < 0:
                confidence = 0
            elif confidence > 1:
                confidence = 1

            if confidence > 0.4:
                matched_sentences.append({
                    "skill": skill,
                    "sentence": sentence,
                    "confidence": round(confidence, 2)
                })
                if skill not in skill_scores or confidence > skill_scores[skill]:
                    skill_scores[skill] = round(confidence, 2)

    return skill_scores, matched_sentences
