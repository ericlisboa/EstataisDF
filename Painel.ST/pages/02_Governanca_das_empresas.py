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
    page_title="Como é a governança das empresas?",
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
st.header("Como é a governança das empresas?", divider="orange")

# Conteúdo específico desta página
st.write("""

A governança corporativa é essencial para as empresas, pois proporciona uma estrutura de regras, práticas e processos que orientam a direção e o controle delas. Geralmente, a governança efetiva leva a uma melhor tomada de decisões, maior transparência, e maior confiança dos investidores e do público em geral. Para estatais, particularmente, a boa governança assegura que as práticas de gestão estejam alinhadas com os interesses públicos e em conformidade com as políticas governamentais.

**Conselho de Administração**  
O Conselho de Administração é um componente central da governança corporativa, responsável por definir a direção estratégica da empresa. Composto por membros que trazem uma diversidade de experiências e perspectivas, este conselho tem a tarefa de supervisionar as operações e garantir que a gestão esteja trabalhando para alcançar os interesses dos acionistas e outros stakeholders. Ele fornece orientação sobre grandes decisões estratégicas e avalia o desempenho da equipe de gestão.

**Conselho Fiscal**  
O Conselho Fiscal tem como principal missão a fiscalização das responsabilidades financeiras e de contabilidade da empresa. Ele funciona como uma salvaguarda independente, garantindo que os gastos sejam apropriados e que as práticas contábeis estejam em conformidade com normas e regulamentos. Ao fazer isso, ele reduz os riscos de fraudes e promove a transparência nos relatórios financeiros, reforçando a confiança dos acionistas e do público.

**Comitê de Auditoria**  
O Comitê de Auditoria trabalha em estreita colaboração com o Conselho Fiscal, desempenhando um papel crucial no fortalecimento dos controles internos da empresa. Este comitê é responsável por revisar e supervisionar os processos de auditoria interna e externa, além de assegurar que a empresa adote práticas de gerenciamento de riscos eficazes. Ao identificar e abordar potenciais problemas antes que se tornem significativos, o Comitê de Auditoria contribui para a saúde financeira sustentável da empresa.

Em conjunto, esses componentes de governança fortalecem a resiliência operativa e financeira da empresa, alinhando suas atividades com as melhores práticas de mercado e regulatórias. Eles formam um sistema de freios e contrapesos que, quando bem implementado, maximiza o valor para acionistas e outros interessados, ao mesmo tempo que mitiga riscos potenciais.

""")	

st.subheader("Quantitativo de Governança Corporativa nas Empresas Estatais do Distrito Federal em 2023", divider="")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo ilustra o quantitativo de empresas estatais do Distrito Federal que adotaram diferentes estruturas de governança corporativa em 2023, destacando a presença de Conselhos de Administração, Conselhos Fiscais e Comitês de Auditoria. O destaque vai para o Conselho Fiscal, implementado em 96,2% das estatais (25 empresas), indicando um compromisso com a fiscalização contínua e a transparência das operações financeiras. Essa estrutura desempenha um papel central na supervisão da gestão financeira, reduzindo riscos de fraudes e desvios, além de assegurar que as práticas contábeis estejam em conformidade com as regulamentações aplicáveis.

Já o Conselho de Administração, presente em 84,6% das estatais (22 empresas), reforça a governança estratégica dessas organizações. Esse órgão é responsável por definir as diretrizes de longo prazo, avaliar o desempenho dos gestores e assegurar que as ações das empresas estejam alinhadas aos objetivos e metas estabelecidas pelo Governo do Distrito Federal. A ampla adoção do Conselho de Administração é um indicativo positivo de que a maioria das estatais busca equilibrar seus objetivos financeiros e sociais com práticas modernas de gestão corporativa.

Por outro lado, o Comitê de Auditoria, embora presente em apenas 38,5% das estatais (10 empresas), desempenha uma função crítica para o fortalecimento da governança. Esse comitê é responsável por garantir a integridade dos controles internos, monitorar os riscos corporativos e revisar relatórios financeiros com imparcialidade. A menor adoção desse órgão pode ser vista como uma oportunidade de melhoria, uma vez que o Comitê de Auditoria agrega valor à supervisão dos processos e aumenta a confiança de investidores e stakeholders no desempenho das estatais.

