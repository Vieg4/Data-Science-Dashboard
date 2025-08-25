import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np


# Configuração do Streamlit
st.set_page_config(layout="wide")
st.title("🚗 Uber Ride Analytics Dataset 2024")

# Descrição inicial
st.markdown("""
**Descrição:**  
Este dataset contém dados detalhados de operações de ride-sharing da Uber ao longo de 2024, oferecendo insights sobre padrões de reserva, desempenho de veículos, receitas, cancelamentos e métricas de satisfação dos clientes.  
O dataset possui 148.770 registros e permite análises completas sobre corridas concluídas, cancelamentos, comportamento de clientes e indicadores financeiros.

**Objetivo da Análise:**  
Classificar todas as variáveis do dataset de acordo com seu tipo, para facilitar a análise exploratória e a construção de modelos preditivos.
""")

# Carregar dataset
df = pd.read_csv("ncr_ride_bookings.csv")

# Classificação detalhada
tipos_detalhados = []
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        if df[col].dropna().apply(float.is_integer).all():
            tipo = "Quantitativa Discreta"
        else:
            tipo = "Quantitativa Contínua"
    else:
        if col in ["Driver Ratings", "Customer Rating"]:
            tipo = "Qualitativa Ordinal"
        else:
            tipo = "Qualitativa Nominal"
    tipos_detalhados.append(tipo)

# Criar tabela
tabela_detalhada = pd.DataFrame({
    "Variável": df.columns,
    "Tipo Detalhado": tipos_detalhados
})

# Exibir tabela
st.subheader("Classificação Detalhada das Variáveis")
st.dataframe(tabela_detalhada)

# --------------------------
# GRÁFICOS EM DUAS COLUNAS (Tamanho uniforme)
# --------------------------
st.subheader("📊 Visualizações e Insights")

fig_width, fig_height = 7, 4  # Tamanho uniforme
limite_y = df["Booking ID"].count() * 0.3  # Limite y padrão para contagens grandes

def plot_count(data, x, palette="Set2", xlabel="", ylabel="Número de Ocorrências", rotation=0, limite_y=None):
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.countplot(data=data, x=x, palette=palette, order=data[x].value_counts().index, ax=ax)
    ax.set_xlabel(xlabel if xlabel else x)
    ax.set_ylabel(ylabel)
    if rotation:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=rotation)
    if limite_y:
        ax.set_ylim(0, limite_y)
    return fig

def plot_hist(data, x, bins=20, color="skyblue", xlabel="", ylabel="Número de Ocorrências"):
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.histplot(data[x], bins=bins, kde=True, color=color, ax=ax)
    ax.set_xlabel(xlabel if xlabel else x)
    ax.set_ylabel(ylabel)
    return fig

# Linha 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Distribuição do Status das Reservas**")
    fig = plot_count(df, "Booking Status", palette="Set2", rotation=45, limite_y=limite_y)
    st.pyplot(fig)

with col2:
    st.markdown("**Tipos de Veículos mais Utilizados**")
    fig = plot_count(df, "Vehicle Type", palette="Set3", rotation=45, limite_y=limite_y)
    st.pyplot(fig)

# Linha 2
col3, col4 = st.columns(2)

with col3:
    st.markdown("**Distribuição das Distâncias das Corridas**")
    fig = plot_hist(df, "Ride Distance", bins=20, color="skyblue", xlabel="Distância (km)")
    st.pyplot(fig)

with col4:
    st.markdown("**Distribuição do Valor das Corridas**")
    fig = plot_hist(df, "Booking Value", bins=20, color="lightgreen", xlabel="Valor")
    st.pyplot(fig)

# Linha 3
col5, col6 = st.columns(2)

