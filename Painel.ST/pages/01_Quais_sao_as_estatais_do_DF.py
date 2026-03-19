# Importando as bibliotecas
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import base64
import matplotlib.pyplot as plt
import seaborn as sns

# Caminho relativo ao arquivo CSV
file_path = 'BD_Completo_Nacional_Formatado.csv'

# Carregando o arquivo CSV no Pandas DataFrame
df = pd.read_csv(file_path)

# Configurações da página
st.set_page_config(
    page_title="Quais são as estatais do DF?",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    /* 1. FUNDO BRANCO */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }

    /* 2. TÍTULOS EM LARANJA */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"], .stHeader {
        color: #fb8c00 !important;
    }
    
    /* Linha divisória laranja */
    hr {
        border-top-color: #fb8c00 !important;
    }

    /* 3. BARRA LATERAL (IDÊNTICA AO INÍCIO) */
    [data-testid="stSidebar"] {
        background-color: #f5f5f5 !important; /* Cinza robusto */
        border-right: 2px solid #fb8c00;
    }

    /* Cor do texto dos itens do menu lateral */
    [data-testid="stSidebarNav"] span {
        color: #363434 !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }

    /* Cor do ícone ao lado do texto no menu */
    [data-testid="stSidebarNav"] svg {
        fill: #FFFFFF !important;
    }

    /* Destaque para a página selecionada */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(251, 140, 0, 0.2) !important;
        border-radius: 5px;
    }
    
    [data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: #fb8c00 !important;
        font-weight: bold !important;
    }

    /* 4. BOTÕES LARANJAS */
    div.stButton > button {
        background-color: #fb8c00 !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
    }

    /* 5. TEXTOS LONGOS (CORRIGINDO ILEGIBILIDADE) */
    .stMarkdown p, .stWrite {
        color: #2F2F2F !important; /* Cinza escuro legível */
        text-align: justify;
    }



    /* Garante que os números das listas (1, 2, 3...) também fiquem escuros */
    .stMarkdown li::marker {
        color: #2F2F2F !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title(":orange[As Empresas Estatais Distritais]")
st.subheader("Quais são as estatais do DF?", divider="orange")

# Conteúdo específico desta página
st.write("""

No ano de 2023, o Distrito Federal possuía 26 empresas estatais ativas. Esse número permaneceu estável em relação aos anos de 2021 e 2022. Já em 2020, o DF contava com 22 estatais, evidenciando um aumento no quantitativo dessas instituições ao longo do período analisado.

A expansão do número de empresas ocorreu devido à criação de quatro novas estatais ligadas ao setor energético, todas pertencentes ao grupo CEB (Companhia Energética de Brasília), a saber:

CEB Geração – Responsável pela produção de energia elétrica em usinas próprias e participação em projetos de geração;

CEB Iluminação Pública e Serviços – Voltada à gestão e operação da infraestrutura de iluminação pública no Distrito Federal;

CEB Lajeado – Criada para atuação específica no setor de energia, com foco em projetos estratégicos de geração e distribuição;

CEB Participações – Destinada à administração de participações societárias da CEB em empresas do setor elétrico;

Além das empresas em operação, o painel identificou quatro estatais em processo de liquidação no ano de 2023. O encerramento dessas entidades pode estar relacionado a reestruturações estratégicas, fusões ou inviabilidade econômica. As empresas em liquidação são:

CODEPLAN - Companhia de Planejamento do Distrito Federal – Empresa pública tradicionalmente voltada ao planejamento e desenvolvimento de soluções tecnológicas para o governo;

DF Gestão de Ativos – Criada para administrar ativos do Governo do Distrito Federal, mas encerrada devido a reestruturações no modelo de gestão patrimonial;

PROFLORA - Florestamento e Reflorestamento – Empresa focada em projetos ambientais e reflorestamento, cuja liquidação pode indicar mudanças na política ambiental do estado;

SAB - Sociedade de Abastecimento de Brasília – Atuava na distribuição de produtos alimentícios e insumos, sendo descontinuada por questões operacionais e econômicas;

A análise do comportamento do número de estatais no DF ao longo do tempo permite compreender as mudanças na estrutura da administração indireta, refletindo decisões estratégicas do governo quanto à viabilidade, eficiência e necessidade dessas entidades. O acompanhamento desses processos de criação e liquidação é essencial para garantir que as empresas públicas cumpram seus objetivos de forma sustentável, promovendo serviços essenciais sem comprometer o equilíbrio fiscal do estado.

""")	

st.subheader("Empresas do Distrito Federal em 2023", divider="orange")

# Filter the dataset for companies located in Distrito Federal (DF), and from the year 2023
df_2023_df_companies = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Select relevant columns: company name (emp), sit, setor, esp, dep
df_2023_df_companies_list = df_2023_df_companies[
    ["emp", "sit", "setor", "esp", "dep"]
].sort_values(by="emp")

# Rename columns
df_2023_df_companies_list.columns = [
    "Empresa",
    "Situação",
    "Setor",
    "Natureza",
    "Dependência",
]

# Reset index to make sure DataFrame starts fresh without showing old indices
df_2023_df_companies_list.reset_index(drop=True, inplace=True)

# Style the DataFrame for a modern look
df_styled = df_2023_df_companies_list.style.set_properties(
    **{
        "background-color": "#fff",
        "color": "#333",
        "border-color": "#ccc",
        "border-style": "solid",
        "border-width": "1px",
        "padding": "10px",
        "text-align": "left",
        "font-family": "Arial, sans-serif",
        "font-size": "12px",  # Reduce the font size
    }
)

# Set table styles for headers
df_styled.set_table_styles(
    [
        {
            "selector": "thead th",
            "props": [
                ("background-color", "#007acc"),
                ("color", "white"),
                ("font-size", "14px"),
                ("text-align", "center"),
            ],
        }
    ]
)

# Display the styled dataframe
df_styled


st.subheader("Distribuição das Empresas Estatais do DF por Dependência Financeira", divider="orange")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo mostra a quantidade de estatais dependentes e não dependentes. A análise da dependência financeira das estatais do Distrito Federal revela um equilíbrio entre empresas autossuficientes e aquelas que necessitam de aportes do governo para sustentar suas operações. O gráfico correspondente, abaixo, ilustra que 27% das estatais distritais são classificadas como dependentes, o que equivale a 7 empresas do total de 26. Essa categorização é definida com base nos critérios estabelecidos pela Lei de Responsabilidade Fiscal (LRF), que determina que uma empresa estatal dependente é aquela que recebe recursos financeiros do governo controlador para cobrir despesas correntes, sejam elas relacionadas a pessoal, custeio geral ou investimentos de capital, excluídos os aportes oriundos de aumento de participação acionária.

A distinção entre empresas dependentes e não dependentes é um aspecto fundamental na gestão das estatais, pois permite compreender o impacto fiscal dessas entidades no orçamento distrital. Empresas não dependentes são aquelas que geram receitas suficientes para cobrir seus custos operacionais, não exigindo repasses do governo para manter suas atividades. Na prática, isso significa que seu funcionamento não compromete diretamente os cofres públicos, o que representa um modelo de gestão financeiramente sustentável.

Por outro lado, as empresas dependentes necessitam de suporte financeiro do tesouro distrital para cobrir suas despesas. Essa dependência pode ocorrer devido à natureza da atividade desempenhada, que pode não ser rentável sob uma ótica estritamente comercial, mas essencial para o interesse público. Serviços como saneamento, transporte público e pesquisa agropecuária, por exemplo, tendem a depender de subsídios governamentais para garantir que a população tenha acesso universal a esses serviços, independentemente de sua viabilidade econômica.

Contudo, a dependência financeira não pode ser interpretada como um indicativo isolado de ineficiência ou má gestão. Uma empresa que recebe repasses do governo não deve ser automaticamente classificada como mal administrada, pois a finalidade social da estatal precisa ser considerada na análise. Empresas que operam em setores críticos para o desenvolvimento social, como habitação e abastecimento de alimentos, podem desempenhar um papel fundamental mesmo que suas operações não sejam lucrativas. Dessa forma, a avaliação deve ir além da dependência financeira e considerar o impacto socioeconômico da estatal, suas entregas à sociedade e a eficiência na aplicação dos recursos públicos.

Entretanto, a dependência financeira não pode ser um fator irrestrito para a concessão de recursos públicos, sob o risco de comprometer a sustentabilidade fiscal do estado. O aporte de verbas governamentais precisa ser acompanhado de rigorosos mecanismos de transparência, controle e prestação de contas, garantindo que os recursos sejam empregados de forma eficiente e que os benefícios gerados para a população justifiquem os investimentos realizados. O monitoramento contínuo das finanças das estatais, aliado a auditorias independentes e relatórios detalhados, é essencial para assegurar que as empresas dependentes operem com responsabilidade fiscal, eficiência e compromisso com a melhoria da prestação de serviços públicos.

Em síntese, a dependência financeira das estatais do DF deve ser analisada sob um viés estratégico e de governança, considerando tanto a sustentabilidade econômica quanto o impacto social dessas entidades. Um modelo de gestão eficiente deve equilibrar autossuficiência financeira e a necessidade de manter serviços públicos essenciais, garantindo que os repasses do tesouro distrital sejam justificados por benefícios tangíveis para a sociedade.

""")	

# Filtrar o dataset para obter empresas localizadas no Distrito Federal (DF)
df_df = df[df["Estado"] == "DF"]

# Agrupar por 'Ano' e 'dep' (dependência) e contar o número de empresas
df_grouped = df_df.groupby(["Ano", "dep"]).size().reset_index(name="company_count")

# Criar um conjunto completo de combinações de ano e dependência
anos = df_grouped["Ano"].unique()
dependencias = ["Dependente", "Não Dependente"]

# Criar um conjunto completo de combinações de ano e dependência
complete_index = pd.MultiIndex.from_product([anos, dependencias], names=["Ano", "dep"])
df_complete = (
    df_grouped.set_index(["Ano", "dep"])
    .reindex(complete_index, fill_value=0)
    .reset_index()
)

# Calcular o total de empresas por ano
totais_anuais = df_complete.groupby("Ano")["company_count"].sum()

# Configuração da largura das barras
largura_barra = 0.35
fig, ax = plt.subplots(figsize=(10, 6))

# Posições para as barras
indice = np.arange(len(anos))

# Mapear as cores para diferentes dependências
cores = {"Dependente": "#F45046", "Não Dependente": "#007acc"}

# Plotar as barras para cada status de dependência
for i, dependencia in enumerate(dependencias):
    subset = df_complete[df_complete["dep"] == dependencia]
    barras = ax.bar(
        indice + i * largura_barra,
        subset["company_count"],
        largura_barra,
        label=dependencia,
        color=cores[dependencia],
    )

    # Adicionar os valores e porcentagens nas barras
    for j, barra in enumerate(barras):
        altura = barra.get_height()
        ano = subset.iloc[j]["Ano"]
        total_ano = totais_anuais[ano]
        porcentagem = (altura / total_ano) * 100 if total_ano > 0 else 0
        ax.annotate(
            f"{int(altura)}\n({porcentagem:.1f}%)",
            xy=(barra.get_x() + barra.get_width() / 2, altura),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

# Adicionar rótulos, título e legenda
ax.set_xlabel("Ano")
ax.set_ylabel("Número de Empresas")
ax.set_title("")
ax.set_xticks(indice + largura_barra / 2)
ax.set_xticklabels(anos)
ax.legend(title="Status de Dependência")

# Remover as bordas do gráfico
for spine in plt.gca().spines.values():
    spine.set_visible(False)

# Ajustar o layout
plt.tight_layout()

# Centralizar o gráfico com largura limitada
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    st.pyplot(fig)

st.subheader("Análise da Quantidade de Empresas Estatais por Setor no Distrito Federal", divider="orange")

st.write("""

O gráfico abaixo ilustra a distribuição das empresas estatais do Distrito Federal por setores corporativos entre 2020 e 2023. Nota-se que os setores Financeiro, Energia e Habitação e Urbanização se destacam como os mais representativos em termos de número de empresas ao longo de todo o período. O setor Financeiro mantém consistentemente seis empresas ativas, lideradas pelo grupo BRB, que diversifica suas operações em serviços bancários, seguros, cartões e investimentos. Essa estabilidade reflete a importância estratégica do setor financeiro para o desenvolvimento econômico do DF e sua robustez em termos de estrutura organizacional.

O setor de Energia, liderado pelas empresas do grupo CEB, registrou um aumento significativo no número de empresas de quatro em 2020 para cinco em 2021, e manteve esse quantitativo nos anos subsequentes. Esse crescimento está diretamente relacionado à criação de novas subsidiárias, como a CEB Geração, CEB Iluminação Pública e Serviços, e CEB Participações, reforçando o foco na expansão e segmentação dos serviços energéticos no DF. A ampliação desse setor demonstra a intenção do governo de modernizar a infraestrutura energética, diversificar as operações e melhorar a prestação de serviços públicos, principalmente em áreas críticas como iluminação e geração de energia sustentável.

O setor de Habitação e Urbanização, representado por empresas como a CODHAB e a NOVACAP, manteve três empresas ativas durante todo o período analisado, evidenciando um foco constante em projetos habitacionais e urbanísticos. Outros setores, como Transporte e Saneamento, apresentam menor número de empresas, refletindo sua concentração em operadores-chave, como o Metrô/DF e a CAESB,respectivamente. Além disso, setores como Pesquisa e Assistência Técnica Agropecuária e Gestão de Ativos mantiveram estabilidade com apenas uma empresa cada, indicando especialização e foco em nichos específicos. Em contraste, o setor de Gás e Derivados permaneceu limitado, com apenas uma empresa, a CEBGÁS, ao longo dos anos, sugerindo potencial para expansão futura, dada a crescente relevância de combustíveis alternativos e infraestrutura de gás natural no Brasil.

De forma geral, o gráfico destaca uma estrutura relativamente estável de estatais por setor no DF, com variações pontuais, como o crescimento do setor energético. Essa estabilidade é reflexo do planejamento estratégico do governo, que prioriza setores com maior impacto socioeconômico, como energia, habitação e serviços financeiros. Essa análise pode subsidiar decisões sobre possíveis reestruturações ou expansões, com foco em maximizar a eficiência operacional e o impacto das estatais no desenvolvimento local.

""")	

# Filtrar o dataset para obter empresas localizadas no Distrito Federal (DF)
df_df = df[df["Estado"] == "DF"]

# Agrupar por 'Ano' e 'setor' e contar o número de empresas
df_grouped_setor = (
    df_df.groupby(["Ano", "setor"]).size().reset_index(name="company_count")
)

# Criar um conjunto completo de combinações de ano e setor
anos = df_grouped_setor["Ano"].unique()
setores = df_grouped_setor["setor"].unique()

# Criar um conjunto completo de combinações de ano e setor
complete_index = pd.MultiIndex.from_product([anos, setores], names=["Ano", "setor"])
df_complete_setor = (
    df_grouped_setor.set_index(["Ano", "setor"])
    .reindex(complete_index, fill_value=0)
    .reset_index()
)

# Criar um gráfico colorido com Plotly Express
fig = px.bar(
    df_complete_setor, 
    x="Ano", 
    y="company_count", 
    color="setor",
    barmode="group",
    title="",
    labels={"company_count": "Número de Empresas", "Ano": "Ano", "setor": "Setor"},
    height=600
)

# Personalizar o layout
fig.update_layout(
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5,
        font=dict(color="black", size=12),  # Texto da legenda em preto
        bgcolor="white",  # Fundo da legenda em branco
        bordercolor="lightgrey",  # Borda cinza claro para melhorar a definição visual
        borderwidth=1  # Espessura da borda
    ),
    plot_bgcolor='white',
    xaxis=dict(
        tickmode='linear',
        type='category',
        tickfont=dict(color="black"),  # Cor dos rótulos do eixo X
        title_font=dict(color="black")  # Cor do título do eixo X
    ),
    yaxis=dict(
        tickfont=dict(color="black"),  # Cor dos rótulos do eixo Y
        title_font=dict(color="black")  # Cor do título do eixo Y
    ),
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial",
        font_color="black"  # Alteração na cor da fonte do hover
    )
)

# Adicionar rótulos de valores nas barras
fig.update_traces(
    texttemplate='%{y:.0f}', 
    textposition='outside',
    textfont=dict(color="black")  # Texto dos valores em preto
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)




# Botão para voltar à página inicial
if st.button("Voltar à Página Inicial"):
    st.switch_page("Início.py")