De maneira geral, o panorama apresentado pelo gráfico demonstra avanços significativos na governança corporativa das empresas estatais do DF. No entanto, há espaço para evolução, especialmente na ampliação da implementação de Comitês de Auditoria. Fortalecer as estruturas de governança com a adoção universal dessas práticas contribuirá para maior eficiência administrativa, mitigação de riscos e alinhamento às melhores práticas de mercado. O compromisso com a transparência e a accountability continuará sendo essencial para sustentar a confiança pública e garantir o cumprimento do papel estratégico das estatais no desenvolvimento do Distrito Federal.

""")	

# Filtrar os dados para o Estado DF e ano de 2023
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)]

# Contar o número de empresas para cada tipo de estrutura de governança
contagem_conselho_admin = df_filtrado["gov_ca"].str.upper().eq("SIM").sum()
contagem_conselho_fiscal = df_filtrado["gov_cf"].str.upper().eq("SIM").sum()
contagem_comite_auditoria = df_filtrado["gov_aud"].str.upper().eq("SIM").sum()

# Calcular o número total de empresas
total_empresas = len(df_filtrado)

# Criar um DataFrame com os dados de contagem
dados_contagem = pd.DataFrame(
    {
        "Estrutura de Governança": [
            "Conselho de Administração",
            "Conselho Fiscal",
            "Comitê de Auditoria",
        ],
        "Número de Empresas": [
            contagem_conselho_admin,
            contagem_conselho_fiscal,
            contagem_comite_auditoria,
        ],
    }
)

# Calcular a porcentagem de empresas para cada tipo de estrutura
dados_contagem["Porcentagem (%)"] = (
    dados_contagem["Número de Empresas"] / total_empresas
) * 100

# Opção 1: Gráfico com Plotly (interativo)
fig = px.bar(
    dados_contagem, 
    x="Estrutura de Governança", 
    y="Número de Empresas",
    text="Número de Empresas",
    color="Estrutura de Governança",
    color_discrete_map={
        "Conselho de Administração": "#007acc",
        "Conselho Fiscal": "#008846",
        "Comitê de Auditoria": "#F45046"
    }
)

# Personalizar o layout do gráfico
fig.update_layout(
    title_text="",
    xaxis_title="Estrutura de Governança",
    yaxis_title="Número de Empresas",
    showlegend=False,
    plot_bgcolor="white",
    font=dict(size=12, color="black"),
    margin=dict(l=20, r=20, t=30, b=20),
)

# Adicionar as porcentagens aos textos das barras
fig.update_traces(
    texttemplate="%{y}<br>(%{customdata:.1f}%)",
    textposition="outside",
    textfont=dict(color="black", size=12),
    customdata=dados_contagem["Porcentagem (%)"]
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Opcional: Exibir os dados em uma tabela
st.dataframe(
    dados_contagem.sort_values("Número de Empresas", ascending=False),
    column_config={
        "Porcentagem (%)": st.column_config.NumberColumn(
            "Porcentagem (%)",
            format="%.1f%%"
        )
    },
    hide_index=True,
    use_container_width=True
)


st.subheader("Análise da Distribuição de Empresas por Combinação de Estruturas de Governança em 2023", divider="")

# Conteúdo específico desta página
st.write("""

O gráfico a seguir ilustra as combinações de estruturas de governança presentes nas empresas estatais do Distrito Federal em 2023. Dentre as combinações avaliadas, a presença conjunta de Conselho de Administração (CA) e Conselho Fiscal (CF) foi a mais comum, adotada por 13 empresas, representando uma maioria significativa. Esse resultado demonstra o compromisso da maioria das estatais em estruturar sua governança com as bases mínimas necessárias para supervisão estratégica e fiscalização financeira, promovendo maior accountability e alinhamento às boas práticas de governança corporativa.

