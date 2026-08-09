import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import base64

# Configuração da Página Web
st.set_page_config(
    page_title="Gestão de Louvor Matriz",
    page_icon="🎵",
    layout="wide"
)

# --- CONVERSÃO DA FOTO DE FUNDO ---
CAMINHO_FUNDO_FOTO = "matt-richmond-8fhGzN5ktJo-unsplash_2.jpg"
if os.path.exists(CAMINHO_FUNDO_FOTO):
    with open(CAMINHO_FUNDO_FOTO, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")
else:
    img_base64 = ""

# --- ESTILOS CSS ---
css_fundo = f"""
    .stApp {{
        background: linear-gradient(rgba(20, 40, 25, 0.75), rgba(40, 25, 15, 0.75)), url("data:image/jpeg;base64,{img_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        color: #f8fafc !important;
    }}
    
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
        color: #f8fafc !important;
    }}
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label, .stMultiSelect label {{
        color: #bbf7d0 !important;
        font-weight: 600 !important;
    }}
    
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background-color: rgba(255, 255, 255, 0.90) !important;
        color: #0f172a !important;
        border: 1px solid #4ade80 !important;
        border-radius: 6px !important;
    }}
    
    .titulo-principal {{
        font-size: 38px !important;
        font-weight: bold !important;
        color: #fef08a !important;
        text-align: center;
        margin-top: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}
    .sub-titulo {{
        font-size: 18px !important;
        color: #bbf7d0 !important;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }}
    div.stButton > button:first-child {{
        background-color: #16a34a !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }}
    .bloco-admin {{
        background-color: rgba(15, 23, 42, 0.85);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #22c55e;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }}
    .bloco-versiculo {{
        background: linear-gradient(135deg, rgba(20, 83, 45, 0.9) 0%, rgba(120, 53, 15, 0.9) 100%);
        color: white !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #eab308;
    }}
    .bloco-versiculo *, .bloco-versiculo p, .bloco-versiculo h3 {{
        color: white !important;
    }}
    .alerta-item {{
        background-color: rgba(15, 23, 42, 0.85);
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 5px solid #22c55e;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    .botao-refresh-container {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 99999;
    }}
"""

st.markdown(f"<style>{css_fundo}</style>", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE VARIÁVEIS NA MEMÓRIA ---
if 'usuarios_adm' not in st.session_state:
    if "admin_username" in st.secrets and "admin_password" in st.secrets:
        st.session_state.usuarios_adm = {st.secrets["admin_username"]: st.secrets["admin_password"]}
    else:
        st.session_state.usuarios_adm = {"admin": "admin123"}

if 'titulo_app' not in st.session_state:
    st.session_state.titulo_app = "Adoração Nova Niterói"
if 'sub_titulo_app' not in st.session_state:
    st.session_state.sub_titulo_app = "Sistema Integrado de Gestão de Louvor, Artes e Escalas"
if 'nomes_extensoes' not in st.session_state:
    st.session_state.nomes_extensoes = ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"]

if 'escalas' not in st.session_state:
    st.session_state.escalas = {ext: [] for ext in st.session_state.nomes_extensoes}
if 'repertorio' not in st.session_state:
    st.session_state.repertorio = {
        "Aclame ao Senhor": {"Artista": "Diante do Trono", "Cifra": "[A] Aclame ao Senhor [D] toda a terra..."}
    }
if 'danca' not in st.session_state:
    st.session_state.danca = []
if 'musicos' not in st.session_state:
    st.session_state.musicos = [
        {"ID": 1, "Nome": "João Silva", "Instrumento": "Guitarra", "Categoria": "Cordas"},
        {"ID": 2, "Nome": "Maria Oliveira", "Instrumento": "Teclado", "Categoria": "Teclas"}
    ]
if 'participantes' not in st.session_state:
    st.session_state.participantes = [
        {
            "ID": 1, "Nome": "João Silva", "Funcao": "Músico", "Telefone": "(21) 99999-1111", 
            "Email": "joao@email.com", "Endereco": "Rua A, 100", "Aniversario": "15/05", "Sugestoes": "Nenhuma"
        }
    ]
if 'logs_notificacoes' not in st.session_state:
    st.session_state.logs_notificacoes = []
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_atual' not in st.session_state:
    st.session_state.usuario_atual = None

def registrar_alerta(txt):
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.session_state.logs_notificacoes.insert(0, {"data": horario, "mensagem": txt})

# --- EXIBIÇÃO ABSOLUTA DA IMAGEM DO BANNER ---
caminho_script_atual = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANNER = os.path.join(caminho_script_atual, "NOVA-NITEROI-Rj_4.jpg")

if os.path.exists(CAMINHO_BANNER):
    st.image(CAMINHO_BANNER, use_container_width=True)
else:
    CAMINHO_BANNER_ALT = "NOVA-NITEROI-Rj_4.jpg"
    if os.path.exists(CAMINHO_BANNER_ALT):
        st.image(CAMINHO_BANNER_ALT, use_container_width=True)

st.markdown(f"<div class='titulo-principal'>{st.session_state.titulo_app}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-titulo'>{st.session_state.sub_titulo_app}</div>", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN PÚBLICO / ADM ---
st.markdown("<div class='bloco-admin'>", unsafe_allow_html=True)
if not st.session_state.logado:
    st.markdown("### 🔒 Acesso Público (Visualização Livre) / Painel Administrativo")
    st.info("💡 Todos podem navegar livremente pelo aplicativo. Insira as credenciais abaixo apenas se precisar alterar dados na aba principal restrita:")
    
    col_login_user, col_login_pass, col_login_btn = st.columns(3)
    with col_login_user:
        login_u = st.text_input("Usuário ADM", key="login_usuario_interface")
    with col_login_pass:
        login_p = st.text_input("Senha do ADM", type="password", key="login_senha_interface")
    with col_login_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔓 Entrar como ADM", use_container_width=True):
            if login_u in st.session_state.usuarios_adm and st.session_state.usuarios_adm[login_u] == login_p:
                st.session_state.logado = True
                st.session_state.usuario_atual = login_u
                st.success(f"Acesso ADM concedido! Bem-vindo {login_u}.")
                st.rerun()
            else:
                st.error("Credenciais incorretas.")
else:
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        st.markdown(f"🟢 **Modo Administrador Ativo (Logado como: {st.session_state.usuario_atual})**. Gestão total liberada na aba principal.")
    with col_inf2:
        if st.button("🚪 Sair do Modo ADM", use_container_width=True):
            st.session_state.logado = False
            st.session_state.usuario_atual = None
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- BOTÃO DE REFRESH ---
st.markdown("<div class='botao-refresh-container'>", unsafe_allow_html=True)
if st.button("🔄 Atualizar Tela"):
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- NAVEGAÇÃO POR ABAS ---
if st.session_state.logado:
    aba_adm_principal, aba_escalas, aba_musicos, aba_repertorio, aba_danca, aba_devocional = st.tabs([
        "👑 Gestão Geral (Admin)", "📊 Escalas Sincronizadas", "🎸 Gestão de Músicos", "🎶 Repertório & Cifras", "🩰 Ministério de Dança", "📖 Devocional & Bíblia"
    ])
else:
    aba_escalas, aba_musicos, aba_repertorio, aba_danca, aba_devocional = st.tabs([
        "📊 Escalas Sincronizadas", "🎸 Gestão de Músicos", "🎶 Repertório & Cifras", "🩰 Ministério de Dança", "📖 Devocional & Bíblia"
    ])

# ==============================================================================
# 0. ABA PRINCIPAL RESTRITA AO ADMINISTRADOR
# ==============================================================================
if st.session_state.logado:
    with aba_adm_principal:
        st.subheader("👑 Área Restrita do Administrador — Gestão Geral do Aplicativo")
        st.info("Gerencie aqui todos os participantes do ministério e configure as informações gerais de título e extensões.")

        st.markdown("---")
        st.markdown("### 📋 Cadastro de Novo Participante")
        with st.form("form_novo_participante_geral"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p_nome = st.text_input("Nome Completo")
                p_funcao = st.selectbox("Função Principal", ["Músico", "Dança", "Vocal", "Apoio / Técnica", "Outros"])
                p_tel = st.text_input("Telefone / WhatsApp")
                p_email = st.text_input("E-mail")
            with col_p2:
                p_end = st.text_input("Endereço")
                p_aniv = st.text_input("Data de Aniversário (ex: DD/MM)")
                p_sug = st.text_area("Sugestões / Observações")

            if st.form_submit_button("➕ Cadastrar Participante"):
                if p_nome:
                    novo_id_p = max([p["ID"] for p in st.session_state.participantes], default=0) + 1
                    novo_registro = {
                        "ID": novo_id_p,
                        "Nome": p_nome,
