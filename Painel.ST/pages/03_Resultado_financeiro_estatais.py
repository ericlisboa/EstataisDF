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
    page_title="Qual o resultado financeiro das estatais?",
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
    .stMarkdown p, .stMarkdown li, .stWrite {
        color: #2F2F2F !important; /* Cinza escuro legível */
        text-align: justify;
    }

    /* Garante que os números/bullets (1, 2, 3...) também fiquem escuros */
    .stMarkdown li::marker {
        color: #2F2F2F !important;
        font-weight: bold;
    }


</style>
""", unsafe_allow_html=True)

st.header("Qual o resultado financeiro das estatais?", divider="orange")

# Conteúdo específico desta página
st.write("""

Entre 2020 e 2023, os resultados financeiros das empresas estatais do Distrito Federal evidenciaram oscilações relevantes, com porangeominância de empresas lucrativas em três dos quatro anos analisados, mas registrando períodos de piora em 2021 e 2023. 

Enquanto 2020 e 2022 foram marcados por maior proporção de resultados positivos, reflexo de esforços em eficiência operacional e recuperação econômica, 2021 destacou-se pelo aumento expressivo de prejuízos, particularmente nos setores de transporte público, saneamento e assistência técnica agropecuária. 

Esse desempenho negativo pode ser associado aos impactos prolongados da pandemia de COVID-19, que comprometeram a demanda por serviços, elevaram custos operacionais e atrasaram investimentos estratégicos, especialmente em setores dependentes de subsídios governamentais.

Em 2023, embora mais da metade das estatais tenham registrado lucro, houve um aumento na proporção de empresas deficitárias, refletindo desafios estruturais e custos crescentes em setores historicamente vulneráveis. Essa evolução demonstra que, além dos efeitos remanescentes da crise sanitária, fatores econômicos e setoriais, como pressão inflacionária e limitações regulatórias, continuam a impactar o desempenho financeiro. 

O comportamento financeiro ao longo do período reforça a necessidade de aprimorar a governança corporativa, analisar as causas estruturais de prejuízos e implementar estratégias voltadas à eficiência, garantindo a sustentabilidade das estatais, especialmente nas áreas mais expostas a pressões externas e dependentes de políticas públicas.

""")	

st.subheader("Distribuição anual das empresas em relação ao lucro ou prejuízo", divider="orange")

st.subheader(":orange[**Ano de 2023**]")

# Conteúdo específico desta página
st.write("""

O ano de 2023 apresentou uma leve piora em relação ao ano anterior, com 61,54% das estatais registrando lucro e 38,46% operando com prejuízo. Essa mudança sugere a existência de desafios persistentes, possivelmente relacionados a pressões macroeconômicas, aumento de custos operacionais e limitações no modelo de financiamento de empresas dependentes. 

Setores tradicionalmente deficitários continuam a impactar negativamente os resultados agregados, reforçando a importância de uma abordagem mais estruturada para equilibrar sustentabilidade financeira e a prestação de serviços essenciais.
""")	

# Filtrar o dataset para obter empresas localizadas no Distrito Federal (DF) para o ano de 2023
df_df = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Classificar as empresas como "Lucro" ou "Prejuízo"
df_df["Resultado"] = df_df["lucros"].apply(lambda x: "Lucro" if x > 0 else "Prejuízo")

# Calcular o total de empresas
total_empresas = len(df_df)

# Contar a quantidade de empresas com lucro e prejuízo
df_resultado = df_df["Resultado"].value_counts().reset_index()
df_resultado.columns = ["Resultado", "Quantidade"]

# Calcular percentuais
df_resultado["Percentual"] = (df_resultado["Quantidade"] / total_empresas * 100).round(2)

# Adicionar coluna de empresas para exibir no hover
resultado_empresas = df_df.groupby("Resultado")["emp"].apply(list).reset_index()
df_merge = pd.merge(df_resultado, resultado_empresas, on="Resultado")
df_merge["Empresas"] = df_merge["emp"].apply(lambda x: "<br>- " + "<br>- ".join(x))

# Definir cores
colors = {"Lucro": "#007acc", "Prejuízo": "#F45046"}

# Plotar gráfico de pizza interativo com Plotly
fig = px.pie(
    df_resultado,
    values="Quantidade",
    names="Resultado",
    color="Resultado",
    color_discrete_map=colors,
    title="Distribuição de Empresas Estatais do DF em 2023",
    hover_data=["Percentual"],
    labels={"Resultado": "Resultado Financeiro", "Quantidade": "Número de Empresas"},
)

# Personalizar o layout
fig.update_traces(
    textposition="inside", 
    textinfo="percent+label",
    textfont_size=14,
    textfont_color="white",
    pull=[0, 0.1],  # Destaca a fatia "Prejuízo"
    marker=dict(line=dict(color="white", width=2)),
    hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{customdata[0]:.2f}%"
)

# Melhorar a aparência do gráfico
fig.update_layout(
    title={
        "text": "<b>Resultado Financeiro das Estatais do DF em 2023</b>",
        "y": 0.95,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
        "font": {"size": 20}
    },
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    font=dict(size=14),
    margin=dict(t=80, b=80),
    height=500,
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Mostrar detalhes das empresas em cada categoria
col1, col2 = st.columns(2)

with col1:
    empresas_lucro = df_df[df_df["Resultado"] == "Lucro"]["emp"].tolist()
    if empresas_lucro:
        st.info(f"**Empresas com Lucro ({len(empresas_lucro)}):**")
        for empresa in sorted(empresas_lucro):
            st.write(f"- {empresa}")
    else:
        st.info("Nenhuma empresa com lucro encontrada.")

with col2:
    empresas_prejuizo = df_df[df_df["Resultado"] == "Prejuízo"]["emp"].tolist()
    if empresas_prejuizo:
        st.error(f"**Empresas com Prejuízo ({len(empresas_prejuizo)}):**")
        for empresa in sorted(empresas_prejuizo):
            st.write(f"- {empresa}")
    else:
        st.error("Nenhuma empresa com prejuízo encontrada.")

# Mostrar tabela com valores detalhados (opcional)
with st.expander("Ver dados detalhados de lucro/prejuízo", expanded=False):
    # Criar um dataframe com as estatísticas para exibição
    df_detalhe = df_df[["emp", "lucros"]].sort_values(by="lucros", ascending=False).copy()
    df_detalhe.columns = ["Empresa", "Resultado Financeiro (R$)"]
    
    # Exibir a tabela formatada
    st.dataframe(
        df_detalhe,
        column_config={
            "Resultado Financeiro (R$)": st.column_config.NumberColumn(
                "Resultado Financeiro (R$)",
                format="R$ %.2f"
            )
        },
        hide_index=True,
        use_container_width=True
    )

st.subheader(":orange[**Ano de 2022**]")

# Conteúdo específico desta página
st.write("""

