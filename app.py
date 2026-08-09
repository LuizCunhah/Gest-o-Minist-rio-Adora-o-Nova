import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# ATENÇÃO: É necessário instalar a biblioteca gspread. 
# Adicione 'gspread' e 'gspread-streamlit' no seu arquivo requirements.txt
import gspread
from google.oauth2.service_account import Credentials

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
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{ color: #f8fafc !important; }}
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label, .stMultiSelect label {{ color: #bbf7d0 !important; font-weight: 600 !important; }}
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{ background-color: rgba(255, 255, 255, 0.90) !important; color: #0f172a !important; border: 1px solid #4ade80 !important; border-radius: 6px !important; }}
    .titulo-principal {{ font-size: 38px !important; font-weight: bold !important; color: #fef08a !important; text-align: center; margin-top: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.8); }}
    .sub-titulo {{ font-size: 18px !important; color: #bbf7d0 !important; text-align: center; margin-bottom: 20px; font-weight: 500; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); }}
    div.stButton > button:first-child {{ background-color: #16a34a !important; color: white !important; font-weight: bold; border-radius: 8px; }}
    .bloco-admin {{ background-color: rgba(15, 23, 42, 0.85); padding: 20px; border-radius: 12px; border: 2px solid #22c55e; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3); }}
    .bloco-versiculo {{ background: linear-gradient(135deg, rgba(20, 83, 45, 0.9) 0%, rgba(120, 53, 15, 0.9) 100%); color: white !important; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border: 1px solid #eab308; }}
    .bloco-versiculo *, .bloco-versiculo p, .bloco-versiculo h3 {{ color: white !important; }}
    .alerta-item {{ background-color: rgba(15, 23, 42, 0.85); padding: 12px 16px; border-radius: 8px; border-left: 5px solid #22c55e; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
    .botao-refresh-container {{ position: fixed; bottom: 20px; left: 20px; z-index: 99999; }}
"""
st.markdown(f"<style>{css_fundo}</style>", unsafe_allow_html=True)

# --- CONEXÃO COM GOOGLE SHEETS ---
def conectar_google_sheets():
    # Definição dos escopos necessários para acessar o Google Drive e Planilhas
    escopos = ["https://googleapis.com", "https://googleapis.com"]
    
    # Carrega as credenciais seguras do painel do Streamlit Community Cloud (st.secrets)
    info_credenciais = {
        "type": st.secrets["gcp_service_account"]["type"],
        "project_id": st.secrets["gcp_service_account"]["project_id"],
        "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
        "private_key": st.secrets["gcp_service_account"]["private_key"],
        "client_email": st.secrets["gcp_service_account"]["client_email"],
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
    }
    
    creds = Credentials.from_service_account_info(info_credenciais, scopes=escopos)
    cliente = gspread.authorize(creds)
    
    # Abre a planilha pelo ID seguro configurado nos segredos do Streamlit
    return cliente.open_by_key(st.secrets["google_sheet_id"])

# --- INICIALIZAÇÃO DE DADOS ---
try:
    planilha_mestre = conectar_google_sheets()
    st.session_state.conexao_nuvem_ativa = True
except Exception as e:
    st.session_state.conexao_nuvem_ativa = False
    st.error(f"Erro ao conectar ao banco de dados em nuvem: {e}")

# Lógica de controle de usuários administradores
st.session_state.usuarios_adm = {}
if "admin_username" in st.secrets and "admin_password" in st.secrets:
    st.session_state.usuarios_adm[st.secrets["admin_username"]] = st.secrets["admin_password"]
else:
    st.session_state.usuarios_adm = {"admin": "admin123"}

if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'usuario_atual' not in st.session_state:
    st.session_state.usuario_atual = None

# --- CARREGAMENTO REATIVO DAS ABAS DO GOOGLE SHEETS ---
if st.session_state.conexao_nuvem_ativa:
    # Busca em tempo real os registros da planilha do Google para evitar perda de dados
    st.session_state.participantes = planilha_mestre.worksheet("Participantes").get_all_records()
    st.session_state.musicos = planilha_mestre.worksheet("Musicos").get_all_records()
    st.session_state.danca = planilha_mestre.worksheet("Danca").get_all_records()
    st.session_state.logs_notificacoes = planilha_mestre.worksheet("Logs").get_all_records()
    
    # Tratamento específico para o dicionário estruturado de Repertório
    dados_brutos_repertorio = planilha_mestre.worksheet("Repertorio").get_all_records()
    st.session_state.repertorio = {row["Musica"]: {"Artista": row["Artista"], "Cifra": row["Cifra"]} for row in dados_brutos_repertorio}
    
    # Tratamento específico para as Escalas por extensão
    st.session_state.nomes_extensoes = ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"]
    dados_brutos_escalas = planilha_mestre.worksheet("Escalas").get_all_records()
    st.session_state.escalas = {ext: [] for ext in st.session_state.nomes_extensoes}
    for row in dados_brutos_escalas:
        if row["Extensão"] in st.session_state.escalas:
            st.session_state.escalas[row["Extensão"]].append({
                "ID": row["ID"], "Data": row["Data"], "Horário": row["Horário"], "Vocal": row["Vocal"], "Músicos": row["Músicos"]
            })
    st.session_state.titulo_app = "Adoração Nova Niterói"
    st.session_state.sub_titulo_app = "Sistema Integrado de Gestão de Louvor, Artes e Escalas"
else:
    # Fallback de segurança local para caso de falha de internet
    st.session_state.participantes = [{"ID": 1, "Nome": "João Silva", "Funcao": "Músico", "Telefone": "(21) 99999-1111", "Email": "joao@email.com", "Endereco": "Rua A, 100", "Aniversario": "15/05", "Sugestoes": "Nenhuma"}]
    st.session_state.musicos = [{"ID": 1, "Nome": "João Silva", "Instrumento": "Guitarra", "Categoria": "Cordas"}]
    st.session_state.danca = []
    st.session_state.repertorio = {"Aclame ao Senhor": {"Artista": "Diante do Trono", "Cifra": "[A] Aclame ao Senhor [D] toda a terra..."}}
    st.session_state.nomes_extensoes = ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"]
    st.session_state.escalas = {ext: [] for ext in st.session_state.nomes_extensoes}
    st.session_state.logs_notificacoes = []
    st.session_state.titulo_app = "Adoração Nova Niterói"
    st.session_state.sub_titulo_app = "Sistema Integrado de Gestão de Louvor, Artes e Escalas"

# --- REESCRITA DAS FUNÇÕES DE SALVAMENTO PARA ESCREVER NA NUVEM ---
def salvar_participante_nuvem(novo_registro):
    if st.session_state.conexao_nuvem_ativa:
        aba = planilha_mestre.worksheet("Participantes")
        aba.append_row(list(novo_registro.values()))

def salvar_escala_nuvem(extensao, nova_entrada):
    if st.session_state.conexao_nuvem_ativa:
        aba = planilha_mestre.worksheet("Escalas")
        linha = [nova_entrada["ID"], extensao, nova_entrada["Data"], nova_entrada["Horário"], nova_entrada["Vocal"], nova_entrada["Músicos"]]
        aba.append_row(linha)

def salvar_musico_nuvem(novo_m):
    if st.session_state.conexao_nuvem_ativa:
        aba = planilha_mestre.worksheet("Musicos")
        aba.append_row(list(novo_m.values()))

def salvar_musica_nuvem(nome_m, dados_m):
    if st.session_state.conexao_nuvem_ativa:
        aba = planilha_mestre.worksheet("Repertorio")
        aba.append_row([nome_m, dados_m["Artista"], dados_m["Cifra"]])

def salvar_danca_nuvem(novo_d):
    if st.session_state.conexao_nuvem_ativa:
        aba = planilha_mestre.worksheet("Danca")
        aba.append_row(list(novo_d.values()))

def registrar_alerta(txt):
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if st.session_state.conexao_nuvem_ativa:
        aba = planilha_mestre.worksheet("Logs")
        aba.append_row([horario, txt])

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
