import streamlit as st

st.set_page_config(page_title="Meu Portfólio", page_icon="💼", layout="wide")

# ===========================
# TÍTULO E INTRO
# ===========================
st.title("💼 Meu Portfólio")
st.write("Bem-vindo! Aqui você encontrará informações sobre minha formação, experiência profissional, habilidades técnicas e projetos desenvolvidos.")

st.divider()

# ===========================
# PERFIL - FOTO + SOBRE
# ===========================
col1, col2 = st.columns([1,3])

with col1:
    st.image("Foto.jpg", width=180)  # coloque sua foto

with col2:
    st.subheader("👋 Sobre mim")
    st.write("""
    Sou **desenvolvedor Python** com experiência em:
    - Criação de aplicações web
    - Automação de processos
    - Análise e visualização de dados  

    🚀 Apaixonado por aprender novas tecnologias e desenvolver soluções que fazem a diferença.
    """)

st.divider()

# ===========================
# DESTAQUES (CARDS SIMPLES)
# ===========================
st.subheader("✨ Destaques")
col1, col2, col3 = st.columns(3)

with col1:
    st.success("💻 Desenvolvimento Web")
    st.write("Experiência com Streamlit, Flask e Django.")

with col2:
    st.info("📊 Análise de Dados")
    st.write("Dashboards interativos e relatórios automatizados.")

with col3:
    st.warning("🤖 Automação")
    st.write("Web scraping, RPA e integração de APIs.")

st.divider()

# ===========================
# PROJETOS EM DESTAQUE
# ===========================
st.subheader("📂 Projetos em Destaque")
st.write("Aqui estão alguns dos meus projetos (confira a aba **Projetos** para ver todos):")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🔹 Fish Manager**")
    st.write("O Fish Manager é um sistema de gestão de aquacultura desenvolvido em Python para ajudar piscicultores a gerenciar suas operações de cultivo de peixes de forma eficiente e sustentável..")
    st.link_button("Ver Projeto", "https://github.com/Global-Solution-1ESPH/Python_GS")

with col2:
    st.markdown("**🔹 Oceano Vivo**")
    st.write("Pagina Web para um projeto de conscientização sobre a poluição dos oceanos e à promoção de soluções sustentáveis")
    st.link_button("Ver Projeto", "https://github.com/Global-Solution-1ESPH/gs-front-web")

st.divider()

# ===========================
# CONTATO
# ===========================
st.subheader("🌐 Conecte-se comigo")
col1, col2, = st.columns(2)

with col1:
    st.link_button("LinkedIn", "https://www.linkedin.com/in/gustavo-viega-martins-lopes-75051a26b/")

with col2:
    st.link_button("GitHub", "https://github.com/Vieg4")

st.divider()

# ===========================
# FRASE FINAL
# ===========================
st.markdown("> *“Transformar ideias em soluções através da tecnologia.”*")