with col5:
    st.markdown("**Cancelamentos por Cliente e Motorista**")
    cancel_df = pd.DataFrame({
        "Tipo de Cancelamento": ["Cliente", "Motorista"],
        "Quantidade": [df["Cancelled Rides by Customer"].sum(), df["Cancelled Rides by Driver"].sum()]
    })
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    sns.barplot(data=cancel_df, x="Tipo de Cancelamento", y="Quantidade", palette="pastel", ax=ax)
    ax.set_ylim(0, cancel_df["Quantidade"].max() * 1.1)  # Limite y uniforme
    st.pyplot(fig)

with col6:
    st.markdown("**Método de Pagamento mais Utilizado**")
    fig = plot_count(df, "Payment Method", palette="Set1", rotation=45, limite_y=limite_y)
    st.pyplot(fig)

# Linha 4
col7, col8 = st.columns(2)

with col7:
    st.markdown("**Avaliações dos Motoristas**")
    fig = plot_count(df, "Driver Ratings", palette="Blues", limite_y=limite_y)
    st.pyplot(fig)

with col8:
    st.markdown("**Avaliações dos Clientes**")
    fig = plot_count(df, "Customer Rating", palette="Greens", limite_y=limite_y)
    st.pyplot(fig)

st.subheader("Perguntas de Análise Possíveis")

st.markdown("""
Corridas
- Qual é a **proporção de corridas concluídas** versus canceladas?  
- Qual é o **tipo de veículo mais utilizado** ao longo do tempo?  
- Qual é a **distância média** de uma corrida? Existem corridas muito longas ou muito curtas?  
- Em que horários do dia ocorre o **maior volume de corridas**?  

Clientes
- Qual é a distribuição de **avaliações dadas pelos clientes**?  
- Quais são os principais **motivos de cancelamento pelos clientes**?  
- Existe algum **padrão de cancelamento** relacionado ao tipo de veículo ou horário?  
- Clientes com **maior frequência de corridas** avaliam melhor ou pior os motoristas?  

Motoristas
- Qual é a distribuição de **avaliações recebidas pelos motoristas**?  
- Quais são os **motivos mais comuns para cancelamentos pelos motoristas**?  
- Motoristas com avaliações mais baixas estão relacionados a **mais cancelamentos**?  
- Há diferenças no **tempo médio de chegada do motorista (VTAT)** entre tipos de veículos?  

Receita e Pagamento
- Qual é o **valor médio de uma corrida** por tipo de veículo?  
- Quais são os **métodos de pagamento mais utilizados**?  
- Existe relação entre **valor da corrida** e **distância percorrida**?  
- Corridas pagas em dinheiro têm maior taxa de cancelamento?  

Localização
- Quais são os **locais mais comuns de partida e destino**?  
- Existe um padrão geográfico em **cancelamentos**?  
- Quais áreas concentram **corridas de maior valor**?  

""")




st.subheader("Proporção de Corridas Concluídas vs Canceladas")

# Criar coluna "Status Simplificado"
df["Status Simplificado"] = df["Booking Status"].apply(
    lambda x: "Concluída" if x == "Completed" else "Cancelada"
)

# Contagem
status_counts = df["Status Simplificado"].value_counts(normalize=True) * 100

# Layout em duas colunas
col1, col2 = st.columns([1, 1.5])

with col1:
    # Gráfico de Pizza menor
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(
        status_counts,
        labels=status_counts.index,
        autopct='%1.1f%%',
        colors=["#4CAF50", "#F44336"],
        startangle=90
    )
    ax.set_title("Corridas Concluídas vs Canceladas", fontsize=12)
    st.pyplot(fig)

with col2:
    st.markdown(
        f"""
         
        - A maioria das corridas foram **concluídas**.  
        - Apenas **{status_counts['Cancelada']:.1f}%** das corridas resultaram em cancelamento.  
        - Isso indica uma **boa taxa de sucesso operacional**.  
        """
    )
    

# --------------------------
# Pergunta: Qual é o tipo de veículo mais utilizado ao longo do tempo?
# --------------------------

st.subheader("Uso de Tipos de Veículo ao Longo do Tempo")

col1, col2 = st.columns([1, 1.2])

