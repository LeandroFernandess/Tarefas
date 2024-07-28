import streamlit as st
import firebase_admin
from firebase_admin import credentials
from Functions.Function import AddTask, RemoveTask, UpdateTask, LoadTask

# Configuração do Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate("credentials.json")  # Atualize esse caminho
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://tarefas-9493e-default-rtdb.firebaseio.com"  # Atualize com o URL do seu banco de dados
        },
    )

st.set_page_config(page_title="Tarefas")


# Função para exibir tarefas com cores do Streamlit
def DisplayTask(user_id, task_list):
    success_color = "#058034"
    warning_color = "#F21010"

    for task_key, task in task_list.items():
        if task["status"] == "Done":
            status_color = success_color
        else:
            status_color = warning_color

        task_label = f"<div style='background-color: {status_color}; padding: 10px; margin-bottom: 5px; border-radius: 5px;'>{task['task']}</div>"
        st.markdown(task_label, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            done_button = st.button(f"Tarefa concluída", key=f"done_{task_key}")
        with col2:
            pending_button = st.button(f"Tarefa pendente", key=f"pending_{task_key}")
        with col3:
            delete_button = st.button(f"Deletar tarefa", key=f"delete_{task_key}")

        if done_button:
            UpdateTask(user_id, task_key, "Done")
            st.rerun()
        if pending_button:
            UpdateTask(user_id, task_key, "Pending")
            st.rerun()
        if delete_button:
            RemoveTask(user_id, task_key)
            st.rerun()


# Carregar as tarefas sem autenticação
def task_manager_page():
    # Defina um ID de usuário fixo, ou modifique conforme necessário
    user_id = "default_user_id"
    task_list = LoadTask(user_id) or {}

    st.markdown(
        "<h1 style='text-align: center;'>Lista de Tarefas</h1>", unsafe_allow_html=True
    )
    st.write("---")

    # Campo para adicionar uma nova tarefa
    new_task = st.text_input("Insira uma nova tarefa aqui:")

    if st.button("Adicionar Tarefa"):
        if new_task == "":
            st.error("Insira alguma tarefa")
        else:
            AddTask(user_id, new_task)
            st.rerun()

    # Exibir lista de tarefas com opções de status e exclusão
    st.subheader("Tarefas")
    DisplayTask(user_id, task_list)


task_manager_page()