Em 2022, houve uma recuperação significativa no desempenho financeiro das estatais, com 69,23% das empresas apresentando lucro e apenas 30,77% registrando prejuízo. Esse aumento na proporção de empresas lucrativas pode ser atribuído a uma recuperação econômica mais ampla, combinada com esforços para melhorar a eficiência operacional e a governança das estatais. 

O desempenho positivo de setores estratégicos, como financeiro e energia, foi crucial para esse resultado. Este período reflete o impacto de políticas públicas e ajustes internos que permitiram maior estabilidade financeira.

""")	

# Filtrar o dataset para obter empresas localizadas no Distrito Federal (DF) para o ano de 2022
df_2022 = df[(df["Estado"] == "DF") & (df["Ano"] == 2022)].copy()

# Verificar se há dados para processar
if len(df_2022) == 0:
    st.warning("Não há dados de empresas para o DF no ano de 2022.")
else:
    # Classificar as empresas como "Lucro" ou "Prejuízo"
    df_2022["Resultado"] = df_2022["lucros"].apply(
        lambda x: "Lucro" if x > 0 else "Prejuízo"
    )
    
    # Calcular o total de empresas
    total_empresas = len(df_2022)
    
    # Contar a quantidade de empresas com lucro e prejuízo
    df_resultado_2022 = df_2022["Resultado"].value_counts().reset_index()
    df_resultado_2022.columns = ["Resultado", "Quantidade"]
    
    # Calcular percentuais
    df_resultado_2022["Percentual"] = (df_resultado_2022["Quantidade"] / total_empresas * 100).round(2)
    
    # Definir cores
    colors = {"Lucro": "#007acc", "Prejuízo": "#F45046"}
    
    # Plotar gráfico de pizza interativo com Plotly
    fig = px.pie(
        df_resultado_2022,
        values="Quantidade",
        names="Resultado",
        color="Resultado",
        color_discrete_map=colors,
        title="Distribuição de Empresas Estatais do DF em 2022",
        hover_data=["Percentual"],
        labels={"Resultado": "Resultado Financeiro", "Quantidade": "Número de Empresas"},
    )
    
    # Personalizar o layout
    fig.update_traces(
        textposition="inside", 
        textinfo="percent+label",
        textfont_size=14,
        textfont_color="white",
        pull=[0, 0.1],  # Destaca a fatia "Prejuízo"
        marker=dict(line=dict(color="white", width=2)),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{customdata[0]:.2f}%"
    )
    
    # Melhorar a aparência do gráfico
    fig.update_layout(
        title={
            "text": "<b>Resultado Financeiro das Estatais do DF em 2022</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",  # Corrigindo a aspas de fechamento faltante
            "font": {"size": 20}
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        font=dict(size=14),
        margin=dict(t=80, b=80),
        height=500,
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar detalhes das empresas em cada categoria
    col1, col2 = st.columns(2)
    
    with col1:
        empresas_lucro = df_2022[df_2022["Resultado"] == "Lucro"]["emp"].tolist()
        if empresas_lucro:
            st.info(f"**Empresas com Lucro ({len(empresas_lucro)}):**")
            for empresa in sorted(empresas_lucro):
                st.write(f"- {empresa}")
        else:
            st.info("Nenhuma empresa com lucro encontrada.")
    
    with col2:
        empresas_prejuizo = df_2022[df_2022["Resultado"] == "Prejuízo"]["emp"].tolist()
        if empresas_prejuizo:
            st.error(f"**Empresas com Prejuízo ({len(empresas_prejuizo)}):**")
            for empresa in sorted(empresas_prejuizo):
                st.write(f"- {empresa}")
        else:
            st.error("Nenhuma empresa com prejuízo encontrada.")
    
    # Mostrar tabela com valores detalhados (opcional)
    with st.expander("Ver dados detalhados de lucro/prejuízo", expanded=False):
        # Criar um dataframe com as estatísticas para exibição
        df_detalhe = df_2022[["emp", "lucros"]].sort_values(by="lucros", ascending=False).copy()
        df_detalhe.columns = ["Empresa", "Resultado Financeiro (R$)"]
        
        # Exibir a tabela formatada
        st.dataframe(
            df_detalhe,
            column_config={
                "Resultado Financeiro (R$)": st.column_config.NumberColumn(
                    "Resultado Financeiro (R$)",
                    format="R$ %.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )

st.subheader(":orange[**Ano de 2021**]")

# Conteúdo específico desta página
st.write("""

O ano de 2021 trouxe uma inversão preocupante no panorama, com 57,69% das estatais apresentando prejuízo, enquanto apenas 42,31% registraram lucro. Essa mudança pode estar relacionada aos impactos prolongados da pandemia e à recuperação econômica ainda lenta em setores-chave. Empresas dependentes de subsídios governamentais, como transporte público e assistência técnica agropecuária, enfrentaram maior pressão financeira. 

Este ano destacou a importância de estratégias de mitigação de riscos e revisão de modelos operacionais para melhorar a sustentabilidade das operações.