with col1:
    # Converter coluna de data
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Criar coluna de ano-mês
    df["AnoMes"] = df["Date"].dt.to_period("M").astype(str)

    # Contagem de corridas por tipo de veículo e mês
    veiculo_tempo = df.groupby(["AnoMes", "Vehicle Type"]).size().reset_index(name="Qtd")

    # Gráfico de linhas menor
    fig, ax = plt.subplots(figsize=(6,4))
    sns.lineplot(data=veiculo_tempo, x="AnoMes", y="Qtd", hue="Vehicle Type", marker="o", ax=ax)

    ax.set_title("Uso de Tipos de Veículo ao Longo do Tempo", fontsize=12)
    ax.set_xlabel("Período (Ano-Mês)", fontsize=10)
    ax.set_ylabel("Quantidade de Corridas", fontsize=10)
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(title="Tipo de Veículo", fontsize=8)

    st.pyplot(fig)

with col2:
    st.markdown(
        """
          
        - Podemos identificar quais **tipos de veículos são mais populares ao longo do tempo**.  
        - Se houver tendências claras (como crescimento no uso de **eBikes** ou queda no uso de **Autos**), isso pode indicar **mudanças no comportamento dos clientes**.  
        - Também é útil para entender **picos sazonais** (feriados, fins de semana, meses de maior movimento).  
        """
    )



# --------------------------
# Pergunta: Em que horários do dia ocorre o maior volume de corridas?
# --------------------------

st.subheader("Volume de Corridas por Hora do Dia")

col1, col2 = st.columns([1, 1.5])

with col1:
    # Extrair hora da coluna "Time"
    df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

    # Contagem de corridas por hora
    corridas_hora = df.groupby("Hour").size()

    # Gráfico de barras menor
    fig, ax = plt.subplots(figsize=(5,3))
    sns.barplot(x=corridas_hora.index, y=corridas_hora.values, palette="coolwarm", ax=ax)

    ax.set_title("Número de Corridas por Hora do Dia", fontsize=12)
    ax.set_xlabel("Hora do Dia", fontsize=10)
    ax.set_ylabel("Quantidade de Corridas", fontsize=10)
    ax.set_xticks(range(0,24))  # Apenas números inteiros de 0 a 23
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    st.pyplot(fig)

with col2:
    st.markdown(
        """
         
        - É possível identificar os **picos de demanda** ao longo do dia.  
        - Geralmente, há **mais corridas nos horários de pico** (manhã e final da tarde).  
        - Horários com menor volume podem indicar **oportunidades de incentivo a corridas**.  
        """
    )



# --------------------------
# Pergunta: Distância Média e Mediana das Corridas ao Longo do Tempo
# --------------------------

st.subheader("Distância Média e Mediana das Corridas ao Longo do Tempo")

col1, col2 = st.columns([1, 1.2])

with col1:
    # Criar coluna Ano-Mês
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["AnoMes"] = df["Date"].dt.to_period("M").astype(str)

    # Calcular média e mediana por mês
    distancia_stats = df.groupby("AnoMes")["Ride Distance"].agg(["mean","median"]).reset_index()

    # Gráfico de linhas
    fig, ax = plt.subplots(figsize=(6,4))
    sns.lineplot(data=distancia_stats, x="AnoMes", y="mean", marker="o", label="Média", ax=ax)
    sns.lineplot(data=distancia_stats, x="AnoMes", y="median", marker="o", label="Mediana", ax=ax)

    ax.set_title("Distância Média e Mediana por Mês", fontsize=12)
    ax.set_xlabel("Período (Ano-Mês)", fontsize=10)
    ax.set_ylabel("Distância (km)", fontsize=10)
    ax.tick_params(axis='x', rotation=45, labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(title="Estatística", fontsize=8)
    
    st.pyplot(fig)

with col2:
    st.markdown(
        """

        - A **distância média** geralmente é maior que a **mediana**, indicando algumas corridas muito longas que puxam a média para cima.  
        - Podemos observar **tendências sazonais**: alguns meses têm distâncias maiores ou menores, possivelmente relacionadas a feriados ou demanda específica.  
        - Esse gráfico ajuda a entender o **padrão de uso dos veículos ao longo do tempo**, útil para planejamento operacional.  
        """
    )



# --------------------------
# Pergunta: Boxplots das Métricas
# --------------------------

st.subheader("Distribuição das Métricas")

# Distância das corridas
col1, col2 = st.columns([1, 1.5])
with col1:
    fig, ax = plt.subplots(figsize=(5,3))
    sns.boxplot(y="Ride Distance", data=df, color="#4CAF50", ax=ax)
    ax.set_title("Distância das Corridas", fontsize=12)
    ax.set_ylabel("Distância (km)", fontsize=10)
    ax.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)

