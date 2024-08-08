import streamlit as st
from Functions.Function import AddTask, LoadTask, DisplayTask, Auth, SetupFirebase


# Configurações iniciais do Streamlit
st.set_page_config(page_title="Tarefas", page_icon="📝")


# Função principal para inserção e exibição de tarefas
def App():
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
    SetupFirebase()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown(
            "<h1 style='text-align: center;'>Gerenciamento de tarefas - Login</h1>",
            unsafe_allow_html=True,
        )
        password = st.text_input("Insira a senha:", type="password")
        if st.button("Entrar"):
            if Auth(password):
                st.success("Autenticado com sucesso!")
                st.rerun()
            else:
                st.error("Senha incorreta. Tente novamente.")
    else:
        App()
