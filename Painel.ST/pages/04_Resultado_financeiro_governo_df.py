# Importando as bibliotecas
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import base64
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"C:\Users\Eric\OneDrive\Estudos\RBCIP\Estatais\Dashboard\Arquivos VS Code\BD_Completo_Nacional_Formatado.csv"
df = pd.read_csv(file_path)

# Configurações da página
st.set_page_config(
    page_title="Qual o resultado financeiro das estatais para o Governo do DF?",
    page_icon="📈",
    layout="wide"
)

st.header("Qual o resultado financeiro das estatais para o Governo do DF?", divider="green")

# Conteúdo específico desta página
st.write("""

Nesta seção, de forma geral, pretende-se apurar, em relação aos últimos anos, quanto o Distrito Federal transferiu às empresas como reforço de capital ou como subvenções e quanto recebeu de dividendos das empresas, ou seja, verificar se houve repasses ou recebimento líquido de forma a entender o impacto fiscal das estatais nas finanças do Distrito Federal.

""")	

st.subheader("Resultado Líquido das Empresas para o Estado em 2023", divider="green")

st.write("""

O gráfico apresentado abaixo evidencia os resultados líquidos das estatais distritais em 2023, destacando a contribuição financeira de cada empresa para o Governo do DF. No topo do ranking, o BRB - Banco Regional de Brasília, junto de suas subsidiárias, aparece como o principal gerador de lucros, com um resultado líquido superior a R$ 322 milhões, consolidando-se como um ativo estratégico para o equilíbrio fiscal. O desempenho do BRB reflete uma gestão eficiente, diversificação de receitas e operações sólidas no mercado financeiro, posicionando-o como uma fonte confiável de retorno ao estado.

Em contraste, setores como habitação e urbanização e transporte público apresentaram os maiores prejuízos. A NOVACAP, por exemplo, registrou um déficit significativo de mais de R$ 341 milhões. 

Outro destaque negativo é a EMATER, que também apresentou prejuízo expressivo, refletindo dificuldades no financiamento de suas operações e no cumprimento de seu papel estratégico no setor agropecuário. Da mesma forma, empresas como a CODHAB e a SAB operaram com resultados líquidos negativos, reforçando a necessidade de maior eficiência na gestão de recursos e de estratégias voltadas à sustentabilidade financeira.

""")	

# Filtrar os dados apropriados de 'DF' em 2023
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"] == 2023)].copy()