with col2:
    st.markdown(
        f"""
        ### Distância  
        - Média da distância: {df['Ride Distance'].mean():.2f} km.  
        - A maior parte das corridas está entre {df['Ride Distance'].quantile(0.25):.2f} km e {df['Ride Distance'].quantile(0.75):.2f} km.  
        - Há algumas corridas muito longas (outliers), que aumentam a média.  
        """
    )

# Valor das corridas
col1, col2 = st.columns([1, 1.5])
with col1:
    fig, ax = plt.subplots(figsize=(5,3))
    sns.boxplot(y="Booking Value", data=df, color="#2196F3", ax=ax)
    ax.set_title("Valor das Corridas", fontsize=12)
    ax.set_ylabel("Valor (R$)", fontsize=10)
    ax.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)

with col2:
    st.markdown(
        f"""
        ### Valor  
        - Média: R$ {df['Booking Value'].mean():.2f}  
        - A maioria das corridas custa entre R$ {df['Booking Value'].quantile(0.25):.2f} e R$ {df['Booking Value'].quantile(0.75):.2f}.  
        - Corridas muito caras ou muito baratas aparecem como outliers, aumentando a média.  
        """
    )

# Tempo médio do motorista (VTAT)
col1, col2 = st.columns([1, 1.5])
with col1:
    fig, ax = plt.subplots(figsize=(5,3))
    sns.boxplot(y="Avg VTAT", data=df, color="#FF9800", ax=ax)
    ax.set_title("Tempo Médio do Motorista (VTAT)", fontsize=12)
    ax.set_ylabel("Tempo (min)", fontsize=10)
    ax.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)

with col2:
    st.markdown(
        f"""
        ### VTAT  
        - Média: {df['Avg VTAT'].mean():.2f} min  
        - A maior parte dos tempos está entre {df['Avg VTAT'].quantile(0.25):.2f} e {df['Avg VTAT'].quantile(0.75):.2f} min.  
        - Outliers indicam alguns motoristas que demoram muito mais para chegar, provavelmente em horários ou regiões específicas.  
        """
    )





st.subheader("📊 Indicadores com Intervalo de Confiança Ajustável")

# Sliders interativos
conf_level = st.slider("Nível de confiança (%)", min_value=60, max_value=100, value=95, step=1)
percentil_max = st.slider("Percentil máximo para outliers", min_value=90, max_value=100, value=95, step=1)

alpha = 1 - conf_level/100

# Função para calcular IC
def calcular_ic(data, alpha):
    n = len(data)
    media = data.mean()
    std = data.std()
    t_crit = stats.t.ppf(1 - alpha/2, df=n-1)
    intervalo = t_crit * (std/np.sqrt(n))
    return media, intervalo

# Preparar métricas
metricas = {
    "Booking Value (R$)": df["Booking Value"],
    "Ride Distance (km)": df["Ride Distance"],
    "Avg VTAT (min)": df["Avg VTAT"]
}

medias = []
intervalos = []
nomes = []

