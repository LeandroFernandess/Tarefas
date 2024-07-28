from firebase_admin import db


# Função para adicionar novas tarefas no Firebase
def AddTask(user_id, task):
    ref = db.reference(f"tasks/{user_id}")
    new_task_ref = ref.push()
    new_task_ref.set({"task": task, "status": "Pending"})


# Função para atualizar o status da tarefa no Firebase
def UpdateTask(user_id, task_key, status):
    ref = db.reference(f"tasks/{user_id}/{task_key}")
    ref.update({"status": status})


# Função para remover uma tarefa do Firebase
def RemoveTask(user_id, task_key):
    ref = db.reference(f"tasks/{user_id}/{task_key}")
    ref.delete()


# Função para carregar tarefas do Firebase
def LoadTask(user_id):
    ref = db.reference(f"tasks/{user_id}")
    return ref.get()