A combinação mais robusta e instrumentos de governança, que inclui Conselho de Administração, Conselho Fiscal e Comitê de Auditoria (CA, CF, COAUD), foi adotada por 9 empresas. Essa configuração é considerada ideal, pois abrange os três pilares fundamentais da governança corporativa, permitindo maior controle interno, supervisão estratégica e mitigação de riscos financeiros. A implementação dessa estrutura demonstra maturidade em governança por parte dessas estatais, pois o Comitê de Auditoria desempenha um papel essencial ao revisar processos financeiros e monitorar a gestão de riscos, fortalecendo a confiança de stakeholders.

Outras configurações, como empresas que possuem apenas o Conselho Fiscal (CF) ou uma combinação de Conselho Fiscal e Comitê de Auditoria (CF, COAUD), foram menos recorrentes, representando 2 e 1 empresa, respectivamente. Notavelmente, apenas uma empresa não possui qualquer estrutura de governança registrada, o que é uma exceção preocupante, dado o potencial impacto dessa lacuna na supervisão e controle. Esse cenário sugere que, embora a maioria das empresas estatais tenha avançado na consolidação de suas estruturas de governança, ainda há espaço para melhorias, especialmente na ampliação da presença do Comitê de Auditoria, que agrega valor à gestão e à transparência.

O gráfico reflete a diversidade nas práticas de governança adotadas pelas estatais do DF, destacando avanços importantes na adoção de estruturas combinadas. Contudo, há oportunidades de aprimoramento, principalmente no fortalecimento das configurações mais completas, garantindo que todas as empresas tenham governança compatível com seu impacto estratégico e financeiro. A ampliação dessas práticas consolidará a credibilidade e a eficiência do setor público distrital.

