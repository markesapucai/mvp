import streamlit as st
import openai
import pandas as pd
from docx import Document
import os
from dotenv import load_dotenv

# Configurações
load_dotenv()  # Carrega variáveis do .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Título da aplicação
st.title("📝 Gerador de Relatórios Ambientais")
st.markdown("Transforme planilhas em relatórios técnicos prontos para EIA-RIMA!")

# Upload da planilha
uploaded_file = st.file_uploader("**Envie sua planilha** (Excel ou CSV)", type=["xlsx", "csv"])

# Inputs do usuário
report_type = st.selectbox(
    "**Tipo de relatório**",
    ("Impactos Hidrológicos", "Qualidade do Ar", "Gestão de Resíduos")
)

# Processamento
if uploaded_file and st.button("Gerar Relatório"):
    with st.spinner("Processando..."):
        try:
            # 1. Lê os dados
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
            
            # 2. Gera texto com IA
            prompt = f"""
            Gere um relatório de {report_type} para engenharia ambiental com os dados abaixo.
            Use linguagem técnica e cite normas como CONAMA 357/05 quando relevante.
            Dados:
            {df.to_string()}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            report_text = response.choices[0].message.content
            
            # 3. Cria um documento Word (opcional)
            doc = Document()
            doc.add_heading(f"Relatório de {report_type}", level=1)
            doc.add_paragraph(report_text)
            doc.save("relatorio.docx")
            
            # 4. Exibe e disponibiliza para download
            st.success("Relatório gerado com sucesso!")
            st.download_button(
                label="⬇️ Baixar Relatório (.docx)",
                data=open("relatorio.docx", "rb").read(),
                file_name=f"relatorio_{report_type}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
            # Preview do texto
            st.expander("Visualizar texto gerado").write(report_text)
            
        except Exception as e:
            st.error(f"Erro: {str(e)}")