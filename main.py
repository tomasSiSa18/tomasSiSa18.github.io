from fastapi import FastAPI
import json
import random
from pydantic import BaseModel
from typing import List, Optional
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montar la carpeta para servir imágenes estáticas (si las usas localmente)
app.mount("/static", StaticFiles(directory="images"), name="static")

# Cargar preguntas desde el archivo JSON
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    questions = data["questions"]

# Modelo de respuesta para una pregunta
class QuestionResponse(BaseModel):
    code: int
    msg: str
    data: dict
    request_id: str

# Generar un ID aleatorio (simulación de request_id)
def generate_request_id():
    return str(random.randint(1000000000, 9999999999))

# Endpoint para obtener una pregunta aleatoria
@app.get("/api/randomquestion", response_model=QuestionResponse)
def get_random_question():
    question = random.choice(questions)
    
    response = {
        "code": 200,
        "msg": "Pregunta obtenida con éxito",
        "data": {
            "context": question["context"],
            "question": question["question"],
            "options": question["options"],
            "correct_answer": question["correct_answer"],
            "image": question["image"]
        },
        "request_id": generate_request_id()
    }
    
    return response
