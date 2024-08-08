import streamlit as st
from Functions.Function import AddTask, LoadTask, DisplayTask
import firebase_admin
from firebase_admin import credentials
import os
import json

# Configurações iniciais do Streamlit
st.set_page_config(page_title="Tarefas", page_icon="📝")

# Função de autenticação
def authenticate(password):
    if st.session_state.get("authenticated", False):
        return True

    # Obtenha a senha da variável de ambiente e log para depuração
    app_password = os.getenv("APP_PASSWORD")
    st.write(f"DEBUG: Stored password: {app_password}")  # Log de depuração

    if password == app_password:
        st.session_state.authenticated = True
        return True

    return False

# Configurar o Firebase
def setup_firebase():
    if not firebase_admin._apps:
        # Obtém as credenciais do Firebase das variáveis de ambiente
        credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        cred = credentials.Certificate(json.loads(credentials_json))
        # Obtém a databaseURL das variáveis de ambiente
        database_url = os.getenv("DATABASE_URL")
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": database_url},
        )

# Função principal para inserção e exibição de tarefas
def main_app():
    st.sidebar.header("Desenvolvido por :red[Leandro Fernandes]", divider="gray")
    
    # Sidebar com opções de categoria
    page = st.sidebar.radio(
        "Selecione a página",
        ["Inserir tarefa", "Tarefas diárias", "Tarefas gerais"],
    )
    st.sidebar.divider()
    st.sidebar.text(
        """
        Sistema desenvolvido para realizar\nanotações do trabalho e demais\natividades.📖
        """
    )

    # Defina um ID de usuário fixo, ou modifique conforme necessário
    user_id = "default_user_id"

    if page == "Inserir tarefa":
        # Campo para adicionar uma nova tarefa
        st.markdown(
            "<h1 style='text-align: center;'>Adicionar Nova Tarefa</h1>",
            unsafe_allow_html=True,
        )
        st.write("---")
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
                new_task = ""

    else:
        # Carregar e exibir tarefas com base na categoria selecionada na sidebar
        task_list = LoadTask(user_id) or {}

        st.markdown(
            f"<h2 style='text-align: center;'>{page}</h2>",
            unsafe_allow_html=True,
        )
        st.write("---")
        DisplayTask(user_id, task_list, page)

if __name__ == "__main__":
    setup_firebase()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown(
            "<h1 style='text-align: center;'>Login</h1>",
            unsafe_allow_html=True,
        )
        password = st.text_input("Insira a senha:", type="password")
        if st.button("Entrar"):
            if authenticate(password):
                st.success("Autenticado com sucesso!")
                st.experimental_rerun()  # Reexecuta a aplicação após autenticação bem-sucedida
            else:
                st.error("Senha incorreta. Tente novamente.")
    else:
        main_app()