# Calcular média e IC para cada métrica
for nome, dados in metricas.items():
    limite = dados.quantile(percentil_max/100)
    dados_clip = dados.clip(upper=limite)
    media, intervalo = calcular_ic(dados_clip, alpha)
    medias.append(media)
    intervalos.append(intervalo)
    nomes.append(nome)

# Layout: gráfico à esquerda e texto à direita
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(nomes, medias, yerr=intervalos, capsize=10, color=["#2196F3", "#4CAF50", "#FF9800"])
    ax.set_ylabel("Valores")
    ax.set_title(f"Média das Métricas com IC {conf_level}%")
    ax.tick_params(axis='y', labelsize=10)
    col1.pyplot(fig)

with col2:
    st.markdown(
    f"""

    - **Ride Distance (km):** a média das distâncias percorridas é {medias[1]:.2f} km, com IC {conf_level}% de {medias[1]-intervalos[1]:.2f} a {medias[1]+intervalos[1]:.2f} km.  

    - **Avg VTAT (min):** o tempo médio que os motoristas levam para chegar aos clientes é {medias[2]:.2f} minutos, com IC {conf_level}% de {medias[2]-intervalos[2]:.2f} a {medias[2]+intervalos[2]:.2f} minutos.  

    - Cada barra do gráfico representa a média de uma métrica e as linhas de erro mostram a variação provável da média real (intervalo de confiança).  

    - Ajuste o percentil máximo para remover outliers extremos e visualizar melhor a maioria dos dados.

    - Booking Value (R$): R$ {medias[0]:.2f}. O intervalo de confiança de {conf_level}% indica que estamos confiantes de que a média real do valor das corridas está entre R$ {medias[0]-intervalos[0]:.2f} e R$ {medias[0]+intervalos[0]:.2f}.  
    """
)
    


st.subheader("🔹 Justificativa do Intervalo de Confiança")

st.markdown(
    """
    Para este estudo, definimos um **intervalo de confiança (IC) ajustável entre 60% e 99%**.  
    A escolha de um IC inferior a 100% é necessária porque valores de 100% geram limites infinitos (-inf a inf), tornando a interpretação impossível.  

    O **nível de confiança ideal** depende do equilíbrio entre **precisão** e **segurança** na estimativa:  
    - **IC muito baixo (60-70%)**: intervalo estreito, mas maior risco de a média verdadeira não estar dentro da faixa.  
    - **IC moderado (90-95%)**: equilíbrio ideal para a maioria das análises, fornecendo uma faixa confiável e ainda representativa.  
    - **IC muito alto (99%)**: intervalo mais amplo, cobre quase todas as possibilidades, mas pode ser pouco informativo visualmente.  

    Portanto, recomendamos **IC entre 90% e 95%** para análise de métricas como **Valor das Corridas, Distância e Tempo de Chegada**, pois fornece **uma estimativa confiável da média sem exagerar a variação**.
    """
)




st.subheader("🔹 Conclusão do Trabalho")

st.markdown(
    """
    Após a análise detalhada do dataset de Uber Ride Analytics 2024, podemos concluir:  

    - A maioria das corridas é concluída, com cancelamentos representando uma pequena fração do total.  
    - O **tipo de veículo mais utilizado** e os **picos de horários** podem ser identificados, permitindo otimização de frota e planejamento de horários de maior demanda.  
    - Métricas como **Valor da Corrida, Distância e Tempo de Chegada** apresentam variações que podem ser visualizadas com **boxplots e intervalos de confiança**, fornecendo insights sobre padrões típicos e outliers.  
    - O uso do **intervalo de confiança (90-95%)** permite entender a faixa provável da média real de cada métrica, tornando a análise mais robusta e confiável.  
    - Essa análise pode servir de base para **estratégias de precificação, alocação de veículos e melhorias no atendimento ao cliente**.

    Em resumo, o dashboard fornece uma visão clara e interativa das operações da Uber, ajudando a **tomar decisões estratégicas com base em dados reais**.
    """
)