# Verificar se há dados disponíveis
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para o DF no ano de 2023.")
else:
    # Ordenar os resultados do maior para o menor
    df_filtrado.sort_values(
        by="Resultado para o Estado Acionista", ascending=True, inplace=True
    )
    
    # Adicionar informação de dependência para análise
    if "dep" in df_filtrado.columns:
        df_filtrado["Dependência"] = df_filtrado["dep"].apply(
            lambda x: "Dependente" if str(x).upper() == "DEPENDENTE" else "Não Dependente"
        )
    
    # Calcular estatísticas para contextualização
    total_resultado = df_filtrado["Resultado para o Estado Acionista"].sum()
    empresas_positivas = df_filtrado[df_filtrado["Resultado para o Estado Acionista"] > 0]
    empresas_negativas = df_filtrado[df_filtrado["Resultado para o Estado Acionista"] < 0]
    
    # Métricas de contexto
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Resultado Líquido Total", 
            f"R$ {total_resultado:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Empresas com Resultado Positivo", 
            f"{len(empresas_positivas)}",
            f"{len(empresas_positivas)/len(df_filtrado)*100:.1f}%"
        )
    
    with col3:
        st.metric(
            "Empresas com Resultado Negativo", 
            f"{len(empresas_negativas)}",
            f"{len(empresas_negativas)/len(df_filtrado)*100:.1f}%",
            delta_color="inverse"
        )
    
    # Criando o gráfico de barras com Plotly Express
    fig = px.bar(
        df_filtrado,
        x="Resultado para o Estado Acionista",
        y="emp",
        orientation="h",
        text="Resultado para o Estado Acionista",
        color="Resultado para o Estado Acionista",
        color_continuous_scale=["#F46045", "#F46045", "#007acc", "#007acc"],
        color_continuous_midpoint=0,
        labels={
            "Resultado para o Estado Acionista": "Valor (R$)", 
            "emp": "Empresa"
        },
        hover_data={
            "Resultado para o Estado Acionista": ":,.2f",
            "setor": True,
            "Dependência": True
        } if "dep" in df_filtrado.columns and "setor" in df_filtrado.columns else None
    )
    
    # Atualizar template de hover e texto
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Resultado: R$ %{x:,.2f}<br>"
            "Setor: %{customdata[0]}<br>"
            "Dependência: %{customdata[1]}<extra></extra>"
        ) if "dep" in df_filtrado.columns and "setor" in df_filtrado.columns else
        "<b>%{y}</b><br>Resultado: R$ %{x:,.2f}<extra></extra>",
        texttemplate="R$ %{x:,.2f}",
        textposition="outside",
        textfont=dict(color="black", size=10),
        cliponaxis=False
    )
    
    # Linha de referência no zero
    fig.add_vline(
        x=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Linha Zero", 
        annotation_position="top"
    )
    
    # Ajustar o layout
    fig.update_layout(
        height=800,  # Altura adaptativa com base no número de empresas
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "text": "<b>Resultado Líquido das Estatais para o Governo do DF em 2023</b>",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": "black"}
        },
        xaxis=dict(
            title=dict(text="Resultado para o Estado Acionista (R$)", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="lightgray",
            zerolinecolor="black",
            zerolinewidth=1.5,
            # Ajustar o limite automático ou definir um intervalo específico se necessário
            # range=[-1.5e9, 1e9]
        ),
        yaxis=dict(
            title=dict(text="Empresa", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="white"
        ),
        coloraxis_showscale=False,  # Ocultar a escala de cores
        margin=dict(l=50, r=120, t=80, b=50)  # Aumentar margem direita para texto
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Adicionar seção expansível com detalhes
    with st.expander("📊 Ver detalhes do resultado financeiro"):
        # Tabela com todos os dados relevantes
        tabela = df_filtrado[["emp", "Resultado para o Estado Acionista", "setor"]] if "setor" in df_filtrado.columns else df_filtrado[["emp", "Resultado para o Estado Acionista"]]
        
        if "dep" in df_filtrado.columns:
            tabela["Dependência"] = df_filtrado["Dependência"]
        
        # Renomear colunas para melhor visualização
        tabela.columns = ["Empresa", "Resultado para o Estado (R$)"] + (["Setor"] if "setor" in df_filtrado.columns else []) + (["Dependência"] if "dep" in df_filtrado.columns else [])
        
        # Ordenar por resultado (maior para menor)
        tabela = tabela.sort_values(by="Resultado para o Estado (R$)", ascending=False)
        
        # Exibir tabela formatada
        st.dataframe(
            tabela,
            column_config={
                "Resultado para o Estado (R$)": st.column_config.NumberColumn(
                    "Resultado para o Estado (R$)",
                    format="R$ %.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Análise adicional
        col1, col2 = st.columns(2)
        
        with col1:
            if len(empresas_positivas) > 0:
                try:
                    # Encontrar empresa com maior resultado positivo
                    melhor_valor = empresas_positivas["Resultado para o Estado Acionista"].max()
                    melhor_empresa = empresas_positivas[empresas_positivas["Resultado para o Estado Acionista"] == melhor_valor].iloc[0]
                    
                    st.success(f"**Empresa com melhor resultado**: {melhor_empresa['emp']}")
                    st.write(f"Valor: **R$ {melhor_empresa['Resultado para o Estado Acionista']:,.2f}**")
                    
                    if "setor" in melhor_empresa and pd.notna(melhor_empresa["setor"]):
                        st.write(f"Setor: {melhor_empresa['setor']}")
                except (IndexError, KeyError) as e:
                    st.info("Não foi possível determinar a empresa com melhor resultado.")
                    st.write(f"Erro: {str(e)}")
            else:
                st.info("Não há empresas com resultado positivo no período.")
        
        with col2:
            if len(empresas_negativas) > 0:
                try:
                    # Encontrar empresa com pior resultado negativo
                    pior_valor = empresas_negativas["Resultado para o Estado Acionista"].min()
                    pior_empresa = empresas_negativas[empresas_negativas["Resultado para o Estado Acionista"] == pior_valor].iloc[0]
                    
                    st.error(f"**Empresa com pior resultado**: {pior_empresa['emp']}")
                    st.write(f"Valor: **R$ {pior_empresa['Resultado para o Estado Acionista']:,.2f}**")
                    
                    if "setor" in pior_empresa and pd.notna(pior_empresa["setor"]):
                        st.write(f"Setor: {pior_empresa['setor']}")
                except (IndexError, KeyError) as e:
                    st.info("Não foi possível determinar a empresa com pior resultado.")
                    st.write(f"Erro: {str(e)}")
            else:
                st.info("Não há empresas com resultado negativo no período.")


st.subheader("Resultado Líquido das Empresas para o Estado - acumulado 2020 a 2023", divider="green")

st.write("""

A análise do resultado líquido acumulado das empresas estatais do Distrito Federal entre 2020 e 2023, gráfico abaixo, revela um panorama marcante de contrastes financeiros. Enquanto algumas empresas contribuíram significativamente para as receitas do estado, outras registraram déficits expressivos, destacando desafios estruturais e operacionais que precisam ser enfrentados.

No grupo das empresas lucrativas, o BRB - Banco Regional de Brasília ocupa o topo do ranking, com um lucro acumulado de mais de 458,7 milhões e R$ 253,3 milhões de reais, respectivamente. Esses números refletem a eficiência dessas empresas em seus setores de atuação, caracterizados por forte geração de receitas, boa governança e estratégias sólidas de expansão e diversificação de negócios. A contribuição dessas empresas não apenas fortalece as finanças públicas do Distrito Federal, mas também evidencia o impacto positivo de uma gestão orientada para resultados.

Por outro lado, os resultados negativos são liderados pela NOVACAP - Companhia Urbanizadora da Nova Capital do Brasil, que acumulou um prejuízo impressionante de mais de 1,1 bilhão e 1,03 bilhão de reais, respectivamente. Esses números destacam a vulnerabilidade de setores que dependem fortemente de subsídios governamentais ou enfrentam dificuldades na geração de receitas próprias. Os prejuízos recorrentes dessas empresas reforçam a necessidade de intervenções estruturais, como reavaliação de modelos operacionais, parcerias público-privadas e adoção de tecnologias para melhorar a eficiência.

Empresas como a EMATER, a CODHAB, e o TCB - Sociedade de Transportes Coletivos de Brasília também apresentaram resultados negativos significativos, evidenciando dificuldades em equilibrar suas operações financeiras com as exigências de suas missões sociais. Esses setores, frequentemente associados a serviços essenciais, enfrentam desafios para alinhar a sustentabilidade financeira com a prestação de serviços de qualidade para a população.

""")	

# Filtrar os dados entre 2020 e 2023 para o estado DF
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"].between(2020, 2023))].copy()

# Verificar se há dados disponíveis
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para o DF entre 2020 e 2023.")
else:
    # Agrupar por empresa e somar os resultados entre os anos desejados
    df_agrupado = df_filtrado.groupby("emp", as_index=False).agg({
        "Resultado para o Estado Acionista": "sum",
        "setor": "first"  # Preservar o setor para análise
    }) if "setor" in df_filtrado.columns else df_filtrado.groupby("emp", as_index=False).agg({
        "Resultado para o Estado Acionista": "sum"
    })
    
    # Ordenar os resultados em ordem crescente para visualização
    df_agrupado.sort_values(
        by="Resultado para o Estado Acionista", ascending=True, inplace=True
    )
    
    # Calcular estatísticas para contextualização
    total_resultado = df_agrupado["Resultado para o Estado Acionista"].sum()
    empresas_positivas = df_agrupado[df_agrupado["Resultado para o Estado Acionista"] > 0]
    empresas_negativas = df_agrupado[df_agrupado["Resultado para o Estado Acionista"] < 0]
    
    # Métricas de resumo
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Resultado Líquido Acumulado", 
            f"R$ {total_resultado:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Empresas com Saldo Positivo", 
            f"{len(empresas_positivas)}",
            f"{len(empresas_positivas)/len(df_agrupado)*100:.1f}%"
        )
    
    with col3:
        st.metric(
            "Empresas com Saldo Negativo", 
            f"{len(empresas_negativas)}",
            f"{len(empresas_negativas)/len(df_agrupado)*100:.1f}%",
            delta_color="inverse"
        )
    
    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(
        df_agrupado,
        x="Resultado para o Estado Acionista",
        y="emp",
        orientation="h",
        text="Resultado para o Estado Acionista",
        color="Resultado para o Estado Acionista",
        color_continuous_scale=["#F46045", "#F46045", "#007acc", "#007acc"],
        color_continuous_midpoint=0,
        labels={
            "Resultado para o Estado Acionista": "Valor Acumulado (R$)", 
            "emp": "Empresa"
        },
        hover_data={
            "Resultado para o Estado Acionista": ":,.2f",
            "setor": True
        } if "setor" in df_agrupado.columns else None
    )
    
    # Configurar formatação do texto e hover
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Resultado Acumulado: R$ %{x:,.2f}<br>"
            "Setor: %{customdata[0]}<extra></extra>"
        ) if "setor" in df_agrupado.columns else
        "<b>%{y}</b><br>Resultado Acumulado: R$ %{x:,.2f}<extra></extra>",
        texttemplate="R$ %{x:,.2f}",
        textposition="outside",
        textfont=dict(color="black", size=10),
        cliponaxis=False
    )
    
    # Linha de referência no zero
    fig.add_vline(
        x=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Linha Zero", 
        annotation_position="top"
    )
    
    # Ajustar o layout
    fig.update_layout(
        height=800,
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "text": "<b>Resultado Líquido Acumulado das Estatais para o Governo do DF (2020-2023)</b>",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": "black"}
        },
        xaxis=dict(
            title=dict(text="Resultado para o Estado Acionista (R$)", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="lightgray",
            zerolinecolor="black",
            zerolinewidth=1.5,
            # Ajustar o limite para que todos os dados sejam visíveis
            # range=[-5e9, 1.5e9]
        ),
        yaxis=dict(
            title=dict(text="Empresa", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="white"
        ),
        coloraxis_showscale=False,  # Ocultar a escala de cores
        margin=dict(l=50, r=150, t=80, b=50)  # Aumentar margem direita para acomodar valores
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Adicionar seção expandível com detalhes
    with st.expander("📊 Ver detalhes do resultado financeiro acumulado"):
        # Tabela com todos os dados relevantes
        tabela = df_agrupado[["emp", "Resultado para o Estado Acionista", "setor"]] if "setor" in df_agrupado.columns else df_agrupado[["emp", "Resultado para o Estado Acionista"]]
        
        # Renomear colunas para melhor visualização
        nomes_colunas = ["Empresa", "Resultado Acumulado para o Estado (R$)"]
        if "setor" in tabela.columns:
            nomes_colunas.append("Setor")
        tabela.columns = nomes_colunas
        
        # Ordenar por resultado (maior para menor)
        tabela = tabela.sort_values(by="Resultado Acumulado para o Estado (R$)", ascending=False)
        
        # Exibir tabela formatada
        st.dataframe(
            tabela,
            column_config={
                "Resultado Acumulado para o Estado (R$)": st.column_config.NumberColumn(
                    "Resultado Acumulado para o Estado (R$)",
                    format="R$ %.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Análise adicional - Top empresas positivas e negativas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Empresas com maior saldo positivo")
            if len(empresas_positivas) > 0:
                top_positivas = empresas_positivas.nlargest(5, "Resultado para o Estado Acionista")
                for i, row in enumerate(top_positivas.itertuples(), 1):
                    st.success(f"{i}. **{row.emp}**")
                    st.write(f"Resultado: R$ {row._2:,.2f}")
                    if hasattr(row, "setor") and pd.notna(row.setor):
                        st.write(f"Setor: {row.setor}")
                    st.write("---")
            else:
                st.info("Não há empresas com saldo positivo no período.")
        
        with col2:
            st.markdown("### Empresas com maior saldo negativo")
            if len(empresas_negativas) > 0:
                top_negativas = empresas_negativas.nsmallest(5, "Resultado para o Estado Acionista")
                for i, row in enumerate(top_negativas.itertuples(), 1):
                    st.error(f"{i}. **{row.emp}**")
                    st.write(f"Resultado: R$ {row._2:,.2f}")
                    if hasattr(row, "setor") and pd.notna(row.setor):
                        st.write(f"Setor: {row.setor}")
                    st.write("---")
            else:
                st.info("Não há empresas com saldo negativo no período.")


st.subheader("Resultado Líquido para o Estado, por Setor - acumulado 2020 a 2023", divider="green")

st.write("""

O gráfico abaixo apresenta o resultado líquido acumulado das empresas estatais do Distrito Federal por setor de atuação entre 2020 e 2023, destacando disparidades marcantes no desempenho financeiro de diferentes segmentos. Os setores de financeiro e energia foram os únicos a apresentar resultados líquidos positivos, enquanto outros setores, especialmente habitação e urbanização, acumularam prejuízos significativos, evidenciando desafios estruturais e operacionais.

O setor financeiro, liderado pelo BRB e suas subsidiárias, alcançou um resultado líquido acumulado de mais de R$ 253 milhões, também demonstrou solidez, impulsionado pela CEB e suas subsidiárias, que se beneficiaram de estratégias de modernização e otimização de operações de geração e distribuição de energia.

Em contrapartida, o setor de habitação e urbanização registrou o maior déficit acumulado, com prejuízo superior a R$ 1,3 bilhão, destacando a dificuldade em equilibrar custos operacionais elevados e receitas insuficientes para cobrir despesas. Esses números reforçam a necessidade de reavaliações estratégicas nesses setores, com foco em reestruturação e maior eficiência na utilização dos recursos públicos.

Setores como gestão de ativos e pesquisa e assistência técnica agropecuária também apresentaram resultados negativos, com déficits de R$ 378 milhões, respectivamente. 

Esses setores enfrentam desafios para equilibrar sua relevância social com a sustentabilidade financeira. O setor de saneamento, em contraste, registrou um leve superávit de R$ 11 milhões, destacando a CAESB como uma empresa capaz de manter resultados positivos, mesmo em um ambiente operacional complexo.

""")	

# Filtrar os dados entre 2020 e 2023 para o estado DF
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"].between(2020, 2023))].copy()

# Verificar se há dados disponíveis
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para o DF entre 2020 e 2023.")
else:
    # Agrupar por setor e somar os resultados entre os anos desejados
    df_agrupado_por_setor = df_filtrado.groupby("setor", as_index=False).agg(
        {
            "Resultado para o Estado Acionista": "sum",
            "emp": lambda x: list(sorted(set(x))),  # Lista de empresas únicas por setor
        }
    )
    
    # Adicionar coluna com número de empresas e lista formatada para exibição
    df_agrupado_por_setor["num_empresas"] = df_agrupado_por_setor["emp"].apply(len)
    df_agrupado_por_setor["empresas_lista"] = df_agrupado_por_setor["emp"].apply(lambda x: ", ".join(x))
    
    # Ordenar os resultados do maior para o menor
    df_agrupado_por_setor.sort_values(
        by="Resultado para o Estado Acionista", ascending=True, inplace=True
    )
    
    # Calcular estatísticas para contextualização
    total_resultado = df_agrupado_por_setor["Resultado para o Estado Acionista"].sum()
    setores_positivos = df_agrupado_por_setor[df_agrupado_por_setor["Resultado para o Estado Acionista"] > 0]
    setores_negativos = df_agrupado_por_setor[df_agrupado_por_setor["Resultado para o Estado Acionista"] < 0]
    
    # Métricas de resumo
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Resultado Total por Setor", 
            f"R$ {total_resultado:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Setores com Saldo Positivo", 
            f"{len(setores_positivos)}",
            f"{len(setores_positivos)/len(df_agrupado_por_setor)*100:.1f}% dos setores"
        )
    
    with col3:
        st.metric(
            "Setores com Saldo Negativo", 
            f"{len(setores_negativos)}",
            f"{len(setores_negativos)/len(df_agrupado_por_setor)*100:.1f}% dos setores",
            delta_color="inverse"
        )
    
    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(
        df_agrupado_por_setor,
        x="Resultado para o Estado Acionista",
        y="setor",
        orientation="h",
        text="Resultado para o Estado Acionista",
        color="Resultado para o Estado Acionista",
        color_continuous_scale=["#F46045", "#F46045", "#007acc", "#007acc"],
        color_continuous_midpoint=0,
        labels={
            "Resultado para o Estado Acionista": "Valor Acumulado (R$)", 
            "setor": "Setor",
            "empresas_lista": "Empresas",
            "num_empresas": "Número de Empresas"
        },
        hover_data={
            "Resultado para o Estado Acionista": ":,.2f",
            "empresas_lista": True,
            "num_empresas": True
        }
    )
    
    # Configurar formatação do texto e hover
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Resultado Acumulado: R$ %{x:,.2f}<br>"
            "Empresas (%{customdata[1]}): %{customdata[0]}<extra></extra>"
        ),
        texttemplate="R$ %{x:,.2f}",
        textposition="outside",
        textfont=dict(color="black", size=12),
        cliponaxis=False
    )
    
    # Linha de referência no zero
    fig.add_vline(
        x=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Linha Zero", 
        annotation_position="top"
    )
    
    # Ajustar o layout
    fig.update_layout(
        height=600,
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "text": "<b>Resultado Líquido para o Estado por Setor (2020-2023)</b>",
            "y": 0.98,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": "black"}
        },
        xaxis=dict(
            title=dict(text="Resultado para o Estado Acionista (R$)", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="lightgray",
            zerolinecolor="black",
            zerolinewidth=1.5,
            # Ajustar o limite para que todos os dados sejam visíveis
            range=[-4.5e9, 2e9]
        ),
        yaxis=dict(
            title=dict(text="Setor", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="white"
        ),
        coloraxis_showscale=False,  # Ocultar a escala de cores
        margin=dict(l=50, r=150, t=80, b=50)  # Aumentar margem direita para acomodar valores
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Adicionar seção expandível com detalhes por setor
    with st.expander("📊 Ver detalhes dos resultados por setor"):
        # Preparar tabela detalhada
        tabela = df_agrupado_por_setor[["setor", "Resultado para o Estado Acionista", "empresas_lista", "num_empresas"]].copy()
        tabela.columns = ["Setor", "Resultado Acumulado (R$)", "Empresas", "Número de Empresas"]
        
        # Ordenar por resultado (maior para menor)
        tabela = tabela.sort_values(by="Resultado Acumulado (R$)", ascending=False)
        
        # Exibir tabela formatada
        st.dataframe(
            tabela,
            column_config={
                "Resultado Acumulado (R$)": st.column_config.NumberColumn(
                    "Resultado Acumulado (R$)",
                    format="R$ %.2f"
                ),
                "Empresas": st.column_config.TextColumn(
                    "Empresas",
                    width="large"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Análise adicional dos setores
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Setor com melhor resultado")
            if len(setores_positivos) > 0:
                # Encontrar o setor com melhor resultado
                melhor_setor = setores_positivos.iloc[setores_positivos["Resultado para o Estado Acionista"].idxmax()]
                st.success(f"**{melhor_setor['setor']}**")
                st.write(f"Resultado: **R$ {melhor_setor['Resultado para o Estado Acionista']:,.2f}**")
                st.write(f"Empresas ({melhor_setor['num_empresas']}): {melhor_setor['empresas_lista']}")
            else:
                st.info("Não há setores com saldo positivo no período.")
        
        with col2:
            st.markdown("### Setor com pior resultado")
            if len(setores_negativos) > 0:
                # Encontrar o setor com pior resultado
                pior_setor = setores_negativos.iloc[setores_negativos["Resultado para o Estado Acionista"].idxmin()]
                st.error(f"**{pior_setor['setor']}**")
                st.write(f"Resultado: **R$ {pior_setor['Resultado para o Estado Acionista']:,.2f}**")
                st.write(f"Empresas ({pior_setor['num_empresas']}): {pior_setor['empresas_lista']}")
            else:
                st.info("Não há setores com saldo negativo no período.")


st.subheader("Resultado Líquido para o Estado Acionista, por Dependência - 2020 a 2023 acumulado", divider="green")

st.write("""

O gráfico a seguir ilustra o resultado líquido acumulado das empresas estatais do Distrito Federal entre 2020 e 2023, categorizando-as em dependentes e não dependentes, conforme a classificação estabelecida pela Lei de Responsabilidade Fiscal (LRF). O contraste entre os dois grupos é significativo: as empresas dependentes acumularam um prejuízo total de R$  306,7 milhões. Esses dados refletem disparidades na capacidade de geração de receitas e eficiência operacional entre os dois grupos.

As empresas dependentes, por definição, necessitam de aportes financeiros do governo para custear despesas operacionais, salariais e de capital, o que compromete sua autonomia financeira e aumenta sua vulnerabilidade a variações no orçamento público. Setores como habitação, transporte e assistência técnica agropecuária, amplamente representados entre as empresas dependentes, enfrentam desafios estruturais como custos elevados e receitas insuficientes para cobrir as despesas, o que contribui para o déficit expressivo registrado. Essa dependência reflete não apenas limitações operacionais, mas também a dificuldade em equilibrar a prestação de serviços essenciais com a sustentabilidade financeira.

Em contraste, as empresas não dependentes demonstraram maior capacidade de geração de resultados positivos. O lucro acumulado de R$ 306,7 milhões foi impulsionado, principalmente, pelos setores financeiro e energético, liderados por empresas como o BRB e a CEB, que possuem modelos de negócios diversificados e operações mais orientadas ao mercado. Essas organizações se destacam por sua eficiência em utilizar seus recursos patrimoniais para gerar retorno financeiro ao estado, sem demandar aportes governamentais regulares. Esse contraste evidencia o impacto da autonomia financeira e da governança corporativa na performance das estatais, reforçando a necessidade de estratégias diferenciadas para cada grupo.

A análise do período acumulado de 2020 a 2023 expõe a importância de priorizar políticas públicas que promovam eficiência operacional e sustentabilidade financeira, principalmente para empresas dependentes. Ao mesmo tempo, os resultados das empresas não dependentes confirmam o valor estratégico de investir em setores capazes de gerar retornos consistentes ao estado, garantindo maior equilíbrio fiscal e alívio à necessidade de subsídios governamentais.

""")	

# Filtrar os dados entre 2020 e 2023 para o estado DF
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"].between(2020, 2023))].copy()

# Verificar se há dados disponíveis e a coluna de dependência existe
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para o DF entre 2020 e 2023.")
elif "dep" not in df_filtrado.columns:
    st.warning("A coluna de dependência não está disponível nos dados.")
else:
    # Garantir que não há valores ausentes na coluna de dependência
    df_filtrado = df_filtrado.dropna(subset=["dep"])
    
    # Padronizar os valores da coluna de dependência
    df_filtrado["dep"] = df_filtrado["dep"].apply(
        lambda x: "Dependente" if str(x).upper() == "DEPENDENTE" else "Não Dependente"
    )
    
    # Agrupar por dependência e somar os resultados entre os anos desejados
    df_agrupado_por_dep = df_filtrado.groupby("dep", as_index=False).agg({
        "Resultado para o Estado Acionista": "sum",
        "emp": lambda x: list(sorted(set(x))),
        "setor": lambda x: list(sorted(set(x))) if "setor" in df_filtrado.columns else None
    })
    
    # Adicionar colunas para facilitar a exibição
    df_agrupado_por_dep["num_empresas"] = df_agrupado_por_dep["emp"].apply(len)
    df_agrupado_por_dep["empresas_lista"] = df_agrupado_por_dep["emp"].apply(lambda x: ", ".join(x))
    
    if "setor" in df_agrupado_por_dep.columns:
        df_agrupado_por_dep["setores_lista"] = df_agrupado_por_dep["setor"].apply(
            lambda x: ", ".join(x) if x is not None else "N/A"
        )
    
    # Calcular estatísticas para contextualização
    total_resultado = df_agrupado_por_dep["Resultado para o Estado Acionista"].sum()
    estatais_dependentes = df_agrupado_por_dep[df_agrupado_por_dep["dep"] == "Dependente"]
    estatais_nao_dependentes = df_agrupado_por_dep[df_agrupado_por_dep["dep"] == "Não Dependente"]
    
    # Exibir métricas resumidas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Resultado Total", 
            f"R$ {total_resultado:,.2f}",
            delta=None
        )
    
    with col2:
        if not estatais_dependentes.empty:
            resultado_dependentes = estatais_dependentes["Resultado para o Estado Acionista"].iloc[0]
            st.metric(
                "Estatais Dependentes", 
                f"R$ {resultado_dependentes:,.2f}",
                delta=f"{resultado_dependentes/total_resultado*100:.1f}%" if total_resultado != 0 else None,
                delta_color="off" if resultado_dependentes < 0 else "normal"
            )
        else:
            st.metric("Estatais Dependentes", "Dados não disponíveis")
    
    with col3:
        if not estatais_nao_dependentes.empty:
            resultado_nao_dependentes = estatais_nao_dependentes["Resultado para o Estado Acionista"].iloc[0]
            st.metric(
                "Estatais Não Dependentes", 
                f"R$ {resultado_nao_dependentes:,.2f}",
                delta=f"{resultado_nao_dependentes/total_resultado*100:.1f}%" if total_resultado != 0 else None,
                delta_color="off" if resultado_nao_dependentes < 0 else "normal"
            )
        else:
            st.metric("Estatais Não Dependentes", "Dados não disponíveis")
    
    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(
        df_agrupado_por_dep,
        x="dep",
        y="Resultado para o Estado Acionista",
        orientation="v",
        text="Resultado para o Estado Acionista",
        color="Resultado para o Estado Acionista",
        color_continuous_scale=["#F46045", "#F46045", "#007acc", "#007acc"],
        color_continuous_midpoint=0,
        labels={
            "Resultado para o Estado Acionista": "Valor Acumulado (R$)", 
            "dep": "Dependência"
        },
        hover_data={
            "Resultado para o Estado Acionista": ":,.2f",
            "num_empresas": True,
            "empresas_lista": True,
            "setores_lista": True if "setores_lista" in df_agrupado_por_dep.columns else False
        }
    )
    
    # Configurar formatação do texto e hover
    if "setores_lista" in df_agrupado_por_dep.columns:
        hover_template = (
            "<b>%{x}</b><br>"
            "Resultado Acumulado: R$ %{y:,.2f}<br>"
            "Número de Empresas: %{customdata[0]}<br>"
            "Empresas: %{customdata[1]}<br>"
            "Setores: %{customdata[2]}<extra></extra>"
        )
    else:
        hover_template = (
            "<b>%{x}</b><br>"
            "Resultado Acumulado: R$ %{y:,.2f}<br>"
            "Número de Empresas: %{customdata[0]}<br>"
            "Empresas: %{customdata[1]}<extra></extra>"
        )
    
    fig.update_traces(
        hovertemplate=hover_template,
        texttemplate="R$ %{y:,.2f}",
        textposition="outside",
        textfont=dict(color="black", size=14),
        marker_line_width=1,
        marker_line_color="gray",
        cliponaxis=False
    )
    
    # Linha de referência no zero
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Linha Zero", 
        annotation_position="right"
    )
    
    # Ajustar o layout
    fig.update_layout(
        height=600,
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "text": "<b>Resultado Líquido para o Estado por Dependência (2020-2023)</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": "black"}
        },
        xaxis=dict(
            title=dict(text="Dependência", font=dict(size=16, color="black")),
            tickfont=dict(size=14, color="black"),
            gridcolor="white"
        ),
        yaxis=dict(
            title=dict(text="Resultado para o Estado Acionista (R$)", font=dict(size=16, color="black")),
            tickfont=dict(size=14, color="black"),
            gridcolor="lightgray",
            zerolinecolor="black",
            zerolinewidth=1.5,
            # Ajustar a escala para melhor visualização
            # range=[-7e9, 1e9]
        ),
        coloraxis_showscale=False,  # Ocultar a escala de cores
        bargap=0.4,  # Aumentar o espaço entre barras
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Adicionar comparação visual entre grupos
    for i, row in df_agrupado_por_dep.iterrows():
        fig.add_annotation(
            x=row["dep"],
            y=row["Resultado para o Estado Acionista"],
            text=f"{row['num_empresas']} empresas",
            showarrow=False,
            font=dict(size=12, color="black"),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="gray",
            borderwidth=1,
            borderpad=4,
            yshift=30 if row["Resultado para o Estado Acionista"] < 0 else -30
        )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Adicionar seção expandível com detalhes
    with st.expander("📊 Ver detalhes por dependência"):
        # Preparar dados para exibição
        for dep_type in df_agrupado_por_dep["dep"].unique():
            st.markdown(f"### {dep_type}")
            
            # Obter dados do grupo
            grupo = df_agrupado_por_dep[df_agrupado_por_dep["dep"] == dep_type].iloc[0]
            
            # Exibir resultado
            if grupo["Resultado para o Estado Acionista"] >= 0:
                st.success(f"**Resultado Acumulado**: R$ {grupo['Resultado para o Estado Acionista']:,.2f}")
            else:
                st.error(f"**Resultado Acumulado**: R$ {grupo['Resultado para o Estado Acionista']:,.2f}")
            
            # Exibir detalhes
            st.write(f"**Número de Empresas**: {grupo['num_empresas']}")
            
            # Criar tabela de empresas
            empresas_df = pd.DataFrame({
                "Empresa": grupo["emp"]
            })
            
            # Filtrar dados destas empresas para mostrar resultados individuais
            if len(grupo["emp"]) > 0:
                resultados_individuais = df_filtrado[df_filtrado["emp"].isin(grupo["emp"])].groupby("emp", as_index=False).agg({
                    "Resultado para o Estado Acionista": "sum",
                    "setor": "first" if "setor" in df_filtrado.columns else None
                })
                
                # Mesclar com a tabela de empresas
                if "setor" in resultados_individuais.columns:
                    empresas_df = empresas_df.merge(
                        resultados_individuais[["emp", "Resultado para o Estado Acionista", "setor"]],
                        left_on="Empresa",
                        right_on="emp",
                        how="left"
                    ).drop(columns=["emp"])
                else:
                    empresas_df = empresas_df.merge(
                        resultados_individuais[["emp", "Resultado para o Estado Acionista"]],
                        left_on="Empresa",
                        right_on="emp",
                        how="left"
                    ).drop(columns=["emp"])
                
                # Ordenar por resultado
                empresas_df = empresas_df.sort_values(by="Resultado para o Estado Acionista", ascending=False)
                
                # Renomear colunas
                empresas_df.columns = ["Empresa", "Resultado (R$)"] + (["Setor"] if "setor" in resultados_individuais.columns else [])
                
                # Exibir tabela
                st.dataframe(
                    empresas_df,
                    column_config={
                        "Resultado (R$)": st.column_config.NumberColumn(
                            "Resultado (R$)",
                            format="R$ %.2f"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
            
            st.markdown("---")


st.subheader("Resultado Líquido Total para o Estado - acumulado 2020 a 2023", divider="green")

st.write("""

O gráfico abaixo apresenta a evolução do resultado líquido total das empresas estatais do Distrito Federal para o Governo, no período de 2020 a 2023, destacando uma trajetória predominantemente negativa. Ao longo dos quatro anos, o acumulado reflete déficits significativos, com ênfase no ano de 2022, que registrou o maior prejuízo, totalizando R$ -2,1 bilhões. Essa deterioração acentuada pode ser atribuída a uma combinação de fatores, como desafios macroeconômicos, aumento de custos operacionais, e limitações na geração de receitas próprias em setores estratégicos como transporte, habitação e urbanização.

O ano de 2020 também apresentou um resultado negativo expressivo, com um déficit total de R$ 1,15 bilhão, refletindo esforços de recuperação econômica, mas ainda marcado por fragilidades operacionais e desafios estruturais.

No entanto, em 2023, observa-se uma redução significativa no déficit total, que foi reduzido para R$ -927 milhões, representando o menor prejuízo do período analisado. Esse resultado pode indicar uma tendência de recuperação financeira, impulsionada por melhorias na governança corporativa e maior eficiência em setores como financeiro e energia, que contribuíram positivamente para mitigar os impactos negativos de outras áreas deficitárias. Apesar da melhora relativa, o acumulado negativo ao longo dos anos destaca a necessidade de ações mais estruturantes para reverter a trajetória de prejuízos, garantindo maior sustentabilidade financeira para as empresas públicas do Distrito Federal.

""")	

# Filtrar os dados entre 2020 e 2023 para o estado DF
df_filtrado = df[(df["Estado"] == "DF") & (df["Ano"].between(2020, 2023))].copy()

# Verificar se há dados disponíveis
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para o DF entre 2020 e 2023.")
else:
    # Agrupar por ano e somar os resultados para cada ano
    df_agrupado_por_ano = df_filtrado.groupby("Ano", as_index=False).agg({
        "Resultado para o Estado Acionista": "sum"
    })
    
    # Ordenar os resultados por ano (crescente)
    df_agrupado_por_ano.sort_values(by="Ano", ascending=True, inplace=True)
    
    # Adicionar coluna formatada para exibição
    df_agrupado_por_ano["Resultado Formatado"] = df_agrupado_por_ano["Resultado para o Estado Acionista"].apply(
        lambda x: f"R$ {x:,.2f}"
    )
    
    # Calcular estatísticas para contextualização
    total_acumulado = df_agrupado_por_ano["Resultado para o Estado Acionista"].sum()
    media_anual = df_agrupado_por_ano["Resultado para o Estado Acionista"].mean()
    pior_ano = df_agrupado_por_ano.loc[df_agrupado_por_ano["Resultado para o Estado Acionista"].idxmin()]
    melhor_ano = df_agrupado_por_ano.loc[df_agrupado_por_ano["Resultado para o Estado Acionista"].idxmax()]
    
    # Exibir métricas resumidas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Resultado Total Acumulado", 
            f"R$ {total_acumulado:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Média Anual", 
            f"R$ {media_anual:,.2f}",
            delta=None
        )
    
    with col3:
        # Comparar o resultado do último ano com o do ano anterior
        if len(df_agrupado_por_ano) >= 2:
            ultimo_ano = df_agrupado_por_ano.iloc[-1]
            penultimo_ano = df_agrupado_por_ano.iloc[-2]
            variacao = ultimo_ano["Resultado para o Estado Acionista"] - penultimo_ano["Resultado para o Estado Acionista"]
            variacao_percentual = (variacao / abs(penultimo_ano["Resultado para o Estado Acionista"])) * 100 if penultimo_ano["Resultado para o Estado Acionista"] != 0 else 0
            
            st.metric(
                f"Variação {ultimo_ano['Ano']}/{penultimo_ano['Ano']}", 
                f"R$ {variacao:,.2f}",
                f"{variacao_percentual:.1f}%",
                delta_color="normal" if variacao > 0 else "inverse"
            )
        else:
            st.metric("Variação Anual", "Dados insuficientes")
    
    # Criar o gráfico de barras com Plotly Express
    fig = px.bar(
        df_agrupado_por_ano,
        x="Resultado para o Estado Acionista",
        y="Ano",
        orientation="h",
        text="Resultado Formatado",
        labels={
            "Resultado para o Estado Acionista": "Valor (R$)", 
            "Ano": ""  # Remover label do eixo Y para maior limpeza visual
        },
        color="Resultado para o Estado Acionista",
        color_continuous_scale=["#F46045", "#F46045", "#007acc", "#007acc"],
        color_continuous_midpoint=0
    )
    
    # Configurar formatação do texto e hover
    fig.update_traces(
        hovertemplate="<b>Ano: %{y}</b><br>Resultado: R$ %{x:,.2f}<extra></extra>",
        textposition="outside",
        textfont=dict(color="black", size=12),
        cliponaxis=False
    )
    
    # Linha de referência no zero
    fig.add_vline(
        x=0, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Zero", 
        annotation_position="top"
    )
    
    # Adicionar linhas de tendência
    fig.add_shape(
        type="line",
        x0=df_agrupado_por_ano["Resultado para o Estado Acionista"].min() * 1.05,  # Estender um pouco além do mínimo
        y0=df_agrupado_por_ano["Ano"].min(),
        x1=df_agrupado_por_ano["Resultado para o Estado Acionista"].max() * 1.05,  # Estender um pouco além do máximo
        y1=df_agrupado_por_ano["Ano"].max(),
        line=dict(color="gray", width=1, dash="dot"),
    )
    
    # Ajustar o layout
    fig.update_layout(
        height=400,
        plot_bgcolor="white",
        paper_bgcolor="white",
        title={
            "text": "<b>Evolução do Resultado para o Estado (2020-2023)</b>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 20, "color": "black"}
        },
        xaxis=dict(
            title=dict(text="Resultado para o Estado Acionista (R$)", font=dict(size=14, color="black")),
            tickfont=dict(size=12, color="black"),
            gridcolor="lightgray",
            zerolinecolor="black",
            zerolinewidth=1.5,
            range=[min(df_agrupado_por_ano["Resultado para o Estado Acionista"]) * 1.1, 0]  # Ajustar para que todos os valores sejam visíveis
        ),
        yaxis=dict(
            tickfont=dict(size=14, color="black", weight="bold"),
            gridcolor="white"
        ),
        coloraxis_showscale=False,  # Ocultar a escala de cores
        margin=dict(l=50, r=120, t=80, b=50)  # Aumentar margem direita para acomodar valores
    )
    
    # Adicionar anotações para destacar os valores extremos
    fig.add_annotation(
        x=pior_ano["Resultado para o Estado Acionista"],
        y=pior_ano["Ano"],
        text="Pior resultado",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#F46045",
        arrowsize=1,
        arrowwidth=2,
        ax=-40,
        ay=-30,
        font=dict(size=12, color="#F46045"),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#F46045",
        borderwidth=1,
        borderpad=4
    )
    
    fig.add_annotation(
        x=melhor_ano["Resultado para o Estado Acionista"],
        y=melhor_ano["Ano"],
        text="Melhor resultado",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#007acc",
        arrowsize=1,
        arrowwidth=2,
        ax=-40,
        ay=30,
        font=dict(size=12, color="#007acc"),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#007acc",
        borderwidth=1,
        borderpad=4
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Adicionar seção expandível com detalhes
    with st.expander("📊 Ver detalhes da evolução anual"):
        # Preparar tabela detalhada
        tabela = df_agrupado_por_ano[["Ano", "Resultado para o Estado Acionista"]].copy()
        tabela.columns = ["Ano", "Resultado (R$)"]
        
        # Calcular variação em relação ao ano anterior
        tabela["Variação em Relação ao Ano Anterior (R$)"] = tabela["Resultado (R$)"].diff()
        tabela["Variação em Relação ao Ano Anterior (%)"] = tabela["Resultado (R$)"].pct_change() * 100
        
        # Adicionar linha com o total acumulado
        total_row = pd.DataFrame({
            "Ano": ["Total Acumulado"],
            "Resultado (R$)": [total_acumulado],
            "Variação em Relação ao Ano Anterior (R$)": [None],
            "Variação em Relação ao Ano Anterior (%)": [None]
        })
        tabela = pd.concat([tabela, total_row], ignore_index=True)
        
        # Exibir tabela formatada
        st.dataframe(
            tabela,
            column_config={
                "Resultado (R$)": st.column_config.NumberColumn(
                    "Resultado (R$)",
                    format="R$ %.2f"
                ),
                "Variação em Relação ao Ano Anterior (R$)": st.column_config.NumberColumn(
                    "Variação em Relação ao Ano Anterior (R$)",
                    format="R$ %.2f"
                ),
                "Variação em Relação ao Ano Anterior (%)": st.column_config.NumberColumn(
                    "Variação em Relação ao Ano Anterior (%)",
                    format="%.2f%%"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Análise de tendência
        st.markdown("### Análise de tendência")
        
        if df_agrupado_por_ano["Resultado para o Estado Acionista"].iloc[-1] > df_agrupado_por_ano["Resultado para o Estado Acionista"].iloc[0]:
            st.success("**Tendência de melhoria ao longo do período analisado.**")
            st.write(f"O resultado do último ano ({df_agrupado_por_ano['Ano'].iloc[-1]}) foi R$ {df_agrupado_por_ano['Resultado para o Estado Acionista'].iloc[-1] - df_agrupado_por_ano['Resultado para o Estado Acionista'].iloc[0]:,.2f} superior ao do primeiro ano da série ({df_agrupado_por_ano['Ano'].iloc[0]}).")
        else:
            st.error("**Tendência de deterioração ao longo do período analisado.**")
            st.write(f"O resultado do último ano ({df_agrupado_por_ano['Ano'].iloc[-1]}) foi R$ {df_agrupado_por_ano['Resultado para o Estado Acionista'].iloc[0] - df_agrupado_por_ano['Resultado para o Estado Acionista'].iloc[-1]:,.2f} inferior ao do primeiro ano da série ({df_agrupado_por_ano['Ano'].iloc[0]}).")
        
        # Visualização alternativa - gráfico de linha
        st.markdown("### Evolução temporal")
        
        fig_line = px.line(
            df_agrupado_por_ano,
            x="Ano",
            y="Resultado para o Estado Acionista",
            markers=True,
            labels={"Resultado para o Estado Acionista": "Resultado (R$)", "Ano": ""}
        )
        
        fig_line.update_traces(
            line=dict(width=3, color="#007acc"),
            marker=dict(size=10, color="#007acc"),
            hovertemplate="<b>Ano: %{x}</b><br>Resultado: R$ %{y:,.2f}<extra></extra>"
        )
        
        fig_line.add_hline(
            y=0, 
            line_dash="dash", 
            line_color="gray",
            annotation_text="Equilíbrio", 
            annotation_position="right"
        )
        
        fig_line.update_layout(
            height=350,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                tickmode='array',
                tickvals=df_agrupado_por_ano["Ano"],
                tickfont=dict(size=12, color="black")
            ),
            yaxis=dict(
                title=dict(text="Resultado para o Estado (R$)", font=dict(size=14, color="black")),
                tickfont=dict(size=12, color="black"),
                gridcolor="lightgray",
                zerolinecolor="black",
                zerolinewidth=1.5
            ),
            margin=dict(l=50, r=50, t=30, b=50)
        )
        
        st.plotly_chart(fig_line, use_container_width=True)

# Botão para voltar à página inicial
if st.button("Voltar à Página Inicial"):
    st.switch_page("Início.py")