""")	

# Filtrar os dados para o Estado DF e ano de 2023
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Definir uma função para categorizar as combinações de governança usando abreviações
def categorizar_combinacoes(row):
    ca = row["gov_ca"].upper() == "SIM"
    cf = row["gov_cf"].upper() == "SIM"
    aud = row["gov_aud"].upper() == "SIM"

    if ca and cf and aud:
        return "CA, CF, COAUD"
    elif ca and cf:
        return "CA, CF"
    elif ca and aud:
        return "CA, COAUD"
    elif cf and aud:
        return "CF, COAUD"
    elif ca:
        return "CA"
    elif cf:
        return "CF"
    elif aud:
        return "COAUD"
    else:
        return "Nenhum"

# Aplicar função de categorização
df_filtrado.loc[:, "Combinação"] = df_filtrado.apply(categorizar_combinacoes, axis=1)

# Contar números de empresas e agrupar por combinação, além de concatenar nomes das empresas
dados_contagem = (
    df_filtrado.groupby("Combinação")
    .agg({"emp": lambda x: "<br>".join(x), "Combinação": "size"})
    .rename(columns={"Combinação": "Número de Empresas", "emp": "Lista de Empresas"})
    .reset_index()
)

# Calcular a porcentagem de empresas para cada tipo de estrutura
dados_contagem["Porcentagem (%)"] = (
    dados_contagem["Número de Empresas"] / len(df_filtrado)
) * 100

# Ordenar as combinações por frequência (opcional)
dados_contagem = dados_contagem.sort_values(by="Número de Empresas", ascending=False)

# Criar gráfico interativo com plotly
fig = px.bar(
    dados_contagem,
    x="Combinação",
    y="Número de Empresas",
    text="Número de Empresas",
    labels={
        "Combinação": "Combinação de Estrutura de Governança",
        "Número de Empresas": "Número de Empresas",
    },
    hover_data={"Lista de Empresas": True, "Porcentagem (%)": ":.1f"},
    color="Combinação",
    color_discrete_sequence=px.colors.qualitative.Bold,
    height=500
)

# Atualizar template de hover para incluir empresas
fig.update_traces(
    hovertemplate=(
        "<b>Combinação:</b> %{x}<br>"
        "<b>Número de Empresas:</b> %{y}<br>"
        "<b>Empresas:</b> <br>%{customdata[0]}<br>"
        "<b>Porcentagem:</b> %{customdata[1]:.1f}%<extra></extra>"
    ),
    textposition="outside",
    textfont=dict(color="black", size=12)
)

# Adicionar legenda explicativa
fig.add_annotation(
    x=0.5,
    y=1.05,
    xref="paper",
    yref="paper",
    text="Legenda: CA = Conselho de Administração, CF = Conselho Fiscal, COAUD = Comitê de Auditoria",
    font=dict(size=11, color="black"),
    showarrow=False,
    align="center"
)

# Personalizar layout
fig.update_layout(
    xaxis_title="Combinação de Estrutura de Governança",
    yaxis_title="Número de Empresas",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=60, b=20, l=20, r=20),
    xaxis=dict(
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    ),
    yaxis=dict(
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial",
        font_color="black"
    )
)

# Mostrar o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Exibir tabela com detalhes para consulta (opcional - pode ser expandido/contraído)
with st.expander("Ver detalhes das combinações de estruturas de governança"):
    # Criar uma versão mais legível da tabela para exibição
    tabela_exibir = dados_contagem.copy()
    tabela_exibir["Lista de Empresas"] = tabela_exibir["Lista de Empresas"].str.replace("<br>", ", ")
    
    # Exibir tabela formatada
    st.dataframe(
        tabela_exibir,
        column_config={
            "Porcentagem (%)": st.column_config.NumberColumn(
                "Porcentagem (%)",
                format="%.1f%%"
            ),
            "Lista de Empresas": st.column_config.TextColumn(
                "Empresas"
            )
        },
        hide_index=True,
        use_container_width=True
    )

    # Explicação detalhada das combinações
    st.markdown("""
    ### Significado das combinações:
    - **CA, CF, COAUD**: Empresas com Conselho de Administração, Conselho Fiscal e Comitê de Auditoria
    - **CA, CF**: Empresas com Conselho de Administração e Conselho Fiscal
    - **CF, COAUD**: Empresas com Conselho Fiscal e Comitê de Auditoria
    - **CA**: Empresas apenas com Conselho de Administração
    - **CF**: Empresas apenas com Conselho Fiscal
    - **Nenhum**: Empresas sem estruturas formais de governança registradas
    """)



st.subheader("Análise da Presença de Estruturas de Governança por Dependência em 2023", divider="orange")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo compara a adoção de estruturas de governança entre as empresas estatais dependentes e não dependentes do Distrito Federal em 2023. Nota-se que todas as empresas dependentes (100%) possuem tanto Conselho de Administração (CA) quanto Conselho Fiscal (CF), enquanto entre as empresas não dependentes, a presença dessas estruturas é ligeiramente inferior: 78,9% possuem Conselho de Administração, e 94,7% contam com Conselho Fiscal. Esse cenário reflete uma preocupação em assegurar mecanismos mínimos de supervisão e estratégia para empresas que demandam recursos do governo, reforçando a necessidade de monitoramento rigoroso sobre o uso de verbas públicas.

A presença de Comitês de Auditoria (COAUD) é significativamente menor, especialmente entre as empresas dependentes, das quais apenas 14,3% (uma empresa) contam com essa estrutura, em contraste com 47,4% das empresas não dependentes (nove empresas). Essa discrepância pode indicar que as empresas dependentes, apesar de demandarem maior supervisão devido à sua dependência financeira, ainda não adotaram amplamente essa estrutura essencial para o monitoramento de riscos e auditoria independente. Por outro lado, a maior presença de Comitês de Auditoria entre empresas não dependentes pode estar associada à busca por maior eficiência e conformidade regulatória, já que essas organizações operam com maior autonomia financeira.

As vantagens da ampla adoção de Conselhos de Administração e Conselhos Fiscais residem na capacidade de supervisionar estrategicamente a gestão e monitorar as finanças das empresas. Para as estatais dependentes, esses órgãos garantem maior accountability e visibilidade no uso de recursos públicos, sendo essenciais para mitigar riscos de má gestão e desvios. Contudo, a ausência ou baixa adoção do Comitê de Auditoria, especialmente nas empresas dependentes, representa uma desvantagem significativa, pois limita a capacidade de identificar e corrigir problemas relacionados à gestão de riscos e conformidade financeira, elementos críticos para empresas que recebem aportes governamentais.

O panorama de governança apresentado reflete um bom nível de adesão às estruturas fundamentais, como os Conselhos de Administração e Fiscal, mas expõe lacunas no uso de ferramentas mais avançadas, como os Comitês de Auditoria. Para maximizar a eficiência e reduzir riscos, recomenda-se que as empresas dependentes priorizem a implementação de Comitês de Auditoria, reforçando sua capacidade de prestação de contas e assegurando a conformidade com as melhores práticas de governança corporativa. Esse fortalecimento é especialmente importante para empresas que recebem recursos do tesouro distrital, garantindo maior transparência e confiança da sociedade em sua gestão.
""")	

