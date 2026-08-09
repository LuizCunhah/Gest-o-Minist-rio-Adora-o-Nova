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

# --- BANCOS DE DADOS PERMANENTES (JSON) ---
ARQUIVO_CONFIG = "dados_config.json"
ARQUIVO_ESCALAS = "dados_escalas.json"
ARQUIVO_REPERTORIO = "dados_repertorio.json"
ARQUIVO_LOGS = "dados_logs.json"
ARQUIVO_DANCA = "dados_danca.json"
ARQUIVO_MUSICOS = "dados_musicos.json"
ARQUIVO_PARTICIPANTES = "dados_participantes.json"

def carregar_dados_sistema():
    if "admin_username" in st.secrets and "admin_password" in st.secrets:
        st.session_state.usuarios_adm = {st.secrets["admin_username"]: st.secrets["admin_password"]}
    else:
        st.session_state.usuarios_adm = {}

    if os.path.exists(ARQUIVO_CONFIG):
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if not st.session_state.usuarios_adm:
                st.session_state.usuarios_adm = cfg.get("usuarios", {"admin": "admin123"})
            st.session_state.titulo_app = cfg.get("titulo", "Adoração Nova Niterói")
            st.session_state.sub_titulo_app = cfg.get("subtitulo", "Sistema Integrado de Gestão de Louvor, Artes e Escalas")
            st.session_state.nomes_extensoes = cfg.get("extensoes", ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"])
    else:
        if not st.session_state.usuarios_adm:
            st.session_state.usuarios_adm = {"admin": "admin123"}
        st.session_state.titulo_app = "Adoração Nova Niterói"
        st.session_state.sub_titulo_app = "Sistema Integrado de Gestão de Louvor, Artes e Escalas"
        st.session_state.nomes_extensoes = ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"]

    if os.path.exists(ARQUIVO_ESCALAS):
        with open(ARQUIVO_ESCALAS, "r", encoding="utf-8") as f:
            st.session_state.escalas = json.load(f)
    else:
        st.session_state.escalas = {ext: [] for ext in st.session_state.nomes_extensoes}

    if os.path.exists(ARQUIVO_REPERTORIO):
        with open(ARQUIVO_REPERTORIO, "r", encoding="utf-8") as f:
            st.session_state.repertorio = json.load(f)
    else:
        st.session_state.repertorio = {
            "Aclame ao Senhor": {"Artista": "Diante do Trono", "Cifra": "[A] Aclame ao Senhor [D] toda a terra..."}
        }

    if os.path.exists(ARQUIVO_DANCA):
        with open(ARQUIVO_DANCA, "r", encoding="utf-8") as f:
            st.session_state.danca = json.load(f)
    else:
        st.session_state.danca = []

    if os.path.exists(ARQUIVO_MUSICOS):
        with open(ARQUIVO_MUSICOS, "r", encoding="utf-8") as f:
            st.session_state.musicos = json.load(f)
    else:
        st.session_state.musicos = [
            {"ID": 1, "Nome": "João Silva", "Instrumento": "Guitarra", "Categoria": "Cordas"},
            {"ID": 2, "Nome": "Maria Oliveira", "Instrumento": "Teclado", "Categoria": "Teclas"}
        ]

    if os.path.exists(ARQUIVO_PARTICIPANTES):
        with open(ARQUIVO_PARTICIPANTES, "r", encoding="utf-8") as f:
            st.session_state.participantes = json.load(f)
    else:
        st.session_state.participantes = [
            {
                "ID": 1, "Nome": "João Silva", "Funcao": "Músico", "Telefone": "(21) 99999-1111", 
                "Email": "joao@email.com", "Endereco": "Rua A, 100", "Aniversario": "15/05", "Sugestoes": "Nenhuma"
            }
        ]

    if os.path.exists(ARQUIVO_LOGS):
        with open(ARQUIVO_LOGS, "r", encoding="utf-8") as f:
            st.session_state.logs_notificacoes = json.load(f)
    else:
        st.session_state.logs_notificacoes = []

def salvar_dados_sistema():
    with open(ARQUIVO_ESCALAS, "w", encoding="utf-8") as f:
        json.dump(st.session_state.escalas, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_REPERTORIO, "w", encoding="utf-8") as f:
        json.dump(st.session_state.repertorio, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_DANCA, "w", encoding="utf-8") as f:
        json.dump(st.session_state.danca, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_MUSICOS, "w", encoding="utf-8") as f:
        json.dump(st.session_state.musicos, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_PARTICIPANTES, "w", encoding="utf-8") as f:
        json.dump(st.session_state.participantes, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_LOGS, "w", encoding="utf-8") as f:
        json.dump(st.session_state.logs_notificacoes, f, ensure_ascii=False, indent=4)
    with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump({
            "usuarios": st.session_state.usuarios_adm,
            "titulo": st.session_state.titulo_app,
            "subtitulo": st.session_state.sub_titulo_app,
            "extensoes": st.session_state.nomes_extensoes
        }, f, ensure_ascii=False, indent=4)

carregar_dados_sistema()

if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_atual' not in st.session_state:
    st.session_state.usuario_atual = None

def registrar_alerta(txt):
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.session_state.logs_notificacoes.insert(0, {"data": horario, "mensagem": txt})
    salvar_dados_sistema()

# --- TELA DE PRIMEIRO ACESSO ---
if not st.session_state.usuarios_adm:
    st.markdown("<div class='bloco-admin'>", unsafe_allow_html=True)
    st.markdown("### ⚠️ Configuração Inicial do Sistema")
    st.info("Nenhuma conta de Administrador foi encontrada. Crie a senha inicial de Administrador para prosseguir:")
    with st.form("form_primeiro_admin"):
        novo_user = st.text_input("Nome do Usuário Administrador Principal", value="admin")
        nova_senha = st.text_input("Senha do Administrador", type="password")
        confirma_senha = st.text_input("Confirme a Senha", type="password")
        
        if st.form_submit_button("🚀 Criar Conta de Administrador"):
            if nova_senha and nova_senha == confirma_senha:
                st.session_state.usuarios_adm[novo_user] = nova_senha
                salvar_dados_sistema()
                st.success("Administrador criado com sucesso! Recarregando...")
                st.rerun()
            else:
                st.error("As senhas não coincidem ou estão vazias.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- EXIBIÇÃO ABSOLUTA DA IMAGEM DO BANNER ---
caminho_script_atual = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANNER = os.path.join(caminho_script_atual, "NOVA-NITEROI-Rj_4.jpg")

if os.path.exists(CAMINHO_BANNER):
    st.image(CAMINHO_BANNER, use_container_width=True)
else:
    CAMINHO_BANNER_ALT = "NOVA-NITEROI-Rj_4.jpg"
    if os.path.exists(CAMINHO_BANNER_ALT):
        st.image(CAMINHO_BANNER_ALT, use_container_width=True)
    else:
