import streamlit as st
import firebase_admin
from firebase_admin import credentials
from Functions.Function import AddTask, LoadTask, DisplayTask

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

# Sidebar com opções de categoria
page = st.sidebar.radio(
    "Selecione a página", ["Inserir tarefa", "Tarefas diárias", "Tarefas gerais"]
)


# Função principal para inserção e exibição de tarefas
def Main():
    # Defina um ID de usuário fixo, ou modifique conforme necessário
    user_id = "default_user_id"

    if page == "Inserir tarefa":
        # Campo para adicionar uma nova tarefa
        st.markdown(
            "<h1 style='text-align: center;'>Adicionar Nova Tarefa</h1>",
            unsafe_allow_html=True,
        )
        new_task = st.text_area("Insira uma nova tarefa aqui:")
        task_category = st.selectbox(
            "Selecione a categoria da tarefa", ["Tarefas diárias", "Tarefas gerais"]
        )

        if st.button("Adicionar Tarefa"):
            if new_task == "":
                st.error("Insira alguma tarefa")
            else:
                st.success("Tarefa inserida com sucesso")
                AddTask(user_id, new_task, task_category)

    else:
        # Carregar e exibir tarefas com base na categoria selecionada na sidebar
        task_list = LoadTask(user_id) or {}

        st.markdown(
            f"<h3 style='text-align: center;'>Tarefas: {page}</h3>",
            unsafe_allow_html=True,
        )
        DisplayTask(user_id, task_list, page)


if __name__ == "__main__":
    Main()