# Filtrar os dados para o Estado DF e ano de 2023
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)]

# Função para contar e calcular porcentagens de empresas em relação à estrutura de governança
def contar_e_calcular_porcentagens(dep_status, total_empresas):
    ca_count = (
        df_filtrado[df_filtrado["dep"].str.upper() == dep_status]["gov_ca"]
        .str.upper()
        .eq("SIM")
        .sum()
    )
    cf_count = (
        df_filtrado[df_filtrado["dep"].str.upper() == dep_status]["gov_cf"]
        .str.upper()
        .eq("SIM")
        .sum()
    )
    aud_count = (
        df_filtrado[df_filtrado["dep"].str.upper() == dep_status]["gov_aud"]
        .str.upper()
        .eq("SIM")
        .sum()
    )
    return (
        (ca_count, ca_count / total_empresas * 100),
        (cf_count, cf_count / total_empresas * 100),
        (aud_count, aud_count / total_empresas * 100),
    )

# Calcular somatórios e porcentagens para empresas dependentes e não dependentes
total_dependentes = df_filtrado[df_filtrado["dep"].str.upper() == "DEPENDENTE"].shape[0]
total_nao_dependentes = df_filtrado[
    df_filtrado["dep"].str.upper() == "NÃO DEPENDENTE"
].shape[0]

dependentes_dados = contar_e_calcular_porcentagens("DEPENDENTE", total_dependentes)
nao_dependentes_dados = contar_e_calcular_porcentagens(
    "NÃO DEPENDENTE", total_nao_dependentes
)

# Estruturar os dados para o Plotly
estruturas = ["Conselho de Administração", "Conselho Fiscal", "Comitê de Auditoria"]

# Criar DataFrame para o gráfico
dados_grafico = pd.DataFrame({
    "Estrutura": estruturas * 2,
    "Status de Dependência": ["Dependente"] * 3 + ["Não Dependente"] * 3,
    "Porcentagem": [d[1] for d in dependentes_dados] + [d[1] for d in nao_dependentes_dados],
    "Quantidade": [d[0] for d in dependentes_dados] + [d[0] for d in nao_dependentes_dados],
    "Total Empresas": [total_dependentes] * 3 + [total_nao_dependentes] * 3
})

# Criar gráfico com Plotly
fig = px.bar(
    dados_grafico,
    x="Estrutura",
    y="Porcentagem",
    color="Status de Dependência",
    barmode="group",
    text="Quantidade",  # Mostrar a quantidade nas barras
    color_discrete_map={
        "Dependente": "#F45046",
        "Não Dependente": "#007acc"
    },
    labels={
        "Porcentagem": "Porcentagem de Empresas (%)",
        "Estrutura": "Estrutura de Governança"
    },
    height=500
)

# Adicionar legenda explicativa - com posição ajustada
fig.add_annotation(
    x=0.5,
    y=1.15,  # Aumentar este valor para mover a legenda para cima
    xref="paper",
    yref="paper",
    text="Legenda: CA = Conselho de Administração, CF = Conselho Fiscal, COAUD = Comitê de Auditoria",
    font=dict(size=11, color="black"),
    showarrow=False,
    align="center"
)

# Personalizar layout
fig.update_layout(
    xaxis_title="Combinação de Estrutura de Governança",
    yaxis_title="Número de Empresas",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(t=80, b=20, l=20, r=20),  # Aumentar margem superior para dar espaço à legenda
    xaxis=dict(
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    ),
    yaxis=dict(
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial",
        font_color="black"
    ),
    height=550  # Aumentar altura do gráfico para acomodar melhor a legenda
)

