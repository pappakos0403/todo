from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Feladat osztálya
class Task(BaseModel):
    name: str = None
    type: str = None
    is_done: bool = False

# Feladatok listája
tasks = []

@app.get("/")
def root():
    return {"Hello World!"}

# Feladat hozzáadása
@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return tasks

# Feladatok listájának lekérése
@app.get("/tasks")
def list_tasks(limit: int = 10):
    return tasks[0:limit]

# Adott feladat lekérése
@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    if task_id < len(tasks):
        return tasks[task_id]
    else:
        raise HTTPException(status_code=404, detail=f"Nem található a következő feladat: {task_id}")
    
# Adott feladat törlése
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int) -> Task:
    if task_id < len(tasks):
        deleted_task = tasks.pop(task_id)
        return deleted_task
    else:
        raise HTTPException(status_code=404, detail=f"Nem létezik {task_id} számú feladat!")