""")	

# Filtrar o dataset para obter empresas localizadas no Distrito Federal (DF) para o ano de 2021
df_2021 = df[(df["Estado"] == "DF") & (df["Ano"] == 2021)].copy()

# Verificar se há dados para processar
if len(df_2021) == 0:
    st.warning("Não há dados de empresas para o DF no ano de 2021.")
else:
    # Classificar as empresas como "Lucro" ou "Prejuízo"
    df_2021["Resultado"] = df_2021["lucros"].apply(
        lambda x: "Lucro" if x > 0 else "Prejuízo"
    )
    
    # Calcular o total de empresas
    total_empresas = len(df_2021)
    
    # Contar a quantidade de empresas com lucro e prejuízo
    df_resultado_2021 = df_2021["Resultado"].value_counts().reset_index()
    df_resultado_2021.columns = ["Resultado", "Quantidade"]
    
    # Calcular percentuais
    df_resultado_2021["Percentual"] = (df_resultado_2021["Quantidade"] / total_empresas * 100).round(2)
    
    # Definir cores
    colors = {"Lucro": "#007acc", "Prejuízo": "#F45046"}
    
    # Plotar gráfico de pizza interativo com Plotly
    fig = px.pie(
        df_resultado_2021,
        values="Quantidade",
        names="Resultado",
        color="Resultado",
        color_discrete_map=colors,
        title="Distribuição de Empresas Estatais do DF em 2021",
        hover_data=["Percentual"],
        labels={"Resultado": "Resultado Financeiro", "Quantidade": "Número de Empresas"},
    )
    
    # Personalizar o layout
    fig.update_traces(
        textposition="inside", 
        textinfo="percent+label",
        textfont_size=14,
        textfont_color="white",
        pull=[0, 0.1],  # Destaca a fatia "Prejuízo"
        marker=dict(line=dict(color="white", width=2)),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{customdata[0]:.2f}%"
    )
    
    # Melhorar a aparência do gráfico
    fig.update_layout(
        title={
            "text": "<b>Resultado Financeiro das Estatais do DF em 2021</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20}
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        font=dict(size=14),
        margin=dict(t=80, b=80),
        height=500,
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar detalhes das empresas em cada categoria
    col1, col2 = st.columns(2)
    
    with col1:
        empresas_lucro = df_2021[df_2021["Resultado"] == "Lucro"]["emp"].tolist()
        if empresas_lucro:
            st.info(f"**Empresas com Lucro ({len(empresas_lucro)}):**")
            for empresa in sorted(empresas_lucro):
                st.write(f"- {empresa}")
        else:
            st.info("Nenhuma empresa com lucro encontrada.")
    
    with col2:
        empresas_prejuizo = df_2021[df_2021["Resultado"] == "Prejuízo"]["emp"].tolist()
        if empresas_prejuizo:
            st.error(f"**Empresas com Prejuízo ({len(empresas_prejuizo)}):**")
            for empresa in sorted(empresas_prejuizo):
                st.write(f"- {empresa}")
        else:
            st.error("Nenhuma empresa com prejuízo encontrada.")
    
    # Mostrar tabela com valores detalhados (opcional)
    with st.expander("Ver dados detalhados de lucro/prejuízo", expanded=False):
        # Criar um dataframe com as estatísticas para exibição
        df_detalhe = df_2021[["emp", "lucros"]].sort_values(by="lucros", ascending=False).copy()
        df_detalhe.columns = ["Empresa", "Resultado Financeiro (R$)"]
        
        # Exibir a tabela formatada
        st.dataframe(
            df_detalhe,
            column_config={
                "Resultado Financeiro (R$)": st.column_config.NumberColumn(
                    "Resultado Financeiro (R$)",
                    format="R$ %.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )

st.subheader(":orange[**Ano de 2020**]")

# Conteúdo específico desta página
st.write("""

No ano de 2020, 63,64% das empresas registraram lucro, enquanto 36,36% operaram com prejuízo. Esse resultado reflete um equilíbrio financeiro, com a maioria das estatais apresentando resultados positivos, mesmo diante do impacto inicial da pandemia de COVID-19. Esse cenário pode ser explicado pelo desempenho robusto de setores como financeiro e imobiliário, que se destacaram pela resiliência em meio às incertezas econômicas. 

Entretanto, os resultados deficitários de uma parcela das empresas sugerem a necessidade de atenção em setores mais vulneráveis, como transporte e saneamento.

