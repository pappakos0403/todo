from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# FastAPI példány
app = FastAPI()

# Adatbázis kapcsolat
conn = sqlite3.connect('tasks_database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               type TEXT,
               is_done BOOLEAN
               )
''')

# Feladat osztálya
class Task(BaseModel):
    id: int | None = None
    name: str = None
    type: str = None
    is_done: bool = False

@app.get("/")
def root():
    return {"Hello World!"}

# Feladat hozzáadása
@app.post("/tasks")
def create_task(task: Task):
    # Adatok hozzáadása az adatbázishoz
    cursor.execute(
        "INSERT INTO tasks (name, type, is_done) VALUES (?, ?, ?)",
        (task.name, task.type, int(task.is_done))
    )
    conn.commit()

    # Visszajelzés küldése
    new_id = cursor.lastrowid
    cursor.execute(
        "SELECT id, name, type, is_done FROM tasks WHERE id = ?",
        (new_id,)
    )
    row = cursor.fetchone()
    return {
        "id": row[0],
        "name": row[1],
        "type": row[2],
        "is_done": bool(row[3])
    }

# Feladatok listájának lekérése
@app.get("/tasks")
def list_tasks(limit: int = 10):
    cursor.execute(
        "SELECT id, name, type, is_done FROM tasks LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "is_done": bool(row[3])
        })
    return tasks

# Adott feladat lekérése
@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    cursor.execute(
        "SELECT id, name, type, is_done FROM tasks WHERE id = ?",
        (task_id,)
    )
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Nem található ez a feladat: {task_id}")
    task = {
        "id": row[0],
        "name": row[1],
        "type": row[2],
        "is_done": bool(row[3])
    }
    return task
    
# Adott feladat törlése
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    )

    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Nem található ez a feladat: {task_id}")
    
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    return {"message": f"{task_id} törölve!"}