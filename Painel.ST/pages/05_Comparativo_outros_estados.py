# Importando as bibliotecas
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Caminho relativo ao arquivo CSV
file_path = 'BD_Completo_Nacional_Formatado.csv'

# Carregando o arquivo CSV no Pandas DataFrame
df = pd.read_csv(file_path)

# Configurações da página
st.set_page_config(
    page_title="Comparativo com outros Estados",
    page_icon="📈",
    layout="wide"
)

# --- NOVO BLOCO DE CSS PARA PADRONIZAÇÃO ---
st.markdown("""
<style>
    /* 1. FUNDO BRANCO */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
    }

    /* 2. TÍTULOS EM red */
    h1, h2, h3, h4, h5, h6, [data-testid="stHeader"], .stHeader {
        color: red !important;
    }
    
    /* Ajuste da cor da linha divisória (divider) para laranja */
    hr {
        border-top-color: red !important;
    }

    /* 3. BOTÕES LARANJAS */
    div.stButton > button {
        background-color: #fb8c00 !important;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
    }

    /* 4. TEXTOS GERAIS EM CINZA ESCURO */
    [data-testid="stWidgetLabel"], .stMarkdown {
        color: #2F2F2F !important;
    }
</style>
""", unsafe_allow_html=True)

st.header("Comparativo com outros Estados", divider="violet")

# Conteúdo específico desta página
st.write("""

Esta seção do painel incorpora quatro gráficos distintos que oferecem uma análise detalhada das empresas estatais. O primeiro gráfico ilustra o Total de empresas por Estado, ano e setor, fornecendo uma visão clara sobre a distribuição e evolução dessas entidades ao longo do tempo e de acordo com diferentes segmentos econômicos. 

O segundo gráfico apresenta o Resultado líquido das empresas para o Estado Acionista por Estado e por ano, permitindo uma observação dos lucros e prejuízos gerados em cada Estado ao longo dos anos.

O terceiro gráfico vai além, detalhando o Resultado Líquido das Empresas para o Estado Acionista por Estado, por ano e por setor, o que ajuda a identificar quais setores contribuem mais significativamente para os resultados financeiros de cada Estado. 

Por fim, o quarto gráfico aborda o Resultado Líquido das Empresas para o Estado Acionista por Estado, por ano e por dependência, oferecendo insights cruciais sobre a relação entre dependência financeira de certas empresas e seu impacto nos cofres estaduais. Juntos, esses gráficos proporcionam uma análise robusta e abrangente, essencial para a avaliação do desempenho das empresas estatais do Distrito Federal no cenário nacional.

""")	


st.subheader("Total de empresas por Estado, por ano e por setor", divider="violet")

# Conteúdo específico desta página
st.write("""

O gráfico apresentado a seguir oferece um panorama abrangente sobre a distribuição de empresas estatais em diferentes estados brasileiros, segmentado por setor e ano, permitindo uma análise comparativa entre as administrações estaduais e a evolução no número de empresas ao longo do tempo. A diversidade setorial e a concentração de empresas em determinados estados refletem tanto as prioridades políticas quanto as condições econômicas regionais, além de apontar para diferenças marcantes na gestão de estatais entre os estados.

Alguns estados destacam-se pela elevada concentração de empresas estatais em setores estratégicos, como energia, transporte e habitação, que estão diretamente relacionados ao fornecimento de serviços essenciais. Estados com maior participação nesses setores demonstram um comprometimento significativo com o atendimento de demandas regionais por infraestrutura e serviços públicos. Por outro lado, estados com menor número de empresas em setores como pesquisa e assistência técnica agropecuária ou saneamento podem indicar menor diversificação econômica ou dependência de iniciativas privadas para suprir essas demandas.

A evolução temporal revela mudanças no número de empresas estatais, o que pode estar relacionado à criação de novas empresas para atender demandas específicas ou à reestruturação de estatais existentes. Essa dinâmica é evidente em anos em que houve um crescimento expressivo em determinados setores, como energia e habitação, sugerindo políticas de expansão e investimento público para impulsionar o desenvolvimento regional. Em contrapartida, a redução no número de empresas em outros estados pode refletir iniciativas de privatização, fechamento de empresas deficitárias ou fusões que visam otimizar a gestão e reduzir custos operacionais.

Adicionalmente, a presença significativa de setores como transporte e saneamento em alguns estados aponta para uma forte dependência de subsídios governamentais nesses serviços essenciais. Em contrapartida, setores como financeiro e energia, que possuem maior potencial de geração de receita, demonstram maior presença em estados com políticas públicas mais orientadas ao mercado e que utilizam essas empresas como importantes alavancas econômicas. Essa variação entre os estados reflete as diferenças nas estratégias de governança e prioridades regionais, influenciando diretamente a sustentabilidade financeira das empresas e seu impacto no desenvolvimento local.

De forma geral, o gráfico destaca a importância de estratégias diferenciadas e adaptadas às características regionais para a gestão de empresas estatais. Ao mesmo tempo, a análise evidencia oportunidades para aumentar a eficiência em setores deficitários e potencializar os resultados financeiros em áreas com maior capacidade de geração de receita, como energia e serviços financeiros. O comparativo entre estados fornece insights valiosos para a formulação de políticas públicas mais eficazes e sustentáveis.

""")	