""")	

# Filtrar o dataset para obter empresas localizadas no Distrito Federal (DF) para o ano de 2020
df_2020 = df[(df["Estado"] == "DF") & (df["Ano"] == 2020)].copy()

# Verificar se há dados para processar
if len(df_2020) == 0:
    st.warning("Não há dados de empresas para o DF no ano de 2020.")
else:
    # Classificar as empresas como "Lucro" ou "Prejuízo"
    df_2020["Resultado"] = df_2020["lucros"].apply(
        lambda x: "Lucro" if x > 0 else "Prejuízo"
    )
    
    # Calcular o total de empresas
    total_empresas = len(df_2020)
    
    # Contar a quantidade de empresas com lucro e prejuízo
    df_resultado_2020 = df_2020["Resultado"].value_counts().reset_index()
    df_resultado_2020.columns = ["Resultado", "Quantidade"]
    
    # Calcular percentuais
    df_resultado_2020["Percentual"] = (df_resultado_2020["Quantidade"] / total_empresas * 100).round(2)
    
    # Definir cores
    colors = {"Lucro": "#007acc", "Prejuízo": "#F45046"}
    
    # Plotar gráfico de pizza interativo com Plotly
    fig = px.pie(
        df_resultado_2020,
        values="Quantidade",
        names="Resultado",
        color="Resultado",
        color_discrete_map=colors,
        title="Distribuição de Empresas Estatais do DF em 2020",
        hover_data=["Percentual"],
        labels={"Resultado": "Resultado Financeiro", "Quantidade": "Número de Empresas"},
    )
    
    # Personalizar o layout
    fig.update_traces(
        textposition="inside", 
        textinfo="percent+label",
        textfont_size=14,
        textfont_color="white",
        pull=[0, 0.1],  # Destaca a fatia "Prejuízo"
        marker=dict(line=dict(color="white", width=2)),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{customdata[0]:.2f}%"
    )
    
    # Melhorar a aparência do gráfico
    fig.update_layout(
        title={
            "text": "<b>Resultado Financeiro das Estatais do DF em 2020</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20}
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        font=dict(size=14),
        margin=dict(t=80, b=80),
        height=500,
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar detalhes das empresas em cada categoria
    col1, col2 = st.columns(2)
    
    with col1:
        empresas_lucro = df_2020[df_2020["Resultado"] == "Lucro"]["emp"].tolist()
        if empresas_lucro:
            st.info(f"**Empresas com Lucro ({len(empresas_lucro)}):**")
            for empresa in sorted(empresas_lucro):
                st.write(f"- {empresa}")
        else:
            st.info("Nenhuma empresa com lucro encontrada.")
    
    with col2:
        empresas_prejuizo = df_2020[df_2020["Resultado"] == "Prejuízo"]["emp"].tolist()
        if empresas_prejuizo:
            st.error(f"**Empresas com Prejuízo ({len(empresas_prejuizo)}):**")
            for empresa in sorted(empresas_prejuizo):
                st.write(f"- {empresa}")
        else:
            st.error("Nenhuma empresa com prejuízo encontrada.")
    
    # Mostrar tabela com valores detalhados (opcional)
    with st.expander("Ver dados detalhados de lucro/prejuízo", expanded=False):
        # Criar um dataframe com as estatísticas para exibição
        df_detalhe = df_2020[["emp", "lucros"]].sort_values(by="lucros", ascending=False).copy()
        df_detalhe.columns = ["Empresa", "Resultado Financeiro (R$)"]
        
        # Exibir a tabela formatada
        st.dataframe(
            df_detalhe,
            column_config={
                "Resultado Financeiro (R$)": st.column_config.NumberColumn(
                    "Resultado Financeiro (R$)",
                    format="R$ %.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )

# Após todos os gráficos, adicionar uma análise comparativa entre os anos
st.subheader("Evolução dos Resultados Financeiros (2020-2023)", divider="orange")

# Criar um dataframe resumindo a evolução ao longo dos anos
anos = [2020, 2021, 2022, 2023]
dados_anos = []

for ano in anos:
    df_ano = df[(df["Estado"] == "DF") & (df["Ano"] == ano)].copy()
    if len(df_ano) > 0:
        lucro_count = len(df_ano[df_ano["lucros"] > 0])
        prejuizo_count = len(df_ano[df_ano["lucros"] <= 0])
        total = len(df_ano)
        dados_anos.append({
            "Ano": ano,
            "Empresas com Lucro": lucro_count,
            "Empresas com Prejuízo": prejuizo_count,
            "% Lucro": round((lucro_count/total*100), 2),  # Usando a função round() em vez do método
            "% Prejuízo": round((prejuizo_count/total*100), 2)  # Usando a função round() em vez do método
        })

# Criar dataframe para visualização
df_evolucao = pd.DataFrame(dados_anos)

# Criar gráfico de linhas para mostrar a evolução
fig_evolucao = px.line(
    df_evolucao,
    x="Ano",
    y=["% Lucro", "% Prejuízo"],
    title="Evolução Percentual das Empresas com Lucro e Prejuízo (2020-2023)",
    labels={"value": "Percentual (%)", "variable": "Resultado"},
    color_discrete_map={"% Lucro": "#007acc", "% Prejuízo": "#F45046"},
    markers=True
)

# Personalizar o layout
fig_evolucao.update_layout(
    xaxis=dict(dtick=1),  # Mostrar todos os anos
    yaxis=dict(range=[0, 100]),
    legend_title_text="",
    hovermode="x unified",
    font=dict(size=14),
    height=450
)

# Exibir o gráfico de evolução
st.plotly_chart(fig_evolucao, use_container_width=True)

# Mostrar tabela resumo
st.markdown("### Resumo dos Resultados por Ano")

# Formatando o dataframe para exibição
df_exibir = df_evolucao.copy()
df_exibir["% Lucro"] = df_exibir["% Lucro"].map(lambda x: f"{x:.2f}%")
df_exibir["% Prejuízo"] = df_exibir["% Prejuízo"].map(lambda x: f"{x:.2f}%")

# Exibir tabela formatada
st.dataframe(
    df_exibir,
    column_config={
        "Ano": st.column_config.NumberColumn("Ano"),
        "Empresas com Lucro": st.column_config.NumberColumn("Empresas com Lucro"),
        "Empresas com Prejuízo": st.column_config.NumberColumn("Empresas com Prejuízo"),
        "% Lucro": st.column_config.TextColumn("% Lucro"),
        "% Prejuízo": st.column_config.TextColumn("% Prejuízo")
    },
    hide_index=True,
    use_container_width=True
)


st.subheader("Relação entre Lucro ou Prejuízo e o Patrimônio Líquido em 2023", divider="orange")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo demonstra a relação entre o lucro ou prejuízo das empresas estatais do Distrito Federal e seus respectivos patrimônios líquidos em 2023. Essa análise é essencial para avaliar a eficiência das empresas em gerar resultados financeiros positivos a partir de seus recursos patrimoniais. Empresas com maior patrimônio líquido tendem a ter maior capacidade de alavancagem operacional e financeira, o que deveria, em teoria, traduzir-se em lucros consistentes. No entanto, os resultados apresentados revelam uma diversidade significativa de desempenhos, com algumas empresas altamente lucrativas e outras registrando prejuízos, independentemente do tamanho de seus patrimônios.

Observa-se que as empresas com patrimônios líquidos elevados, representadas por pontos no extremo direito do gráfico, em sua maioria apresentam lucros consistentes. Este é o caso de empresas do setor financeiro e energético, que, devido à natureza de suas operações e à estrutura de governança robusta, conseguem maximizar a eficiência no uso de seus recursos patrimoniais. A relação positiva entre patrimônio líquido e lucro nessas empresas reforça a importância de uma gestão estratégica orientada para resultados, com foco na otimização de receitas e controle de custos.

Por outro lado, é preocupante notar a presença de empresas com patrimônio líquido orangeuzido e prejuízos recorrentes, marcadas por pontos no quadrante inferior esquerdo do gráfico. Esses casos, muitas vezes associados a setores como transporte público e assistência técnica agropecuária, evidenciam desafios estruturais significativos. As limitações na geração de receitas próprias, aliadas a custos operacionais elevados e dependência de subsídios governamentais, dificultam a sustentabilidade financeira dessas organizações. Além disso, a gestão de empresas com patrimônios líquidos negativos merece atenção especial, pois representa um risco fiscal para o Governo do Distrito Federal, sendo necessário avaliar medidas de reestruturação e melhoria operacional.

A análise reforça a importância de uma governança corporativa sólida e de estratégias diferenciadas para setores mais vulneráveis. A implementação de práticas de gestão eficientes, associada ao controle rigoroso dos custos e à diversificação de receitas, é essencial para alinhar o desempenho financeiro das empresas ao potencial representado por seus patrimônios líquidos. Em última análise, o gráfico destaca a necessidade de intervenções estratégicas em empresas defi

""")	

# Filtrar o dataset e garantir a ordem correta dos dados
df_filteorange = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Verificar a consistência removendo nulos e resetando o índice
df_filteorange_clean = df_filteorange.dropna(subset=["lucros", "PL"]).reset_index(drop=True)

# Adicionar colunas para formatação e exibição
df_filteorange_clean["Status"] = df_filteorange_clean["lucros"].apply(
    lambda lucro: "Lucro" if lucro > 0 else "Prejuízo"
)

# Adicionar informação de dependência para o hover
df_filteorange_clean["Dependência"] = df_filteorange_clean["dep"].apply(
    lambda x: "Dependente" if str(x).upper() == "DEPENDENTE" else "Não Dependente"
)

