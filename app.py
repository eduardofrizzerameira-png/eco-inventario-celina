import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página do app
st.set_page_config(page_title="Eco-Inventário Celina", page_icon="🌿")

st.title("🌿 Eco-Inventário Domiciliar de Fármacos")
st.subheader("Ciência Cidadã - EEEFM Sirena Rezende Fonseca")

st.write("Utilize este formulário anônimo para cadastrar os medicamentos encontrados na sua farmácia caseira.")

# Formulário para o usuário preencher pelo celular
with st.form("form_medicamento"):
    st.text("📋 Dados do Medicamento")
    
    principio_ativo = st.text_input("Nome do Princípio Ativo (ex: Paracetamol, Losartana):")
    
    status_validade = st.selectbox(
        "O medicamento está dentro da validade?",
        ["No prazo de validade", "Vencido", "Não sei / Apagado"]
    )
    
    destino_comum = st.selectbox(
        "Como sua família costuma descartar o que não usa?",
        ["Lixo comum", "Vaso sanitário / Pia", "Posto de Saúde / Farmácia", "Guarda em casa indefinidamente"]
    )
    
    foto_caixa = st.file_uploader("Envie uma foto da embalagem (Opcional):", type=["jpg", "png", "jpeg"])
    
    turma = st.selectbox("Qual a sua turma na escola Sirena?", ["1º Ano", "2º Ano", "3º Ano", "Professor / Funcionário"])

    # Botão de envio
    enviar = st.form_submit_button("Enviar Inventário")

if enviar:
    if principio_ativo:
        # Simula o salvamento dos dados
        novo_registro = {
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Turma": turma,
            "Princípio Ativo": principio_ativo.capitalize(),
            "Validade": status_validade,
            "Descarte Comum": destino_comum
        }
        
        # Salvando em um arquivo CSV local para teste
        try:
            df_existente = pd.read_csv("banco_dados_ficticio.csv")
            df_novo = pd.concat([df_existente, pd.DataFrame([novo_registro])], ignore_index=True)
        except FileNotFoundError:
            df_novo = pd.DataFrame([novo_registro])
            
        df_novo.to_csv("banco_dados_ficticio.csv", index=False)
        
        st.success("Obrigado! Seu dado foi contabilizado com sucesso para a gincana científica da escola!")
        st.balloons()
    else:
        st.error("Por favor, preencha pelo menos o nome do princípio ativo.")

# Seção restrita para os Bolsistas ICJr verem o Dashboard (Painel)
st.markdown("---")
if st.checkbox("🔓 Acesso Restrito: Painel dos Bolsistas (Dashboard)"):
    st.subheader("📊 Painel de Controle da Gincana")
    try:
        df_dados = pd.read_csv("banco_dados_ficticio.csv")
        st.metric(label="Total de Embalagens Mapeadas", value=len(df_dados))
        
        st.write("Registros recebidos em tempo real:")
        st.dataframe(df_dados)
        
        # Gráfico simples de princípios ativos mais comuns
        if not df_dados.empty:
            st.write("Fármacos mais cadastrados:")
            conTAGem = df_dados["Princípio Ativo"].value_counts()
            st.bar_chart(conTAGem)
            
    except FileNotFoundError:
        st.info("Ainda não há dados cadastrados no sistema.")