# Filtrar os estados para garantir que todos estão sendo incluídos
df_filtrado = df[df["Estado"].notna()]

# Verificar se há dados disponíveis
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis com informação de Estado.")
else:
    # Interface de seleção para filtrar os dados (opcional, pode ser removido se quiser manter exatamente como o original)
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtrar anos disponíveis
        anos_disponíveis = sorted(df_filtrado["Ano"].unique())
        anos_selecionados = st.multiselect(
            "Selecione os anos:",
            options=anos_disponíveis,
            default=anos_disponíveis  # Selecionar todos por padrão
        )
    
    with col2:
        # Filtrar estados disponíveis
        estados_disponíveis = sorted(df_filtrado["Estado"].unique())
        estados_selecionados = st.multiselect(
            "Selecione os estados:",
            options=estados_disponíveis,
            default=estados_disponíveis  # Selecionar todos por padrão
        )
    
    # Aplicar filtros se selecionados
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado["Ano"].isin(anos_selecionados)]
    
    if estados_selecionados:
        df_filtrado = df_filtrado[df_filtrado["Estado"].isin(estados_selecionados)]
    
    # Verificar novamente após filtros
    if len(df_filtrado) == 0:
        st.warning("Nenhum dado disponível com os filtros selecionados.")
    else:
        # Agrupar por estado, ano e setor para contar as empresas - exatamente como no original
        agrupado = df_filtrado.groupby(["Estado", "Ano", "setor"]).size().unstack(fill_value=0)
        
        # Ajustar os índices para adicionar mais espaçamento (concatenando Estado e Ano)
        x_labels = ["{}, {}".format(estado, ano) for estado, ano in agrupado.index]
        x = np.arange(len(x_labels))
        
        # Criar figura matplotlib
        fig, ax = plt.subplots(figsize=(18, 10))  # Aumentando o tamanho da figura
        width = 0.9  # Largura das barras, para aumentar o espaçamento entre elas
        
        # Plotar gráfico de barras empilhadas - mesmo gráfico do original
        agrupado.plot(kind="bar", stacked=True, ax=ax, width=width)
        
        # Ajustar os rótulos do eixo X para que haja mais espaçamento e garantir que fiquem visíveis
        ax.set_xticks(x)
        ax.set_xticklabels(
            x_labels, rotation=90, ha="center", fontsize=8
        )  # Rotacionando os rótulos
        
        # Definir título e rótulos
        plt.title("Total de Empresas Estatais por Estado, Ano e Setor", fontsize=16)
        plt.xlabel("Estado, Ano", fontsize=14)
        plt.ylabel("Número de Empresas", fontsize=14)
        
        # Ajustar a posição da legenda e o layout para evitar sobreposição
        plt.legend(title="Setor", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.tight_layout()
        
        # Exibir no Streamlit - aqui está a principal diferença da versão original
        st.pyplot(fig)
        
        # Adicionar opção para download do gráfico (funcionalidade extra)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        
        btn = st.download_button(
            label="Baixar Gráfico",
            data=buffer,
            file_name="total_empresas_estatais_por_estado_ano_setor.png",
            mime="image/png"
        )

st.subheader("Resultado Líquido das Empresas para o Estado Acionista por Estado e por ano", divider="violet")

# Conteúdo específico desta página
st.write("""

O gráfico demonstra o desempenho financeiro das empresas estatais para seus respectivos estados acionistas, distribuído por ano e estado, evidenciando uma discrepância significativa entre lucros e prejuízos ao longo do período analisado. A análise revela que, enquanto alguns estados conseguem gerar resultados positivos consistentes por meio de suas empresas públicas, outros enfrentam déficits expressivos que impactam negativamente suas finanças públicas. A variação observada reflete não apenas a natureza e gestão das empresas estatais em cada estado, mas também as condições econômicas regionais e as políticas públicas adotadas.

Estados como São Paulo e Minas Gerais aparecem com resultados positivos significativos em anos específicos, impulsionados, sobretudo, por empresas dos setores financeiro e energético. Essas empresas, caracterizadas por maior eficiência e potencial de geração de receita, têm se destacado em seus mercados e contribuído de forma relevante para o equilíbrio fiscal dos estados. Esse desempenho é reflexo de uma gestão orientada para resultados e da diversificação de operações, o que permite maior resiliência frente às variações econômicas e setoriais.

Em contrapartida, estados como Rio de Janeiro e Rio Grande do Sul enfrentam déficits expressivos ao longo de vários anos, com destaque para empresas de setores como transporte e habitação, que tradicionalmente demandam subsídios governamentais para manter suas operações. O estado do Rio de Janeiro, em particular, apresenta quedas acentuadas nos resultados líquidos, refletindo problemas estruturais, altos custos operacionais e dificuldades na geração de receitas suficientes para equilibrar despesas. Esse padrão aponta para a necessidade de reestruturação nos modelos de negócios dessas empresas e maior eficiência na alocação de recursos públicos.

O gráfico também evidencia períodos de deterioração financeira generalizada, especialmente em anos marcados por crises econômicas, como 2020, que refletiram os impactos da pandemia de COVID-19. Nesse período, a maioria dos estados registrou resultados líquidos negativos, indicando os desafios enfrentados pelas empresas estatais em manter suas operações durante um contexto de retração econômica e aumento de custos. A análise global do gráfico reforça a importância de estratégias diferenciadas e adaptações estruturais, tanto para melhorar os desempenhos financeiros quanto para garantir a sustentabilidade das empresas públicas em estados com desafios fiscais mais agudos.

""")	

# Filtrar os dados novamente para garantir que estamos usando os dados filtrados pelos seletores
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para gerar o gráfico de resultado líquido.")
else:
    # Interface de filtros específica para este gráfico
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtrar anos disponíveis
        anos_resultado = sorted(df_filtrado["Ano"].unique())
        anos_selecionados_resultado = st.multiselect(
            "Filtrar por anos:",
            options=anos_resultado,
            default=anos_resultado,
            key="anos_resultado"
        )
    
    with col2:
        # Filtrar estados disponíveis
        estados_resultado = sorted(df_filtrado["Estado"].unique())
        estados_selecionados_resultado = st.multiselect(
            "Filtrar por estados:",
            options=estados_resultado,
            default=estados_resultado,  # Selecionar todos por padrão
            key="estados_resultado"
        )
    
    # Aplicar filtros se selecionados
    df_resultado = df_filtrado.copy()
    
    if anos_selecionados_resultado:
        df_resultado = df_resultado[df_resultado["Ano"].isin(anos_selecionados_resultado)]
    
    if estados_selecionados_resultado:
        df_resultado = df_resultado[df_resultado["Estado"].isin(estados_selecionados_resultado)]
    
    # Verificar novamente após filtros
    if len(df_resultado) == 0:
        st.warning("Nenhum dado disponível com os filtros selecionados para o gráfico de resultado líquido.")
    else:
        # Certifique-se de que os valores de 'Resultado para o Estado Acionista' sejam numéricos
        df_resultado["Resultado para o Estado Acionista"] = pd.to_numeric(
            df_resultado["Resultado para o Estado Acionista"], errors="coerce"
        )
        
        # Agrupar por Estado e Ano para somar o Resultado Líquido para o Estado Acionista
        agrupado_resultado = (
            df_resultado.groupby(["Estado", "Ano"])["Resultado para o Estado Acionista"]
            .sum()
            .reset_index()
        )
        
        # Criar coluna combinada de Estado e Ano para o eixo X
        agrupado_resultado["Estado_Ano"] = agrupado_resultado["Estado"] + ", " + agrupado_resultado["Ano"].astype(str)
        
        # Ordenar por Estado e Ano para melhor visualização
        agrupado_resultado = agrupado_resultado.sort_values(by=["Estado", "Ano"])
        
        # Determinar as cores com base se o valor é positivo ou negativo
        agrupado_resultado["color"] = agrupado_resultado[
            "Resultado para o Estado Acionista"
        ].apply(lambda x: "#007acc" if x > 0 else "#F46045")
        
        # Escolha entre gráfico de barras ou gráfico de linha
        tipo_grafico = st.radio(
            "Escolha o tipo de visualização:",
            options=["Barras", "Linhas por Estado"],
            horizontal=True,
            key="tipo_grafico_resultado"
        )
        
        # Modificação para gráfico de barras

        if tipo_grafico == "Barras":
            # Criar gráfico de barras interativo com Plotly
            fig = go.Figure()
            
            # Adicionar barras ao gráfico
            for i, row in agrupado_resultado.iterrows():
                fig.add_trace(
                    go.Bar(
                        x=[row["Estado_Ano"]],
                        y=[row["Resultado para o Estado Acionista"]],
                        name=row["Estado_Ano"],
                        hoverinfo="text",
                        textposition="none",
                        hovertext=f"<b>Estado:</b> {row['Estado']}<br><b>Ano:</b> {row['Ano']}<br><b>Resultado:</b> R$ {row['Resultado para o Estado Acionista']:,.2f}",
                        marker_color=row["color"],
                    )
                )
            
            # Adicionar linha de referência no zero
            fig.add_shape(
                type="line",
                x0=0,
                y0=0,
                x1=1,
                y1=0,
                line=dict(color="gray", width=1, dash="dash"),
                xref="paper",
                yref="y"
            )
            
            # Atualizar layout do gráfico
            fig.update_layout(
                title="Resultado Líquido das Empresas para o Estado Acionista",
                xaxis_title="Estado, Ano",
                yaxis_title="Resultado Líquido (R$)",
                yaxis=dict(
                    gridcolor="lightgray",
                    title=dict(font=dict(color="black", size=14)),  # Cor preta para título do eixo Y
                    tickfont=dict(color="black", size=12),  # Cor preta para valores do eixo Y
                ),
                xaxis=dict(
                    tickangle=-90,
                    tickfont=dict(size=10, color="black"),  # Cor preta para valores do eixo X
                    title=dict(font=dict(color="black", size=14)),  # Cor preta para título do eixo X
                ),
                showlegend=False,
                template="plotly_white",
                height=600,
                margin=dict(l=40, r=40, t=60, b=150),
                plot_bgcolor="white",
                paper_bgcolor="white",
                title_font=dict(color="black"),  # Cor preta para título principal
            )
            
            # Mostrar o gráfico
            st.plotly_chart(fig, use_container_width=True)

        else:  # Gráfico de linhas por Estado
            # Criar gráfico de linhas com Plotly Express
            fig = px.line(
                agrupado_resultado,
                x="Ano",
                y="Resultado para o Estado Acionista",
                color="Estado",
                markers=True,
                labels={
                    "Resultado para o Estado Acionista": "Resultado Líquido (R$)",
                    "Ano": "Ano",
                    "Estado": "Estado"
                },
                title="Evolução do Resultado Líquido por Estado ao Longo dos Anos",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            
            # Adicionar linha de referência no zero
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color="gray",
                annotation_text="Equilíbrio",
                annotation_position="right"
            )
            
            # Atualizar formatação do hover
            fig.update_traces(
                hovertemplate="<b>%{customdata[0]}</b><br>Ano: %{x}<br>Resultado: R$ %{y:,.2f}<extra></extra>",
                customdata=agrupado_resultado[["Estado"]],
            )
            
            # Atualizar layout do gráfico
            fig.update_layout(
                xaxis_title="Ano",
                yaxis_title="Resultado Líquido (R$)",
                legend_title="Estado",
                template="plotly_white",
                height=500,
                margin=dict(l=40, r=40, t=60, b=40),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="black", size=12)  # Cor preta para legenda
                ),
                xaxis=dict(
                    title=dict(font=dict(color="black", size=14)),  # Cor preta para título do eixo X
                    tickfont=dict(color="black", size=12),  # Cor preta para valores do eixo X
                    gridcolor="lightgray"
                ),
                yaxis=dict(
                    title=dict(font=dict(color="black", size=14)),  # Cor preta para título do eixo Y
                    tickfont=dict(color="black", size=12),  # Cor preta para valores do eixo Y
                    gridcolor="lightgray"
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                title_font=dict(color="black")  # Cor preta para título principal
            )
            
            # Mostrar o gráfico
            st.plotly_chart(fig, use_container_width=True)
        
        # Adicionar seção expandível com detalhes
        with st.expander("📊 Ver detalhes do resultado líquido"):
            # Preparar dados para exibição
            tabela = agrupado_resultado[["Estado", "Ano", "Resultado para o Estado Acionista"]].copy()
            tabela = tabela.sort_values(by=["Estado", "Ano"])
            
            # Mostrar tabela formatada
            st.dataframe(
                tabela,
                column_config={
                    "Resultado para o Estado Acionista": st.column_config.NumberColumn(
                        "Resultado Líquido (R$)",
                        format="R$ %.2f"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Análise adicional
            col1, col2 = st.columns(2)
            
            with col1:
                # Estado com melhor resultado
                melhor_estado = agrupado_resultado.loc[agrupado_resultado["Resultado para o Estado Acionista"].idxmax()]
                st.success(f"**Maior resultado positivo**")
                st.write(f"**Estado**: {melhor_estado['Estado']}")
                st.write(f"**Ano**: {melhor_estado['Ano']}")
                st.write(f"**Valor**: R$ {melhor_estado['Resultado para o Estado Acionista']:,.2f}")
            
            with col2:
                # Estado com pior resultado
                pior_estado = agrupado_resultado.loc[agrupado_resultado["Resultado para o Estado Acionista"].idxmin()]
                st.error(f"**Maior resultado negativo**")
                st.write(f"**Estado**: {pior_estado['Estado']}")
                st.write(f"**Ano**: {pior_estado['Ano']}")
                st.write(f"**Valor**: R$ {pior_estado['Resultado para o Estado Acionista']:,.2f}")
            
            # Estatísticas adicionais
            st.markdown("### Estatísticas por Estado")
            
            # Agrupar por estado para análise
            por_estado = agrupado_resultado.groupby("Estado")["Resultado para o Estado Acionista"].agg(
                ["sum", "mean", "min", "max", "count"]
            ).reset_index()
            por_estado.columns = ["Estado", "Total", "Média", "Mínimo", "Máximo", "Anos com Dados"]
            
            # Ordenar por total
            por_estado = por_estado.sort_values(by="Total", ascending=False)
            
            # Mostrar tabela formatada
            st.dataframe(
                por_estado,
                column_config={
                    "Total": st.column_config.NumberColumn("Total (R$)", format="R$ %.2f"),
                    "Média": st.column_config.NumberColumn("Média Anual (R$)", format="R$ %.2f"),
                    "Mínimo": st.column_config.NumberColumn("Mínimo (R$)", format="R$ %.2f"),
                    "Máximo": st.column_config.NumberColumn("Máximo (R$)", format="R$ %.2f"),
                },
                hide_index=True,
                use_container_width=True
            )




st.subheader("Resultado Líquido das Empresas para o Estado Acionista por Estado, por ano e por setor", divider="violet")

# Conteúdo específico desta página
st.write("""

O gráfico apresenta uma visão detalhada do resultado líquido das empresas estatais brasileiras, analisado por estado, ano e setor de atuação. Essa segmentação permite identificar padrões setoriais de desempenho e tendências financeiras que variam significativamente entre regiões e períodos, evidenciando tanto as potencialidades quanto os desafios enfrentados pelos estados no gerenciamento de suas estatais.

Estados que possuem forte atuação em setores como financeiro e energia, a exemplo de São Paulo, Minas Gerais e Paraná, frequentemente registram resultados líquidos positivos. Esses setores se destacam pela elevada capacidade de geração de receita, graças à robustez de seus modelos de negócio, que combinam eficiência operacional e diversificação de serviços. Empresas financeiras e de energia, como bancos estatais regionais e concessionárias de energia elétrica, demonstram ser pilares importantes para o equilíbrio fiscal de seus estados, desempenhando papel estratégico em suas economias.

Por outro lado, o gráfico destaca o impacto negativo de setores como habitação e urbanização, transporte e pesquisa e assistência técnica agropecuária, que frequentemente apresentam déficits significativos. Esses resultados negativos são mais acentuados em estados como Rio de Janeiro e Rio Grande do Sul, onde empresas de transporte e habitação enfrentam desafios estruturais, incluindo alta dependência de subsídios governamentais e dificuldade em gerar receitas que cubram os custos operacionais. Essa situação é agravada em anos de crise econômica, como 2020, quando os efeitos da pandemia de COVID-19 intensificaram os déficits em diversos setores.

Adicionalmente, observa-se uma correlação entre os resultados líquidos negativos e a predominância de empresas em setores que atendem a demandas sociais essenciais. Empresas de saneamento, saúde e transporte, embora deficitárias em muitos casos, desempenham papéis críticos no cumprimento de políticas públicas e no atendimento à população. Isso reforça a necessidade de um equilíbrio entre eficiência financeira e impacto social, principalmente em estados com restrições fiscais mais severas.

Por fim, a análise segmentada por setor ao longo dos anos destaca a importância da diversificação econômica e do fortalecimento da governança corporativa nas estatais. Estados que priorizam investimentos em setores de alta rentabilidade, como energia e financeiro, apresentam maior resiliência fiscal, enquanto estados mais dependentes de setores deficitários precisam buscar soluções estratégicas, como reestruturação de empresas, ampliação de parcerias público-privadas e modernização tecnológica. Esses ajustes são cruciais para garantir a sustentabilidade financeira e o impacto positivo das estatais no desenvolvimento econômico e social de suas respectivas regiões.

""")	

# Filtrar os dados para este gráfico
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para gerar o gráfico de resultado líquido por setor.")
else:
    # Interface de filtros específica para este gráfico
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtrar anos disponíveis
        anos_resultado_setor = sorted(df_filtrado["Ano"].unique())
        anos_selecionados_resultado_setor = st.multiselect(
            "Filtrar por anos:",
            options=anos_resultado_setor,
            default=anos_resultado_setor,
            key="anos_resultado_setor"
        )
    
    with col2:
        # Filtrar estados disponíveis - todos selecionados por padrão
        estados_resultado_setor = sorted(df_filtrado["Estado"].unique())
        estados_selecionados_resultado_setor = st.multiselect(
            "Filtrar por estados:",
            options=estados_resultado_setor,
            default=estados_resultado_setor,  # Todos os estados selecionados por padrão
            key="estados_resultado_setor"
        )
    
    # Aplicar filtros se selecionados
    df_resultado_setor = df_filtrado.copy()
    
    if anos_selecionados_resultado_setor:
        df_resultado_setor = df_resultado_setor[df_resultado_setor["Ano"].isin(anos_selecionados_resultado_setor)]
    
    if estados_selecionados_resultado_setor:
        df_resultado_setor = df_resultado_setor[df_resultado_setor["Estado"].isin(estados_selecionados_resultado_setor)]
    
    # Verificar novamente após filtros
    if len(df_resultado_setor) == 0:
        st.warning("Nenhum dado disponível com os filtros selecionados para o gráfico de resultado líquido por setor.")
    else:
        # Verificar se a coluna 'setor' existe
        if 'setor' not in df_resultado_setor.columns:
            st.error("A coluna 'setor' não foi encontrada nos dados. Não é possível gerar o gráfico.")
        else:
            # Certifique-se de que os valores sejam numéricos
            df_resultado_setor["Resultado para o Estado Acionista"] = pd.to_numeric(
                df_resultado_setor["Resultado para o Estado Acionista"], errors="coerce"
            )
            
            # Agrupar por Estado, Ano e Setor para somar o Resultado Líquido
            agrupado_resultado = (
                df_resultado_setor.groupby(["Estado", "Ano", "setor"])["Resultado para o Estado Acionista"]
                .sum()
                .unstack(fill_value=0)
            )
            
            # Preparando os dados para o matplotlib
            fig, ax = plt.subplots(figsize=(18, 10))
            width = 0.9  # Largura das barras para maior espaçamento
            
            # Plotar gráfico de barras empilhadas
            agrupado_resultado.plot(kind="bar", stacked=True, ax=ax, width=width)
            
            # Ajustar os índices e rótulos
            x_labels = ["{}, {}".format(estado, ano) for estado, ano in agrupado_resultado.index]
            x = np.arange(len(x_labels))
            
            # Configurar os rótulos do eixo X
            ax.set_xticks(x)
            ax.set_xticklabels(x_labels, rotation=90, ha="center", fontsize=8)
            
            # Adicionar linha no zero para facilitar visualização
            ax.axhline(y=0, color='gray', linestyle='-', alpha=0.7, linewidth=0.8)
            
            # Ajustar limites do eixo Y para melhor visualização
            min_value = agrupado_resultado.sum(axis=1).min()
            max_value = agrupado_resultado.sum(axis=1).max()
            y_range_min = min(min_value * 1.1, -500000000) if min_value < 0 else -500000000
            y_range_max = max(max_value * 1.1, 500000000)
            ax.set_ylim(bottom=y_range_min, top=y_range_max)
            
            # Definir título e rótulos
            plt.title("Resultado Líquido das Empresas para o Estado Acionista por Estado, Ano e Setor", fontsize=16)
            plt.xlabel("Estado, Ano", fontsize=14)
            plt.ylabel("Resultado Líquido para o Estado (R$)", fontsize=14)
            
            # Ajustar a posição da legenda
            plt.legend(title="Setor", bbox_to_anchor=(1.05, 1), loc="upper left")
            
            # Ajustar o layout para evitar sobreposição
            plt.tight_layout()
            
            # Exibir gráfico no Streamlit
            st.pyplot(fig)
            
            # Adicionar botão para download
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            
            st.download_button(
                label="Baixar Gráfico",
                data=buffer,
                file_name="resultado_liquido_por_setor.png",
                mime="image/png"
            )
            
            # Adicionar seção de análise expandível
            with st.expander("📊 Ver análise detalhada por setor"):
                # Agrupar por setor para análise global
                setor_analysis = df_resultado_setor.groupby("setor")["Resultado para o Estado Acionista"].agg(
                    ["sum", "mean", "count"]
                ).reset_index()
                setor_analysis.columns = ["Setor", "Total", "Média", "Quantidade de Registros"]
                
                # Ordenar do mais positivo ao mais negativo
                setor_analysis = setor_analysis.sort_values(by="Total", ascending=False)
                
                # Mostrar tabela formatada
                st.dataframe(
                    setor_analysis,
                    column_config={
                        "Total": st.column_config.NumberColumn("Total (R$)", format="R$ %.2f"),
                        "Média": st.column_config.NumberColumn("Média (R$)", format="R$ %.2f")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Análise de melhores e piores setores
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Setores com melhor desempenho")
                    top_setores = setor_analysis.nlargest(3, "Total")
                    
                    for i, row in enumerate(top_setores.itertuples(), 1):
                        st.success(f"**{i}. {row.Setor}**")
                        st.write(f"Total: **R$ {row.Total:,.2f}**")
                        st.write(f"Média: R$ {row.Média:,.2f}")
                        st.write("---")
                
                with col2:
                    st.markdown("### Setores com pior desempenho")
                    bottom_setores = setor_analysis.nsmallest(3, "Total")
                    
                    for i, row in enumerate(bottom_setores.itertuples(), 1):
                        st.error(f"**{i}. {row.Setor}**")
                        st.write(f"Total: **R$ {row.Total:,.2f}**")
                        st.write(f"Média: R$ {row.Média:,.2f}")
                        st.write("---")



st.subheader("Resultado Líquido das Empresas para o Estado Acionista por Estado, por ano e por dependência", divider="violet")

# Conteúdo específico desta página
st.write("""

O gráfico analisa o resultado líquido das empresas estatais por estado, ano e classificação de dependência (dependente, não dependente ou não informado), evidenciando as disparidades de desempenho financeiro das empresas em relação ao suporte recebido de seus respectivos estados acionistas. A segmentação entre empresas dependentes e não dependentes fornece uma visão clara sobre a influência da autonomia financeira na sustentabilidade das estatais.

Empresas não dependentes, representadas em azul no gráfico, apresentam, em sua maioria, resultados líquidos positivos ou menos deficitários. Isso reflete sua capacidade de gerar receitas próprias suficientes para cobrir despesas operacionais e de capital. Estados como São Paulo, Minas Gerais e Paraná têm uma concentração maior de empresas não dependentes que registram desempenho positivo, especialmente em setores como financeiro e energia. Essas empresas contribuem significativamente para o equilíbrio fiscal do estado, demonstrando que a autonomia operacional combinada com boas práticas de governança pode resultar em maior eficiência financeira.

Por outro lado, as empresas dependentes, destacadas em vermelho, apresentam déficits expressivos, que são mais evidentes em estados como Rio de Janeiro e Rio Grande do Sul. Setores como transporte, habitação e urbanização, altamente representados por empresas dependentes, frequentemente demandam aportes financeiros significativos do governo para custear suas operações. Esses déficits refletem não apenas a alta dependência de subsídios governamentais, mas também desafios estruturais relacionados a custos operacionais elevados e modelos de negócios pouco eficientes. Estados com maior concentração de empresas dependentes enfrentam desafios fiscais mais severos, dado o impacto direto desses déficits no orçamento público.

O gráfico também destaca um padrão ao longo do tempo: anos de crises econômicas, como 2020, apresentam déficits mais acentuados, especialmente entre empresas dependentes, devido ao aumento dos custos operacionais e à redução das receitas próprias. Por outro lado, os resultados das empresas não dependentes mostram maior estabilidade e resiliência em momentos de instabilidade econômica, refletindo modelos de negócios mais robustos.

A presença de uma categoria de dados não informados, indicada em cinza, levanta a necessidade de maior transparência nos relatórios financeiros das estatais. A falta de clareza na classificação de dependência pode dificultar análises mais precisas e a formulação de estratégias para melhorar a sustentabilidade financeira das empresas públicas. No geral, o gráfico reforça a importância de fortalecer a governança corporativa, promover a eficiência operacional e buscar alternativas estratégicas, como parcerias público-privadas, especialmente para empresas deficitárias.

""")	

st.subheader("Resultado Líquido das Empresas para o Estado Acionista por Estado, por ano e por dependência", divider="violet")

# Conteúdo específico desta página
st.write("""
O gráfico analisa o resultado líquido das empresas estatais por estado, ano e classificação de dependência (dependente, não dependente ou não informado), evidenciando as disparidades de desempenho financeiro das empresas em relação ao suporte recebido de seus respectivos estados acionistas. A segmentação entre empresas dependentes e não dependentes fornece uma visão clara sobre a influência da autonomia financeira na sustentabilidade das estatais.
""")

# Verificar se há dados disponíveis
if len(df_filtrado) == 0:
    st.warning("Não há dados disponíveis para gerar o gráfico de resultado por dependência.")
else:
    # Verificar se a coluna 'dep' existe no DataFrame
    if 'dep' not in df_filtrado.columns:
        st.error("A coluna 'dep' (dependência) não foi encontrada nos dados. Não é possível gerar o gráfico.")
    else:
        # Interface de filtros específica para este gráfico
        col1, col2 = st.columns(2)
        
        with col1:
            # Filtrar anos disponíveis
            anos_dep = sorted(df_filtrado["Ano"].unique())
            anos_selecionados_dep = st.multiselect(
                "Filtrar por anos:",
                options=anos_dep,
                default=anos_dep,
                key="anos_dep"
            )
        
        with col2:
            # Filtrar estados disponíveis - todos selecionados por padrão
            estados_dep = sorted(df_filtrado["Estado"].unique())
            estados_selecionados_dep = st.multiselect(
                "Filtrar por estados:",
                options=estados_dep,
                default=estados_dep,  # Todos os estados selecionados por padrão
                key="estados_dep"
            )
        
        # Aplicar filtros se selecionados
        df_resultado_dep = df_filtrado.copy()
        
        if anos_selecionados_dep:
            df_resultado_dep = df_resultado_dep[df_resultado_dep["Ano"].isin(anos_selecionados_dep)]
        
        if estados_selecionados_dep:
            df_resultado_dep = df_resultado_dep[df_resultado_dep["Estado"].isin(estados_selecionados_dep)]
        
        # Verificar novamente após filtros
        if len(df_resultado_dep) == 0:
            st.warning("Nenhum dado disponível com os filtros selecionados para o gráfico de resultado por dependência.")
        else:
            # Certifique-se de que os valores sejam numéricos
            df_resultado_dep["Resultado para o Estado Acionista"] = pd.to_numeric(
                df_resultado_dep["Resultado para o Estado Acionista"], errors="coerce"
            )
            
            # Padronizar valores na coluna 'dep' para garantir consistência
            df_resultado_dep['dep'] = df_resultado_dep['dep'].fillna("Não Informado")
            df_resultado_dep['dep'] = df_resultado_dep['dep'].replace({
                'Dependente': 'Dependente',
                'Não Dependente': 'Não Dependente',
                'Não dependente': 'Não Dependente',
                'não dependente': 'Não Dependente',
                'dependente': 'Dependente'
            })
            
            # Agrupar por Estado, Ano e 'dep' para somar o Resultado Líquido para o Estado Acionista
            agrupado_resultado = (
                df_resultado_dep.groupby(["Estado", "Ano", "dep"])["Resultado para o Estado Acionista"]
                .sum()
                .reset_index()
            )
            
            # Juntar Estado e Ano para usar como rótulo
            agrupado_resultado["label"] = (
                agrupado_resultado["Estado"] + ", " + agrupado_resultado["Ano"].astype(str)
            )
            
            # Ordenar o DataFrame com base nos rótulos alfabéticos
            agrupado_resultado.sort_values("label", inplace=True)
            
            # Definir as cores específicas para cada categoria
            color_map = {
                "Não Dependente": "#007acc",
                "Dependente": "#F46045",
                "Não Informado": "rgba(150, 150, 150, 0.8)",
            }
            
            # Criar gráfico de barras interativo com Plotly
            fig = go.Figure()
            
            # Loop sobre cada 'dep' distinto e adicionar como uma série no gráfico
            for categoria in agrupado_resultado['dep'].unique():
                color = color_map.get(categoria, "gray")  # Usar gray como cor padrão se a categoria não estiver no mapa
                df_categoria = agrupado_resultado[agrupado_resultado["dep"] == categoria]
                
                fig.add_trace(
                    go.Bar(
                        x=df_categoria["label"],
                        y=df_categoria["Resultado para o Estado Acionista"],
                        name=categoria,
                        hoverinfo="text",
                        textposition="none",
                        hovertext=df_categoria.apply(
                            lambda row: f"<b>Estado:</b> {row['Estado']}<br><b>Ano:</b> {row['Ano']}<br><b>Dependência:</b> {row['dep']}<br><b>Resultado:</b> R$ {row['Resultado para o Estado Acionista']:,.2f}",
                            axis=1,
                        ),
                        marker_color=color,
                    )
                )
            
            # Linha zero para referência
            fig.add_shape(
                type="line",
                x0=0,
                y0=0,
                x1=1,
                y1=0,
                line=dict(color="gray", width=1, dash="dash"),
                xref="paper",
                yref="y"
            )
            
            # Atualizar layout do gráfico
            fig.update_layout(
                title="Resultado Líquido das Empresas para o Estado Acionista por Dependência",
                xaxis_title="Estado, Ano",
                yaxis_title="Resultado Líquido para o Estado (R$)",
                barmode="stack",
                xaxis=dict(
                    categoryorder="array",
                    categoryarray=sorted(agrupado_resultado["label"].unique()),
                    tickangle=-90,
                    tickfont=dict(size=10, color="black"),
                    title=dict(font=dict(color="black", size=14)),
                ),
                yaxis=dict(
                    tickfont=dict(color="black", size=12),
                    title=dict(font=dict(color="black", size=14)),
                    gridcolor="lightgray",
                ),
                legend=dict(
                    title=dict(text="Dependência", font=dict(color="black", size=12)),
                    font=dict(color="black"),
                    orientation="h",
                    yanchor="bottom",
                    y=-0.30,  # Aumentado para mover a legenda mais para baixo
                    xanchor="center",
                    x=0.5
                ),
                showlegend=True,
                template="plotly_white",
                height=600,
                margin=dict(l=40, r=40, t=80, b=180),  # Aumentado o valor de b (margem inferior)
                plot_bgcolor="white",
                paper_bgcolor="white",
                title_font=dict(color="black", size=16)
            )
            
            # Mostrar o gráfico
            st.plotly_chart(fig, use_container_width=True)
            
            # Adicionar seção expandível com análise detalhada
            with st.expander("📊 Ver análise detalhada por dependência"):
                # Agrupar por tipo de dependência para análise global
                dep_analysis = df_resultado_dep.groupby("dep")["Resultado para o Estado Acionista"].agg(
                    ["sum", "mean", "count"]
                ).reset_index()
                dep_analysis.columns = ["Dependência", "Total", "Média", "Quantidade de Registros"]
                
                # Ordenar do mais positivo ao mais negativo
                dep_analysis = dep_analysis.sort_values(by="Total", ascending=False)
                
                # Mostrar tabela formatada
                st.dataframe(
                    dep_analysis,
                    column_config={
                        "Total": st.column_config.NumberColumn("Total (R$)", format="R$ %.2f"),
                        "Média": st.column_config.NumberColumn("Média (R$)", format="R$ %.2f")
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Comparação direta entre categorias de dependência
                st.markdown("### Comparação entre categorias de dependência")
                
                fig_comp = px.bar(
                    dep_analysis,
                    x="Dependência",
                    y="Total",
                    color="Dependência",
                    color_discrete_map={
                        "Não Dependente": "#007acc",
                        "Dependente": "#F46045",
                        "Não Informado": "rgba(150, 150, 150, 0.8)",
                    },
                    text="Total",
                    labels={"Total": "Resultado Total (R$)"},
                    height=400
                )
                
                # Configurações adicionais
                fig_comp.update_traces(
                    texttemplate="R$ %{y:,.2f}",
                    textposition="outside"
                )
                
                fig_comp.update_layout(
                    xaxis_title=dict(text="Categoria de Dependência", font=dict(color="black", size=14)),
                    yaxis_title=dict(text="Resultado Total (R$)", font=dict(color="black", size=14)),
                    xaxis=dict(tickfont=dict(color="black")),
                    yaxis=dict(tickfont=dict(color="black")),
                    showlegend=False,
                    plot_bgcolor="white",
                    paper_bgcolor="white"
                )
                
                # Adicionar linha no zero
                fig_comp.add_hline(y=0, line_dash="dash", line_color="gray")
                
                # Mostrar o gráfico de comparação
                st.plotly_chart(fig_comp, use_container_width=True)
                
                # Análise por estado e dependência
                st.markdown("### Resultado por Estado e Dependência")
                
                # Agrupar por estado e dependência
                estado_dep = df_resultado_dep.groupby(["Estado", "dep"])["Resultado para o Estado Acionista"].sum().reset_index()
                
                # Criar tabela dinâmica para visualização
                pivot_estado_dep = estado_dep.pivot_table(
                    index="Estado",
                    columns="dep",
                    values="Resultado para o Estado Acionista",
                    fill_value=0
                ).reset_index()
                
                # Adicionar coluna de total
                pivot_estado_dep["Total"] = pivot_estado_dep.iloc[:, 1:].sum(axis=1)
                
                # Ordenar por total
                pivot_estado_dep = pivot_estado_dep.sort_values("Total", ascending=False)
                
                # Formatar para exibição
                st.dataframe(
                    pivot_estado_dep,
                    column_config={
                        col: st.column_config.NumberColumn(
                            col, format="R$ %.2f"
                        ) for col in pivot_estado_dep.columns if col != "Estado"
                    },
                    hide_index=True,
                    use_container_width=True
                )

# Botão para voltar à página inicial
if st.button("Voltar à Página Inicial"):
    st.switch_page("Início.py")
