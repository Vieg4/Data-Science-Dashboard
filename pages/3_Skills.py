import streamlit as st

st.set_page_config(page_title="Skills Técnicas", page_icon="⚡", layout="wide")

st.title("⚡ Skills Técnicas")

# ===========================
# HARD SKILLS
# ===========================
skills = {
    "Python": "Avançado",
    "SQL": "Intermediário",
    "Machine Learning": "Intermediário",
    "Streamlit": "Intermediário",
    "Git/GitHub": "Intermediário",
    "HTML/CSS": "Avançado",
    "JavaScript": "Básico"
}

st.subheader("🔹 Hard Skills")
col1, col2 = st.columns(2)

with col1:
    for skill, nivel in list(skills.items())[:4]:
        st.markdown(f"- **{skill}** — {nivel}")

with col2:
    for skill, nivel in list(skills.items())[4:]:
        st.markdown(f"- **{skill}** — {nivel}")

st.divider()

# ===========================
# SOFT SKILLS
# ===========================
st.subheader("🤝 Soft Skills")

soft_skills = [
    "Trabalho em equipe",
    "Comunicação clara",
    "Resolução de problemas",
    "Adaptabilidade",
    "Gestão do tempo"
]

for skill in soft_skills:
    st.markdown(f"- {skill}")