# Criar o gráfico de dispersão interativo
fig = px.scatter(
    df_filteorange_clean,
    x="PL",
    y="lucros",
    color="Status",
    size=df_filteorange_clean["PL"].abs() / df_filteorange_clean["PL"].abs().max() * 50 + 10,  
    labels={
        "PL": "Patrimônio Líquido (R$)",
        "lucros": "Lucro/Prejuízo (R$)",
        "Status": "Resultado",
        "size": "Tamanho"
    },
    color_discrete_map={
        "Lucro": "#007acc",
        "Prejuízo": "#F45046",
    },
    hover_name="emp",
    hover_data={
        "Status": True,
        "PL": ":,.2f",
        "lucros": ":,.2f",
        "Dependência": True,
    },
    title="Relação entre Patrimônio Líquido e Resultado Financeiro das Estatais do DF (2023)"
)

# Configurar hovertemplate para garantir formatação correta
fig.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "Status: %{customdata[0]}<br>"
        "Dependência: %{customdata[3]}<br>"
        "Patrimônio Líquido: R$ %{customdata[1]:,.2f}<br>"
        "Resultado: R$ %{customdata[2]:,.2f}<extra></extra>"
    ),
    marker=dict(
        line=dict(width=1, color="DarkSlateGray")
    ),
)

# Atualizar layout com melhorias nos textos e legenda
fig.update_layout(
    xaxis=dict(
        title=dict(
            text="Patrimônio Líquido (R$)",
            font=dict(size=16, color="black")
        ),
        tickfont=dict(size=14, color="black"),
        gridcolor="lightgray"
    ),
    yaxis=dict(
        title=dict(
            text="Lucro/Prejuízo (R$)",
            font=dict(size=16, color="black")
        ),
        tickfont=dict(size=14, color="black"),
        gridcolor="lightgray"
    ),
  
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.25,  # Aumentar a distância para evitar sobreposição
        xanchor="center",
        x=0.5,
        font=dict(size=14, color="black"),
        itemsizing="constant",  # Manter tamanho constante dos itens da legenda
        itemwidth=50,  # Largura dos itens da legenda
        borderwidth=1,  # Adicionar borda à legenda
        bordercolor="lightgray",
        bgcolor="rgba(255, 255, 255, 0.9)"  # Fundo levemente transparente
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=650,  # Aumentar a altura para acomodar melhor a legenda
    margin=dict(t=80, b=120, l=80, r=40),  # Aumentar margem inferior para a legenda
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial",
        font_color="black"
    ),
    showlegend=True,
)

# Adicionar linha de referência no eixo Y=0
fig.add_hline(
    y=0, 
    line_dash="dash", 
    line_color="gray", 
    annotation_text="Linha de Referência (Zero)", 
    annotation_position="bottom right",
    annotation_font=dict(size=12, color="black")
)

