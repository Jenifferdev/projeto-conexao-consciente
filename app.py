import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
import os

ARQUIVO_DADOS = "/dados_conexao_consciente.csv"

if not os.path.exists(ARQUIVO_DADOS):
    df_inicial = pd.DataFrame(columns=["Idade", "Tempo_Tela", "Principal_Uso", "Dificuldade_Concentracao"])
    df_inicial.to_csv(ARQUIVO_DADOS, index=False)

st.set_page_config(page_title="Projeto Conexão Consciente", layout="wide")
st.title("📱 Projeto Conexão Consciente")
st.subheader("Análise de Informação e Estatística do Tempo de Tela na Comunidade")

col_form, col_dash = st.columns([1, 2])

with col_form:
    st.markdown("### 📝 Participe da Pesquisa")
    with st.form("formulario_jovem"):
        idade = st.number_input("Sua Idade:", min_value=12, max_value=29, value=18)
        tempo = st.slider("Quantas horas você passa no celular por dia?", 0, 16, 5)
        uso = st.selectbox("Qual aplicativo consome mais o seu tempo?", ["Redes Sociais", "Jogos", "Estudos", "Vídeos/Streaming"])
        concentracao = st.radio("Sente dificuldade de concentração nas tarefas diárias?", ["Sim", "Não"])
        enviado = st.form_submit_button("Enviar e Atualizar Painel")
        
    if enviado:
        novo_dado = pd.DataFrame([[idade, tempo, uso, concentracao]], columns=["Idade", "Tempo_Tela", "Principal_Uso", "Dificuldade_Concentracao"])
        novo_dado.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False)
        st.success("Dados computados com sucesso!")

with col_dash:
    df = pd.read_csv(ARQUIVO_DADOS)
    if len(df) < 5:
        st.warning(f"📥 Aguardando respostas dos jovens... ({len(df)}/5 computadas para liberar as estatísticas).")
    else:
        st.markdown("### 📊 Painel Estatístico em Tempo Real")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Jovens (N)", f"{len(df)}")
        m2.metric("Média de Tempo", f"{df['Tempo_Tela'].mean():.1f}h/dia")
        m3.metric("Desvio Padrão (σ)", f"{df['Tempo_Tela'].std():.2f}h")
        
        fig_hist = px.histogram(df, x="Tempo_Tela", nbins=10, title="Distribuição do Tempo de Tela")
        st.plotly_chart(fig_hist, use_container_width=True)
