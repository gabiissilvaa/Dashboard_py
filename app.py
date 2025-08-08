#Importações
import streamlit as st
import pandas as pd
import plotly.express as px

#------------Configuração da página------------
#Define o título da página e o layout para ocupar a largura inteira
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon=":bar_chart:",
    layout="wide", #Para deixar a página com largura total
)

#------------Carregamento dos dados------------
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

#------------Barra lateral (Filtros)------------
st.sidebar.header("Filtros")

#Filtro por ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

#Filtro de senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

#Filtro por tipo de contrato
contrato_disponiveis = sorted(df['contrato'].unique())
contrato_selecionados = st.sidebar.multiselect("Tipo de Contrato", contrato_disponiveis, default=contrato_disponiveis)

#Filtro por tamanho da empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

#------------Filtragem do DataFrame------------
#O DataFrame principal é filtrado com base nas seleções feitas na barra lateral
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contrato_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

#------------Conteúdo Principal------------
st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Análise de salários com base em diferentes filtros como ano, senioridade, tipo de contrato e tamanho da empresa.")

#------------Métricas Principáis (KPIs)------------
st.subheader("Métricas gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio, salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4) #Divide a tela em 4 colunas iguais, permitindo exibir informações lado a lado
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", f"{total_registros:,}")
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---") #Adiciona uma linha horizontal para separar visualmente essa seção das próximas

#------------Análises Visuais com Plotly------------
st.subheader("Gráficos de Análise")

col_graf1, col_graf2 = st.columns(2) #Divide a tela em 2 colunas para os gráficos

with col_graf1:
    if not df_filtrado.empty:
        #Agrupa os dados filtrados pelo nome do cargo, calcula a média salarial de cada cargo e reseta o índice para facilitar a plotagem
        #Seleciona os 10 cargos com maior média salarial= (nlargest(10)
        #Ordena esses cargos do menor para o maior salário médio= (sort_values(ascending=True))
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por Salário Médio",
            labels={'usd': 'Média Salarial Anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'}) #Ajusta o layout do gráfico, centralizando o título e ordenando o eixo Y
        st.plotly_chart(grafico_cargos, use_container_width=True) #Exibe o gráfico na coluna, ocupando toda a largura disponível
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30, #nbins=30 = Define o número de barras (bins) do histograma
            title="Distribuição de Salários Anuais",
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True) 
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de distribuição de salários.")

col_graf3, col_graf4 = st.columns(2) #Divide a tela em 2 colunas para os gráficos

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade'] # Cria um DataFrame com duas colunas: 'tipo_trabalho' e 'quantidade' 
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title="Distribuição de Trabalho Remoto",
            hole=0.5 # hole=0.5 = Deixa o gráfico em formato de "rosquinha" 
        )
        grafico_remoto.update_traces(textinfo='percent+label') # Mostra o percentual e o nome do tipo em cada fatia do gráfico
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de trabalho remoto.")