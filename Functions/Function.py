from firebase_admin import db
import streamlit as st
import firebase_admin
from firebase_admin import credentials


# Configuração do Firebase Admin SDK
def SetupFirebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://tarefas-9493e-default-rtdb.firebaseio.com"},
        )


# Função de autenticação
def Authenticate(password):
    if st.session_state.get("authenticated", False):
        return True

    # Verifica a senha inserida contra a senha armazenada em secrets
    if password == st.secrets["app_password"]:
        st.session_state.authenticated = True
        return True

    return False


# Função para adicionar novas tarefas no Firebase
def AddTask(user_id, task, category):
    ref = db.reference(f"tasks/{user_id}")
    new_task_ref = ref.push()
    new_task_ref.set({"task": task, "status": "Pending", "category": category})


# Função para atualizar o status da tarefa no Firebase
def UpdateTask(user_id, task_key, status):
    ref = db.reference(f"tasks/{user_id}/{task_key}")
    ref.update({"status": status})


# Função para editar a tarefa no Firebase
def EditTask(user_id, task_key, new_task):
    ref = db.reference(f"tasks/{user_id}/{task_key}")
    ref.update({"task": new_task})


# Função para remover uma tarefa do Firebase
def RemoveTask(user_id, task_key):
    ref = db.reference(f"tasks/{user_id}/{task_key}")
    ref.delete()


# Função para carregar tarefas do Firebase
def LoadTask(user_id):
    ref = db.reference(f"tasks/{user_id}")
    return ref.get()


# Função para exibir tarefas com cores do Streamlit e opção de edição
def DisplayTask(user_id, task_list, selected_category):
    success_color = "#058034"
    warning_color = "#F21010"

    for task_key, task in task_list.items():
        if "category" not in task or task["category"] != selected_category:
            continue

        if task["status"] == "Done":
            status_color = success_color
        else:
            status_color = warning_color

        task_label = f"<div style='background-color: {status_color}; padding: 10px; margin-bottom: 20px; border-radius: 10px;'>{task['task']}</div>"
        st.markdown(task_label, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            done_button = st.button(f"Tarefa concluída", key=f"done_{task_key}")
        with col2:
            pending_button = st.button(f"Tarefa pendente", key=f"pending_{task_key}")
        with col3:
            delete_button = st.button(f"Deletar tarefa", key=f"delete_{task_key}")
        with col4:
            edit_button = st.button(f"Editar tarefa", key=f"edit_{task_key}")

        if edit_button or f"input_{task_key}" in st.session_state:
            if f"input_{task_key}" not in st.session_state:
                st.session_state[f"input_{task_key}"] = task["task"]
            new_task = st.text_input(
                "Editar Tarefa",
                value=st.session_state[f"input_{task_key}"],
                key=f"input_{task_key}",
            )
            save_button = st.button("Salvar", key=f"save_{task_key}")

            if save_button:
                EditTask(user_id, task_key, new_task)
                st.session_state.pop(f"input_{task_key}", None)
                st.rerun()

        if done_button:
            UpdateTask(user_id, task_key, "Done")
            st.rerun()
        if pending_button:
            UpdateTask(user_id, task_key, "Pending")
            st.rerun()
        if delete_button:
            RemoveTask(user_id, task_key)
            st.rerun()