# Adicionar linha de referência no eixo X=0
fig.add_vline(
    x=0, 
    line_dash="dash", 
    line_color="gray", 
    annotation_text="PL Zero", 
    annotation_position="top right",
    annotation_font=dict(size=12, color="black")
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Adicionar informações complementares
with st.expander("Ver detalhes dos dados"):
    # Criar tabela com informações organizadas
    tabela_detalhe = df_filteorange_clean[["emp", "PL", "lucros", "Status", "Dependência"]].sort_values(
        by="PL", ascending=False
    ).copy()
    
    tabela_detalhe.columns = [
        "Empresa", 
        "Patrimônio Líquido (R$)", 
        "Resultado Financeiro (R$)", 
        "Status",
        "Dependência"
    ]
    
    # Exibir tabela formatada
    st.dataframe(
        tabela_detalhe,
        column_config={
            "Patrimônio Líquido (R$)": st.column_config.NumberColumn(
                "Patrimônio Líquido (R$)",
                format="R$ %.2f"
            ),
            "Resultado Financeiro (R$)": st.column_config.NumberColumn(
                "Resultado Financeiro (R$)",
                format="R$ %.2f"
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Resumo estatístico
    st.markdown("### Resumo estatístico")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Média de Patrimônio Líquido", 
            f"R$ {df_filteorange_clean['PL'].mean():,.2f}"
        )
        st.metric(
            "Empresa com maior PL", 
            df_filteorange_clean.loc[df_filteorange_clean['PL'].idxmax(), 'emp'],
            f"R$ {df_filteorange_clean['PL'].max():,.2f}"
        )
    
    with col2:
        st.metric(
            "Média de Lucro/Prejuízo", 
            f"R$ {df_filteorange_clean['lucros'].mean():,.2f}"
        )
        st.metric(
            "Empresa mais lucrativa", 
            df_filteorange_clean.loc[df_filteorange_clean['lucros'].idxmax(), 'emp'],
            f"R$ {df_filteorange_clean['lucros'].max():,.2f}"
        )


st.subheader("Rentabilidade das empresas em 2023 - (Lucro ou Prejuízo / Patrimônio Líquido)", divider="orange")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo evidencia a rentabilidade das empresas estatais do Distrito Federal em 2023, medida pela relação entre lucro ou prejuízo e patrimônio líquido. Empresas como CEB Participações, CEB Lajeado e CAESB destacaram-se com as maiores rentabilidades, demonstrando eficiência na utilização de seus ativos para gerar retornos financeiros positivos. Esses resultados refletem estratégias de gestão sólidas, otimização de processos operacionais e modelos de negócios ajustados à demanda do mercado. O destaque do setor energético e do saneamento reforça o impacto de serviços essenciais com forte capacidade de geração de receitas, mesmo em um cenário econômico desafiador.

No entanto, o gráfico também expõe pontos críticos relacionados a empresas com rentabilidade negativa, como a DF Gestão de Ativos, que apresentou o desempenho mais preocupante, com valores muito abaixo do esperado. Essa baixa rentabilidade pode ser atribuída a uma combinação de desafios estruturais, falta de estratégias claras de geração de receita e possível subutilização de ativos. Outras empresas com resultados negativos incluem a CODHAB, o Metrô/DF e a CEB Iluminação Pública e Serviços, setores historicamente desafiadores, dada sua dependência de subsídios governamentais e altos custos operacionais. Esses desempenhos deficitários destacam a necessidade de reavaliações estratégicas, orangeução de ineficiências e implementação de melhorias na gestão.

A análise geral revela um panorama de contraste entre empresas altamente rentáveis e aquelas em dificuldades financeiras, reforçando a necessidade de políticas diferenciadas para cada caso. Empresas com bom desempenho devem continuar investindo na ampliação de suas operações e inovação, enquanto aquelas com rentabilidade negativa requerem intervenções específicas, como reestruturação, diversificação de receitas e maior eficiência nos custos operacionais. Esses ajustes são essenciais para garantir a sustentabilidade e o impacto positivo das estatais no desenvolvimento econômico e social do Distrito Federal.

Alguns pontos adicionais que complementam a análise sistêmica das empresas:

I. Disparidade na Rentabilidade: O gráfico mostra uma disparidade acentuada entre empresas com alta rentabilidade e aquelas com resultados negativos. Essa diferença destaca a necessidade de aprofundar a análise das políticas setoriais e dos modelos de gestão. Empresas de setores essenciais, como transporte e habitação, muitas vezes operam com foco em atender políticas públicas, o que pode impactar negativamente sua rentabilidade, mas reforça sua relevância social. Esse trade-off entre sustentabilidade financeira e impacto social deve ser avaliado de forma integrada.

II. Impacto Setorial e Subsídios: Empresas de setores como transporte e habitação (e.g., Metrô/DF, CODHAB) enfrentam desafios estruturais decorrentes de sua dependência de subsídios governamentais e pressão para manter tarifas acessíveis. Essa condição pode justificar parcialmente os resultados negativos, mas reforça a necessidade de buscar alternativas sustentáveis, como parcerias público-privadas (PPPs), modernização tecnológica e revisão de custos operacionais.

III. Governança e Impacto nos Resultados: Um ponto que merece destaque é o papel da governança corporativa na determinação desses resultados. Empresas com estrutura de governança mais robusta tendem a apresentar maior capacidade de adaptação às pressões econômicas e regulatórias, o que pode explicar o desempenho positivo de algumas estatais, como as do setor energético. Investir no fortalecimento da governança, especialmente nas empresas deficitárias, pode ser uma estratégia para melhorar seus resultados financeiros.

Instituto BRB e BRB Administradora e Corretora de Seguros não aparecem no gráfico pois possuem dados faltantes. Além disso, foram desconsideradas as empresas com patrimônio líquido negativo:

CEBGAS - Companhia Brasiliense de Gás

CODEPLAN - Companhia de Planejamento do Distrito Federal

EMATER - Empresa de Assistência Técnica e Extensão Rural do Distrito Federal

SAB - Sociedade de Abastecimento de Brasília

""")	

# Filtrar o dataframe para incluir apenas o Estado DF e Ano 2023
df_filteorange = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Remover linhas com valores NaN nas colunas necessárias e PL negativo
df_filteorange = df_filteorange.dropna(subset=["lucros", "PL"])
df_filteorange = df_filteorange[df_filteorange["PL"] > 0]  # Remover empresas com PL negativo ou zero

# Calcular Rentabilidade (%)
df_filteorange["Rentabilidade (%)"] = (df_filteorange["lucros"] / df_filteorange["PL"]) * 100

# Adicionar uma coluna para indicar se é lucro ou prejuízo
df_filteorange["Status"] = df_filteorange["Rentabilidade (%)"].apply(
    lambda x: "Rentabilidade Positiva" if x >= 0 else "Rentabilidade Negativa"
)

# Ordenar o dataframe pela rentabilidade
df_filteorange.sort_values(by="Rentabilidade (%)", ascending=True, inplace=True)

# Adicionar informação de dependência para o hover
df_filteorange["Dependência"] = df_filteorange["dep"].apply(
    lambda x: "Dependente" if str(x).upper() == "DEPENDENTE" else "Não Dependente"
)

# Criação do gráfico de barras
fig = px.bar(
    df_filteorange,
    x="Rentabilidade (%)",
    y="emp",
    orientation="h",
    color="Status",
    color_discrete_map={
        "Rentabilidade Positiva": "#007acc", 
        "Rentabilidade Negativa": "#F45046"
    },
    hover_data={
        "Rentabilidade (%)": ":.2f", 
        "lucros": ":,.2f", 
        "PL": ":,.2f",
        "Dependência": True,
        "Status": False
    },
    labels={
        "emp": "Empresa", 
        "Rentabilidade (%)": "Rentabilidade (%)",
        "lucros": "Lucro/Prejuízo (R$)",
        "PL": "Patrimônio Líquido (R$)"
    },
    title="Rentabilidade das Empresas Estatais do DF em 2023",
    text="Rentabilidade (%)"  # Adicionar valor da rentabilidade em cada barra
)

# Personalizar o texto nas barras
fig.update_traces(
    texttemplate="%{x:.1f}%",
    textposition="outside",
    textfont=dict(size=12, color="black"),
    cliponaxis=False,  # Permitir que o texto seja exibido fora do eixo
)

# Formatando o hovertemplate para exibir valores de forma mais amigável
fig.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Rentabilidade: %{x:.2f}%<br>"
        "Lucro/Prejuízo: R$ %{customdata[0]:,.2f}<br>"
        "Patrimônio Líquido: R$ %{customdata[1]:,.2f}<br>"
        "Dependência: %{customdata[2]}<extra></extra>"
    )
)

# Linha de referência em 0%
fig.add_vline(
    x=0, 
    line_dash="dash", 
    line_color="gray",
    annotation_text="Linha de Rentabilidade Zero",
    annotation_position="top"
)

# Melhorar o layout do gráfico
fig.update_layout(
    height=650,  # Altura adaptativa com base no número de empresas
    plot_bgcolor="white",
    paper_bgcolor="white",
    title={
        "text": "<b>Rentabilidade das Empresas Estatais do DF em 2023</b>",
        "y": 0.98,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
        "font": {"size": 20, "color": "black"}
    },
    xaxis=dict(
        title=dict(text="Rentabilidade (%)", font=dict(size=14, color="black")),
        tickfont=dict(size=12, color="black"),
        gridcolor="lightgray",
        zerolinecolor="black",
        zerolinewidth=1.5
    ),
    yaxis=dict(
        title=dict(text="Empresa", font=dict(size=14, color="black")),
        tickfont=dict(size=12, color="black"),
        gridcolor="white"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(size=12, color="black"),
        borderwidth=1,
        bordercolor="lightgray"
    ),
    margin=dict(l=50, r=50, t=80, b=80)
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Adicionar informações complementares
with st.expander("📊 Ver detalhes da rentabilidade"):
    # Calcular estatísticas
    media_rentabilidade = df_filteorange["Rentabilidade (%)"].mean()
    rentabilidade_positiva = df_filteorange[df_filteorange["Rentabilidade (%)"] > 0]["Rentabilidade (%)"].mean()
    rentabilidade_negativa = df_filteorange[df_filteorange["Rentabilidade (%)"] < 0]["Rentabilidade (%)"].mean()
    
    # Exibir estatísticas
    st.markdown("### Estatísticas de rentabilidade")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Média geral de rentabilidade", 
            f"{media_rentabilidade:.2f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            "Média das rentabilidades positivas", 
            f"{rentabilidade_positiva:.2f}%",
            delta="positivo", 
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Média das rentabilidades negativas", 
            f"{rentabilidade_negativa:.2f}%",
            delta="negativo", 
            delta_color="inverse"
        )
    
    # Tabela detalhada
    st.markdown("### Dados detalhados")
    tabela = df_filteorange[["emp", "Rentabilidade (%)", "lucros", "PL", "Status", "Dependência"]].copy()
    tabela.columns = ["Empresa", "Rentabilidade (%)", "Lucro/Prejuízo (R$)", "Patrimônio Líquido (R$)", "Status", "Dependência"]
    
    # Ordenar por rentabilidade (maior para menor)
    tabela = tabela.sort_values(by="Rentabilidade (%)", ascending=False)
    
    # Exibir tabela formatada
    st.dataframe(
        tabela,
        column_config={
            "Rentabilidade (%)": st.column_config.NumberColumn(
                "Rentabilidade (%)", 
                format="%.2f%%"
            ),
            "Lucro/Prejuízo (R$)": st.column_config.NumberColumn(
                "Lucro/Prejuízo (R$)",
                format="R$ %.2f"
            ),
            "Patrimônio Líquido (R$)": st.column_config.NumberColumn(
                "Patrimônio Líquido (R$)",
                format="R$ %.2f"
            )
        },
        hide_index=True,
        use_container_width=True
    )


st.subheader("Rentabilidade média das empresas por setor em 2023 (Lucro ou Prejuízo / Patrimônio Líquido)", divider="orange")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo, de rentabilidade média das empresas estatais do Distrito Federal em 2023, por setor, reflete a eficiência na utilização do patrimônio líquido para gerar resultados financeiros positivos ou negativos. Os setores de saneamento, energia e financeiro destacaram-se positivamente, apresentando os melhores índices de rentabilidade média. O setor de saneamento, liderado pela CAESB, alcançou o topo do ranking, evidenciando a robustez da gestão operacional e a relevância estratégica de serviços essenciais bem estruturados. Já os setores de energia e financeiro, com destaque para o grupo CEB e o BRB, respectivamente, demonstraram grande capacidade de geração de receita em contextos econômicos desafiadores, reforçando a maturidade na gestão dos ativos e a diversificação dos modelos de negócio.

Por outro lado, o setor de gestão de ativos registrou o pior desempenho, com uma rentabilidade média extremamente negativa. Essa situação pode ser atribuída a desafios estruturais e operacionais enfrentados pela DF Gestão de Ativos, que sofre com a baixa utilização de seu patrimônio e modelos de negócios ineficazes. O desempenho negativo desse setor é um alerta para a necessidade de reestruturação e estratégias voltadas à valorização e melhor uso dos ativos administrados, buscando reverter prejuízos e aumentar a sustentabilidade financeira.

Os setores de habitação e urbanização, transporte e abastecimento de alimentos também apresentaram resultados negativos, mas em menor magnitude quando comparados ao setor de gestão de ativos. A CODHAB e o Metrô/DF, líderes nesses setores, operam em áreas altamente dependentes de subsídios governamentais, enfrentando dificuldades para alinhar a prestação de serviços sociais às exigências de rentabilidade financeira. Esses resultados sugerem a necessidade de políticas públicas e intervenções estratégicas que equilibrem o impacto social e a eficiência financeira, garantindo a continuidade e melhoria dos serviços essenciais para a população.

Em síntese, a análise de rentabilidade média por setor em 2023 evidencia disparidades significativas no desempenho das estatais distritais, reforçando a importância de estratégias específicas para cada setor. Setores lucrativos devem continuar investindo em inovação e expansão, enquanto setores deficitários necessitam de reformas estruturais e melhorias na governança para superar os desafios financeiros e operacionais. Essa abordagem permitirá maior equilíbrio entre a sustentabilidade financeira das empresas e seu papel estratégico no desenvolvimento econômico e social do Distrito Federal.

Instituto BRB e BRB Administradora e Corretora de Seguros não aparecem no gráfico pois possuem dados faltantes. Além disso, foram desconsideradas as empresas com patrimônio líquido negativo:

CEBGAS - Companhia Brasiliense de Gás

CODEPLAN - Companhia de Planejamento do Distrito Federal

EMATER - Empresa de Assistência Técnica e Extensão Rural do Distrito Federal

SAB - Sociedade de Abastecimento de Brasília

""")	

# Filtrar o dataframe para incluir apenas o Estado DF e Ano 2023
df_filteorange = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Remover linhas com valores NaN nas colunas necessárias e desconsiderar PL negativo
df_filteorange = df_filteorange.dropna(subset=["lucros", "PL", "setor"])
df_filteorange = df_filteorange[df_filteorange["PL"] > 0]  # Excluir empresas com PL negativo

# Calcular Rentabilidade (%)
df_filteorange["Rentabilidade (%)"] = (df_filteorange["lucros"] / df_filteorange["PL"]) * 100

# Agrupar por setor e calcular a média de rentabilidade e compilar a lista de empresas
df_grouped = (
    df_filteorange.groupby("setor")
    .agg(
        Rentabilidade_medio=("Rentabilidade (%)", "mean"),
        Lucros_total=("lucros", "sum"),
        PL_total=("PL", "sum"),
        empresas=("emp", lambda x: list(x)),
        num_empresas=("emp", "count")
    )
    .reset_index()
)

# Adicionar uma coluna para status da rentabilidade
df_grouped["Status"] = df_grouped["Rentabilidade_medio"].apply(
    lambda x: "Rentabilidade Positiva" if x >= 0 else "Rentabilidade Negativa"
)

# Criar coluna com lista de empresas para exibição no hover
df_grouped["empresas_list"] = df_grouped["empresas"].apply(lambda x: ", ".join(x))

# Ordenar o dataframe pela rentabilidade média
df_grouped.sort_values(by="Rentabilidade_medio", ascending=True, inplace=True)

# Criação do gráfico de barras por setor
fig = px.bar(
    df_grouped,
    x="Rentabilidade_medio",
    y="setor",
    orientation="h",
    color="Status",
    color_discrete_map={
        "Rentabilidade Positiva": "#007acc", 
        "Rentabilidade Negativa": "#F45046"
    },
    hover_data={
        "Rentabilidade_medio": ":.2f",
        "Lucros_total": ":,.2f",
        "PL_total": ":,.2f",
        "empresas_list": True,
        "num_empresas": True,
        "Status": False
    },
    labels={
        "setor": "Setor",
        "Rentabilidade_medio": "Rentabilidade Média (%)",
        "Lucros_total": "Lucros Totais (R$)",
        "PL_total": "Patrimônio Líquido Total (R$)",
        "empresas_list": "Empresas",
        "num_empresas": "Número de Empresas"
    },
    text="Rentabilidade_medio"  # Adicionar valor na barra
)

# Personalizar o texto nas barras
fig.update_traces(
    texttemplate="%{x:.1f}%",
    textposition="outside",
    textfont=dict(size=12, color="black"),
    cliponaxis=False,  # Permitir que o texto seja exibido fora do eixo
)

# Formatando o hovertemplate para exibir valores de forma mais amigável
fig.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Rentabilidade Média: %{x:.2f}%<br>"
        "Lucros Totais: R$ %{customdata[0]:,.2f}<br>"
        "Patrimônio Líquido Total: R$ %{customdata[1]:,.2f}<br>"
        "Empresas (%{customdata[3]}): %{customdata[2]}<extra></extra>"
    )
)