# Ajustar formato dos rótulos nas barras
fig.update_traces(
    texttemplate="%{text}<br>(%{y:.1f}%)",
    textposition="outside",
    textfont=dict(color="black", size=12),
    hovertemplate="<b>%{x}</b><br>Status: %{data.name}<br>Quantidade: %{text}<br>Porcentagem: %{y:.1f}%<br>Total de empresas: %{customdata}<extra></extra>",
    customdata=dados_grafico["Total Empresas"]
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Opcional: Tabela com os detalhes
with st.expander("Ver dados detalhados"):
    # Preparar dados para a tabela
    tabela_dependencia = pd.DataFrame({
        "Estrutura de Governança": estruturas,
        "Dependentes": [f"{d[0]} ({d[1]:.1f}%)" for d in dependentes_dados],
        "Não Dependentes": [f"{d[0]} ({d[1]:.1f}%)" for d in nao_dependentes_dados],
        "Total": [
            f"{d1[0] + d2[0]} ({(d1[0] + d2[0]) / (total_dependentes + total_nao_dependentes) * 100:.1f}%)"
            for d1, d2 in zip(dependentes_dados, nao_dependentes_dados)
        ]
    })
    
    st.dataframe(
        tabela_dependencia,
        hide_index=True,
        use_container_width=True
    )
    
    # Resumo
    st.info(f"""
    **Resumo das estruturas de governança por dependência:**
    - Total de empresas dependentes: {total_dependentes}
    - Total de empresas não dependentes: {total_nao_dependentes}
    - Total geral: {total_dependentes + total_nao_dependentes}
    """)


st.subheader("Análise da Rentabilidade Média das Empresas pela Combinação de Estruturas de Governança", divider="orange")

# Conteúdo específico desta página
st.write("""

O gráfico abaixo representa a rentabilidade média das empresas estatais distritais, calculada pela relação entre lucro e patrimônio líquido, considerando diferentes combinações de estruturas de governança em 2023. A combinação que inclui Conselho de Administração (CA), Conselho Fiscal (CF) e Comitê de Auditoria (COAUD) apresenta uma rentabilidade média de 17,5%, destacando-se como uma das mais robustas. Essa configuração promove maior supervisão estratégica e controle interno, elementos que contribuem significativamente para o desempenho financeiro positivo dessas empresas. A presença do Comitê de Auditoria nessa configuração é especialmente relevante, pois reforça a capacidade de identificar riscos e promover uma gestão eficiente.

Por outro lado, empresas que possuem apenas o Conselho Fiscal (CF) como estrutura de governança registraram a maior rentabilidade média, de 26,4%. Esse resultado pode refletir um foco direcionado em aspectos financeiros e contábeis, sem os custos e a complexidade de estruturas adicionais. No entanto, a ausência de um Conselho de Administração ou Comitê de Auditoria pode limitar o alinhamento estratégico e o monitoramento detalhado dos riscos de longo prazo. Isso sugere que, embora o desempenho financeiro imediato seja positivo, a sustentabilidade dessas empresas pode ser desafiada sem uma supervisão estratégica abrangente.

As empresas que adotaram apenas Conselho de Administração e Conselho Fiscal (CA, CF) apresentaram uma rentabilidade média de 3,0%, consideravelmente inferior às demais combinações. Essa configuração, embora suficiente para atender às exigências mínimas de governança, pode carecer de um nível mais profundo de análise e controle, especialmente nas áreas de auditoria e gestão de riscos. A ausência do Comitê de Auditoria, que proporciona maior detalhamento nos processos financeiros e operacionais, pode explicar o desempenho reduzido dessas empresas em comparação com as configurações mais completas.

Por fim, as empresas que não possuem qualquer estrutura de governança formal exibiram uma rentabilidade média negativa de -105,8%, refletindo severas dificuldades financeiras e de gestão. Essa ausência de governança formal é um fator crítico que impacta diretamente a sustentabilidade e a eficiência das operações. A falta de supervisão adequada impede o controle de riscos e compromete a capacidade de gerar resultados positivos. Essa situação destaca a importância de estruturas de governança bem implementadas como alicerces para o equilíbrio e o desempenho financeiro. Em síntese, o gráfico demonstra que a adoção de uma governança corporativa mais abrangente, com foco no alinhamento estratégico e no controle interno, é um elemento-chave para assegurar a rentabilidade das estatais distritais e sua contribuição sustentável para o desenvolvimento regional.

Observação: Instituto BRB e BRB Administradora e Corretora de Seguros não aparecem no gráfico pois possuem dados faltantes. Além disso, foram desconsideradas as empresas com patrimônio líquido negativo:

• CEBGAS - Companhia Brasiliense de Gás

• CODEPLAN - Companhia de Planejamento do Distrito Federal

• EMATER - Empresa de Assistência Técnica e Extensão Rural do Distrito Federal

• SAB - Sociedade de Abastecimento de Brasília

""")

 # Filtrar os dados apropriados: deve ser de 2023, estado DF, PL positivo e não nulo e lucros não nulos
df_2023 = df[
    (df["Ano"] == 2023) & (df["Estado"] == "DF") & (df["PL"] > 0) & df["lucros"].notna()
].copy()

# Calcular a rentabilidade individual
df_2023["rentabilidade"] = (df_2023["lucros"] / df_2023["PL"]) * 100

# Função de categorização de combinações de conselhos
def categorizar_combinacoes(row):
    # Verificar e processar gov_ca
    if pd.isna(row["gov_ca"]):
        ca = False
    else:
        ca = str(row["gov_ca"]).strip().upper() == "SIM"
        
    # Verificar e processar gov_cf
    if pd.isna(row["gov_cf"]):
        cf = False
    else:
        cf = str(row["gov_cf"]).strip().upper() == "SIM"
        
    # Verificar e processar gov_aud
    if pd.isna(row["gov_aud"]):
        aud = False
    else:
        aud = str(row["gov_aud"]).strip().upper() == "SIM"

    # Determinar a combinação
    if ca and cf and aud:
        return "CA, CF, COAUD"
    elif ca and cf:
        return "CA, CF"
    elif ca and aud:
        return "CA, COAUD"
    elif cf and aud:
        return "CF, COAUD"
    elif ca:
        return "CA"
    elif cf:
        return "CF"
    elif aud:
        return "COAUD"
    else:
        return "Nenhum"

# Aplicar categorização de forma segura
df_2023["combinação"] = df_2023.apply(categorizar_combinacoes, axis=1)

# Agregar e preparar dados
df_agrupado = (
    df_2023.groupby("combinação")
    .agg(
        media_rentabilidade=("rentabilidade", "mean"),
        empresas=("emp", lambda x: "<br>".join(x)),
        detalhamento_rentabilidade=(
            "rentabilidade",
            lambda x: "<br>".join([f"{y:.1f}%" for y in x])
        ),
        count=("emp", "count")  # Adicionar contagem de empresas
    )
    .reset_index()
)

# Determinar a cor com base na rentabilidade média
df_agrupado["cor"] = df_agrupado["media_rentabilidade"].apply(
    lambda x: "#F46045" if x < 0 else "#007acc"
)

# Relação de combinações
todas_combinacoes = [
    "CA, CF, COAUD",
    "CA, CF",
    "CA, COAUD",
    "CF, COAUD",
    "CA",
    "CF",
    "COAUD",
    "Nenhum",
]

# Garantir que todas as combinações estejam presentes
combinacoes_presentes = df_agrupado["combinação"].unique()
combinacoes_faltantes = [c for c in todas_combinacoes if c not in combinacoes_presentes]

# Adicionar combinações faltantes
for comb in combinacoes_faltantes:
    # Criar um DataFrame com a nova linha
    nova_linha = pd.DataFrame({
        "combinação": [comb],
        "media_rentabilidade": [0],
        "empresas": ["Nenhuma empresa nesta categoria"],
        "detalhamento_rentabilidade": ["N/A"],
        "count": [0],
        "cor": ["#007acc"]  # cor padrão para barras sem dados
    })
    
    # Concatenar com o DataFrame existente
    df_agrupado = pd.concat([df_agrupado, nova_linha], ignore_index=True)
# Ordenar pelas combinações predefinidas
df_agrupado["ordem"] = df_agrupado["combinação"].apply(lambda x: todas_combinacoes.index(x) if x in todas_combinacoes else 999)
df_agrupado = df_agrupado.sort_values("ordem").drop("ordem", axis=1)

# Criação de gráfico interativo com Plotly
fig = px.bar(
    df_agrupado,
    x="combinação",
    y="media_rentabilidade",
    text="media_rentabilidade",
    color="combinação",
    color_discrete_map={row["combinação"]: row["cor"] for _, row in df_agrupado.iterrows()},
    labels={
        "media_rentabilidade": "Rentabilidade Média (%)",
        "combinação": "Combinação de Estruturas de Governança",
    },
    custom_data=["empresas", "detalhamento_rentabilidade", "count"],
    height=550
)

# Atualizar template de hover
fig.update_traces(
    hovertemplate=(
        "<b>Combinação:</b> %{x}<br>"
        "<b>Rentabilidade Média:</b> %{y:.1f}%<br>"
        "<b>Número de Empresas:</b> %{customdata[2]}<br>"
        "<b>Empresas:</b> <br>%{customdata[0]}<br>"
        "<b>Rentabilidades Individuais:</b> <br>%{customdata[1]}<extra></extra>"
    ),
    texttemplate="%{y:.1f}%",  # Ajustar label de cada barra para porcentagem
    textposition="outside",
    textfont=dict(color="black", size=12)
)

# Adicionar legenda explicativa
fig.add_annotation(
    x=0.5,
    y=1.10,
    xref="paper",
    yref="paper",
    text="Legenda: CA = Conselho de Administração, CF = Conselho Fiscal, COAUD = Comitê de Auditoria",
    font=dict(size=11, color="black"),
    showarrow=False,
    align="center"
)

# Ajustar layout final
fig.update_layout(
    xaxis_title="Combinação de Estrutura de Governança",
    yaxis_title="Rentabilidade Média (%)",
    showlegend=False,
    plot_bgcolor="white", 
    paper_bgcolor="white",
    margin=dict(t=70, b=20, l=20, r=20),
    xaxis=dict(
        tickfont=dict(color="black"),
        title_font=dict(color="black")
    ),
    yaxis=dict(
        tickfont=dict(color="black"),
        title_font=dict(color="black"),
        zeroline=True,
        zerolinecolor="black",
        zerolinewidth=0.5
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_family="Arial",
        font_color="black"
    )
)

# Exibir gráfico no Streamlit
st.plotly_chart(fig, use_container_width=True)

# Tabela com dados detalhados
with st.expander("Ver detalhes de rentabilidade por estrutura de governança"):
    # Criar versão formatada para exibição
    tabela_detalhe = df_agrupado.copy()
    tabela_detalhe["empresas"] = tabela_detalhe["empresas"].str.replace("<br>", ", ")
    tabela_detalhe["detalhamento_rentabilidade"] = tabela_detalhe["detalhamento_rentabilidade"].str.replace("<br>", ", ")
    tabela_detalhe.rename(columns={
        "combinação": "Combinação",
        "media_rentabilidade": "Rentabilidade Média (%)",
        "empresas": "Empresas",
        "detalhamento_rentabilidade": "Rentabilidades Individuais",
        "count": "Número de Empresas"
    }, inplace=True)
    
    # Exibir tabela formatada
    st.dataframe(
        tabela_detalhe[["Combinação", "Número de Empresas", "Rentabilidade Média (%)", "Empresas", "Rentabilidades Individuais"]],
        column_config={
            "Rentabilidade Média (%)": st.column_config.NumberColumn(
                "Rentabilidade Média (%)",
                format="%.1f%%"
            )
        },
        hide_index=True,
        use_container_width=True
    )
    
# Botão para voltar à página inicial
if st.button("Voltar à Página Inicial"):
    st.switch_page("Início.py")
