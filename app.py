import streamlit as st
import xml.etree.ElementTree as ET

st.set_page_config(page_title="Leitor Universal de XML", page_icon="🔎", layout="wide")
st.title("Raio-X de XML (Diagnóstico de Fornecedores) 🔎")
st.write("Faça o upload do XML de um novo fornecedor. O sistema vai varrer o arquivo e extrair o código puro do primeiro produto para você copiar e enviar para análise.")

uploaded_file = st.file_uploader("Arraste e solte o XML aqui", type=["xml"])

if uploaded_file is not None:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        
        produtos = root.findall('.//nfe:det', ns)
        
        if not produtos:
            st.error("❌ Nenhum produto encontrado neste XML.")
        else:
            st.success(f"✅ Encontrei {len(produtos)} produtos! Aqui está o Raio-X do primeiro item:")
            
            # Pega apenas o primeiro produto da nota
            det = produtos[0]
            
            st.subheader("Código Cru do Produto (Copie o quadro abaixo)")
            
            # Transforma o elemento de volta em texto puro (código XML)
            xml_cru = ET.tostring(det, encoding='unicode')
            
            # Exibe na tela com um botão de cópia automático no canto superior direito
            st.code(xml_cru, language='xml')
            
            st.info("👆 Passe o mouse no canto superior direito do quadro preto acima e clique no ícone de copiar. Cole o resultado para a inteligência artificial analisar onde estão escondidas a cor e o tamanho.")

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