# Linha de referência em 0%
fig.add_vline(
    x=0, 
    line_dash="dash", 
    line_color="gray",
    annotation_text="Rentabilidade Zero",
    annotation_position="top"
)

# Melhorar o layout do gráfico
fig.update_layout(
    height=500,
    plot_bgcolor="white",
    paper_bgcolor="white",
    title={
        "text": "<b>Rentabilidade Média por Setor das Empresas Estatais do DF em 2023</b>",
        "y": 0.98,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
        "font": {"size": 20, "color": "black"}
    },
    xaxis=dict(
        title=dict(
            text="Rentabilidade Média (%)", 
            font=dict(size=14, color="black"),
            standoff=25  # Aumentar a distância entre o título do eixo e os números
        ),
        tickfont=dict(size=12, color="black"),
        gridcolor="lightgray",
        zerolinecolor="black",
        zerolinewidth=1.5
    ),
    yaxis=dict(
        title=dict(text="Setor", font=dict(size=14, color="black")),
        tickfont=dict(size=12, color="black"),
        gridcolor="white"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.30,  # Aumentar significativamente a distância da legenda
        xanchor="center",
        x=0.5,
        font=dict(size=12, color="black"),
        borderwidth=1,
        bordercolor="lightgray",
        bgcolor="rgba(255, 255, 255, 0.9)"  # Adicionar um fundo semi-transparente
    ),
    margin=dict(l=50, r=80, t=80, b=150)  # Aumentar significativamente a margem inferior
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Adicionar informações complementares
with st.expander("📊 Ver detalhes da rentabilidade por setor"):
    # Calcular estatísticas
    setores_positivos = df_grouped[df_grouped["Rentabilidade_medio"] > 0]
    setores_negativos = df_grouped[df_grouped["Rentabilidade_medio"] < 0]
    
    # Métricas gerais
    st.markdown("### Estatísticas de rentabilidade por setor")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total de setores analisados", 
            f"{len(df_grouped)}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Setores com rentabilidade positiva", 
            f"{len(setores_positivos)}",
            delta=f"{len(setores_positivos)/len(df_grouped)*100:.1f}%", 
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Setores com rentabilidade negativa", 
            f"{len(setores_negativos)}",
            delta=f"{len(setores_negativos)/len(df_grouped)*100:.1f}%", 
            delta_color="inverse"
        )
    
    # Tabela detalhada
    st.markdown("### Detalhamento por setor")
    
    # Preparar dados para a tabela
    tabela_setores = df_grouped.copy()
    tabela_setores["Empresas"] = tabela_setores["empresas_list"]
    tabela_setores = tabela_setores[["setor", "Rentabilidade_medio", "Lucros_total", "PL_total", "num_empresas", "Empresas"]]
    tabela_setores.columns = ["Setor", "Rentabilidade Média (%)", "Lucros Totais (R$)", "Patrimônio Líquido Total (R$)", "Número de Empresas", "Empresas"]
    
    # Ordenar por rentabilidade (maior para menor)
    tabela_setores = tabela_setores.sort_values(by="Rentabilidade Média (%)", ascending=False)
    
    # Exibir tabela formatada
    st.dataframe(
        tabela_setores,
        column_config={
            "Rentabilidade Média (%)": st.column_config.NumberColumn(
                "Rentabilidade Média (%)", 
                format="%.2f%%"
            ),
            "Lucros Totais (R$)": st.column_config.NumberColumn(
                "Lucros Totais (R$)",
                format="R$ %.2f"
            ),
            "Patrimônio Líquido Total (R$)": st.column_config.NumberColumn(
                "Patrimônio Líquido Total (R$)",
                format="R$ %.2f"
            ),
            "Número de Empresas": st.column_config.NumberColumn(
                "Número de Empresas"
            ),
            "Empresas": st.column_config.TextColumn(
                "Empresas", 
                width="large"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Mostrar informações adicionais sobre o setor mais e menos rentável
    st.markdown("### Destaques")
    col1, col2 = st.columns(2)
    
    with col1:
        setor_mais_rentavel = tabela_setores.iloc[0]
        st.success(f"**Setor mais rentável: {setor_mais_rentavel['Setor']}**")
        st.write(f"Rentabilidade média: **{setor_mais_rentavel['Rentabilidade Média (%)']:.2f}%**")
        st.write(f"Empresas: {setor_mais_rentavel['Empresas']}")
    
    with col2:
        setor_menos_rentavel = tabela_setores.iloc[-1]
        st.error(f"**Setor menos rentável: {setor_menos_rentavel['Setor']}**")
        st.write(f"Rentabilidade média: **{setor_menos_rentavel['Rentabilidade Média (%)']:.2f}%**")
        st.write(f"Empresas: {setor_menos_rentavel['Empresas']}")



# Botão para voltar à página inicial
if st.button("Voltar à Página Inicial"):
    st.switch_page("Início.py")
