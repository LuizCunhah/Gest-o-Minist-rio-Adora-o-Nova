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

# --- BANNER DA SEGUNDA FOTO ---
CAMINHO_BANNER = "NOVA-NITEROI-Rj_2.jpg"

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
    if os.path.exists(ARQUIVO_CONFIG):
        with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            st.session_state.usuarios_adm = cfg.get("usuarios", {})
            st.session_state.titulo_app = cfg.get("titulo", "Adoração Nova Niterói")
            st.session_state.sub_titulo_app = cfg.get("subtitulo", "Sistema Integrado de Gestão de Louvor, Artes e Escalas")
            st.session_state.nomes_extensoes = cfg.get("extensoes", ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"])
            st.session_state.banner_path = cfg.get("banner", "")
    else:
        st.session_state.usuarios_adm = {}
        st.session_state.titulo_app = "Adoração Nova Niterói"
        st.session_state.sub_titulo_app = "Sistema Integrado de Gestão de Louvor, Artes e Escalas"
        st.session_state.nomes_extensoes = ["Sede Piratininga", "Extensão São Gonçalo", "Extensão Maricá"]
        st.session_state.banner_path = ""

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
            "extensoes": st.session_state.nomes_extensoes,
            "banner": st.session_state.banner_path
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

# --- TELA DE PRIMEIRO ACESSO (CADASTRO DA SENHA DO ADMINISTRADOR) ---
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

# --- EXIBIÇÃO DO TÍTULO E BANNER NO TOPO ---
st.markdown(f"<div class='titulo-principal'>{st.session_state.titulo_app}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='sub-titulo'>{st.session_state.sub_titulo_app}</div>", unsafe_allow_html=True)

if os.path.exists(CAMINHO_BANNER):
    st.image(CAMINHO_BANNER, use_container_width=True)

# --- SISTEMA DE LOGIN PÚBLICO / ADM ---
st.markdown("<div class='bloco-admin'>", unsafe_allow_html=True)
if not st.session_state.logado:
    st.markdown("### 🔒 Acesso Público (Visualização Livre) / Painel Administrativo")
    st.info("💡 Todos podem navegar livremente pelo aplicativo. Insira as credenciais abaixo apenas se precisar alterar dados na aba principal restrita:")
    c_user, c_pass, c_bt = st.columns([3, 3, 2])
    with c_user:
        login_u = st.text_input("Usuário ADM", key="login_usuario_interface")
    with c_pass:
        login_p = st.text_input("Senha do ADM", type="password", key="login_senha_interface")
    with c_bt:
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
    col_inf1, col_inf2 = st.columns([6, 2])
    with col_inf1:
        st.markdown(f"🟢 **Modo Administrador Ativo (Logado como: {st.session_state.usuario_atual})**. Gestão total liberada na aba principal.")
    with col_inf2:
        if st.button("🚪 Sair do Modo ADM", use_container_width=True):
            st.session_state.logado = False
            st.session_state.usuario_atual = None
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- BOTÃO DE REFRESH NA PARTE INFERIOR ESQUERDA ---
st.markdown("""
    <div class="botao-refresh-container">
""", unsafe_allow_html=True)
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

# 0. ABA PRINCIPAL RESTRITA AO ADMINISTRADOR
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
                        "ID": novo_id_p, "Nome": p_nome, "Funcao": p_funcao, "Telefone": p_tel,
                        "Email": p_email, "Endereco": p_end, "Aniversario": p_aniv, "Sugestoes": p_sug
                    }
                    st.session_state.participantes.append(novo_registro)
                    
                    if p_funcao in ["Músico", "Vocal"]:
                        novo_id_m = max([m["ID"] for m in st.session_state.musicos], default=0) + 1
                        st.session_state.musicos.append({
                            "ID": novo_id_m, "Nome": p_nome, "Instrumento": "Violão", "Categoria": "Cordas"
                        })

                    salvar_dados_sistema()
                    registrar_alerta(f"Participante cadastrado: {p_nome} ({p_funcao}).")
                    st.success("Participante cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("O nome do participante é obrigatório.")

        st.markdown("---")
        st.markdown("### 🛠️ Editar ou Excluir Participantes Cadastrados")
        if st.session_state.participantes:
            opcoes_part = {f"ID {p['ID']} - {p['Nome']} ({p['Funcao']})": p for p in st.session_state.participantes}
            escolha_part_str = st.selectbox("Selecione o Participante", list(opcoes_part.keys()))
            part_selecionado = opcoes_part[escolha_part_str]

            with st.form("form_editar_excluir_participante"):
                ep_nome = st.text_input("Nome Completo", value=part_selecionado["Nome"])
                ep_funcao = st.selectbox("Função Principal", ["Músico", "Dança", "Vocal", "Apoio / Técnica", "Outros"], index=["Músico", "Dança", "Vocal", "Apoio / Técnica", "Outros"].index(part_selecionado["Funcao"]) if part_selecionado["Funcao"] in ["Músico", "Dança", "Vocal", "Apoio / Técnica", "Outros"] else 0)
                ep_tel = st.text_input("Telefone / WhatsApp", value=part_selecionado["Telefone"])
                ep_email = st.text_input("E-mail", value=part_selecionado["Email"])
                ep_end = st.text_input("Endereço", value=part_selecionado["Endereco"])
                ep_aniv = st.text_input("Data de Aniversário (ex: DD/MM)", value=part_selecionado["Aniversario"])
                ep_sug = st.text_area("Sugestões / Observações", value=part_selecionado["Sugestoes"])

                col_eb1, col_eb2 = st.columns(2)
                with col_eb1:
                    btn_salvar_part = st.form_submit_button("💾 Salvar Alterações do Participante")
                with col_eb2:
                    btn_excluir_part = st.form_submit_button("🗑️ Excluir Participante")

                if btn_salvar_part:
                    for p in st.session_state.participantes:
                        if p["ID"] == part_selecionado["ID"]:
                            p["Nome"] = ep_nome
                            p["Funcao"] = ep_funcao
                            p["Telefone"] = ep_tel
                            p["Email"] = ep_email
                            p["Endereco"] = ep_end
                            p["Aniversario"] = ep_aniv
                            p["Sugestoes"] = ep_sug
                            break
                    salvar_dados_sistema()
                    registrar_alerta(f"Participante atualizado: {ep_nome}.")
                    st.success("Participante atualizado com sucesso!")
                    st.rerun()

                if btn_excluir_part:
                    st.session_state.participantes = [p for p in st.session_state.participantes if p["ID"] != part_selecionado["ID"]]
                    salvar_dados_sistema()
                    registrar_alerta(f"Participante removido: {part_selecionado['Nome']}.")
                    st.success("Participante excluído com sucesso!")
                    st.rerun()

            st.markdown("#### 📊 Tabela Geral de Participantes")
            st.dataframe(pd.DataFrame(st.session_state.participantes), use_container_width=True)

        st.markdown("---")
        st.markdown("### ⚙️ Configurações Gerais do Aplicativo")
        with st.form("form_config_geral_app"):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                edt_titulo = st.text_input("Título do Aplicativo", value=st.session_state.titulo_app)
            with col_t2:
                edt_sub = st.text_input("Subtítulo do Aplicativo", value=st.session_state.sub_titulo_app)

            st.markdown("**Nomes das 3 Extensões Cadastradas:**")
            col_ex0, col_ex1, col_ex2 = st.columns(3)
            with col_ex0:
                nome_ext0 = st.text_input("Extensão 1", value=st.session_state.nomes_extensoes[0])
            with col_ex1:
                nome_ext1 = st.text_input("Extensão 2", value=st.session_state.nomes_extensoes[1])
            with col_ex2:
                nome_ext2 = st.text_input("Extensão 3", value=st.session_state.nomes_extensoes[2])

            if st.form_submit_button("💾 Salvar Configurações Globais"):
                novos_nomes_lista = [nome_ext0, nome_ext1, nome_ext2]
                antigos_nomes_lista = st.session_state.nomes_extensoes

                nova_estrutura = {}
                for index, n_novo in enumerate(novos_nomes_lista):
                    n_antigo = antigos_nomes_lista[index] if index < len(antigos_nomes_lista) else n_novo
                    nova_estrutura[n_novo] = st.session_state.escalas.get(n_antigo, [])

                st.session_state.escalas = nova_estrutura
                st.session_state.titulo_app = edt_titulo
                st.session_state.sub_titulo_app = edt_sub
                st.session_state.nomes_extensoes = novos_nomes_lista

                salvar_dados_sistema()
                st.success("Configurações atualizadas com sucesso!")
                st.rerun()

# 1. ABA DE ESCALAS
with aba_escalas:
    sub_abas_locais = st.tabs([f"📍 {nome}" for nome in st.session_state.nomes_extensoes])
    nomes_disponiveis_cadastrados = [p["Nome"] for p in st.session_state.participantes] if st.session_state.participantes else ["João Silva", "Maria Oliveira"]

    for i, nome_da_extensao in enumerate(st.session_state.nomes_extensoes):
        with sub_abas_locais[i]:
            st.subheader(f"Quadro de Horários — {nome_da_extensao}")

            if nome_da_extensao not in st.session_state.escalas:
                st.session_state.escalas[nome_da_extensao] = []

            lista_atual = st.session_state.escalas[nome_da_extensao]

            if lista_atual:
                df_escala = pd.DataFrame(lista_atual)
                st.dataframe(df_escala, use_container_width=True)
            else:
                st.info("Nenhuma escala cadastrada para esta extensão no momento.")

            if st.session_state.logado:
                st.markdown("---")
                st.markdown(f"🛠️ **Gerenciar Escala: {nome_da_extensao}**")
                
                with st.form(key=f"form_escala_{i}"):
                    c_data, c_vocal, c_musicos = st.columns(3)
                    with c_data:
                        inp_data = st.date_input("Data do Culto", key=f"data_{i}")
                    with c_vocal:
                        inp_vocal = st.selectbox("Selecione o Vocal / Líder", [""] + nomes_disponiveis_cadastrados, key=f"vocal_{i}")
                    with c_musicos:
                        inp_musicos = st.selectbox("Selecione o Músico", [""] + nomes_disponiveis_cadastrados, key=f"musicos_{i}")

                    btn_adicionar = st.form_submit_button("➕ Adicionar Nova Escala")
                    if btn_adicionar:
                        nova_entrada = {
                            "ID": len(lista_atual) + 1,
                            "Data": inp_data.strftime("%d/%m/%Y"),
                            "Vocal": inp_vocal,
                            "Músicos": inp_musicos
                        }
                        lista_atual.append(nova_entrada)
                        salvar_dados_sistema()
                        registrar_alerta(f"Nova escala adicionada na {nome_da_extensao} para o dia {inp_data.strftime('%d/%m/%Y')}.")
                        st.success("Escala adicionada com sucesso!")
                        st.rerun()

                if lista_atual:
                    ids_disponiveis = [item["ID"] for item in lista_atual]
                    id_para_excluir = st.selectbox("Selecione o ID da linha para excluir", ids_disponiveis, key=f"del_escala_{i}")
                    if st.button(f"🗑️ Excluir Linha Selecionada ({nome_da_extensao})", key=f"btn_del_{i}"):
                        st.session_state.escalas[nome_da_extensao] = [item for item in lista_atual if item["ID"] != id_para_excluir]
                        salvar_dados_sistema()
                        registrar_alerta(f"Escala ID {id_para_excluir} foi removida da {nome_da_extensao}.")
                        st.success("Registro excluído com sucesso!")
                        st.rerun()

# 2. ABA DE MÚSICOS (COM CATEGORIAS EXATAS E INSTRUMENTOS AUTOMATIZADOS)
with aba_musicos:
    st.subheader("🎸 Equipe de Músicos & Instrumentos")
    if st.session_state.musicos:
        df_musicos = pd.DataFrame(st.session_state.musicos)
        st.dataframe(df_musicos, use_container_width=True)
    else:
        st.info("Nenhum músico cadastrado.")

    if st.session_state.logado:
        st.markdown("---")
        st.markdown("### ➕ Cadastrar Novo Músico")
        
        nomes_participantes_musicos = [p["Nome"] for p in st.session_state.participantes] if st.session_state.participantes else ["João Silva", "Maria Oliveira"]

        # RESTRIÇÃO EXATA DAS CATEGORIAS SOLICITADAS
        lista_categorias_exatas = ["Cordas", "Teclas", "Percussão", "Outro"]

        # MAPEAMENTO DOS PRINCIPAIS INSTRUMENTOS USADOS NAS IGREJAS ATUALMENTE
        mapa_instrumentos_igreja = {
            "Cordas": ["Violão", "Guitarra", "Contrabaixo", "Violino", "Viola", "Ukulele", "Cello"],
            "Teclas": ["Teclado", "Piano", "Órgão", "Synthesizer", "Piano Digital"],
            "Percussão": ["Bateria", "Cajón", "Pandeiro", "Bongô", "Congas", "Timbales", "Percussão Geral"],
            "Outro": ["Saxofone", "Flauta", "Trompete", "Clarinet", "Vocal / Backing Vocal"]
        }

        with st.form("form_novo_musico"):
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                nome_musico = st.selectbox("Nome do Músico", [""] + nomes_participantes_musicos)
            
            with col_m2:
                # Menu suspenso estrito contendo APENAS: Cordas, Teclas, Percussão, Outro
                categoria_selecionada = st.selectbox("Categoria", lista_categorias_exatas)
            
            with col_m3:
                # Menu suspenso dinâmico baseado na categoria escolhida com os instrumentos da igreja
                instrumentos_disponiveis = mapa_instrumentos_igreja.get(categoria_selecionada, ["Outro"])
                instrumento_principal = st.selectbox("Instrumento Principal", instrumentos_disponiveis)

            if st.form_submit_button("➕ Cadastrar Músico"):
                if nome_musico:
                    novo_id = max([m["ID"] for m in st.session_state.musicos], default=0) + 1
                    st.session_state.musicos.append({
                        "ID": novo_id,
                        "Nome": nome_musico,
                        "Instrumento": instrumento_principal,
                        "Categoria": categoria_selecionada
                    })
                    salvar_dados_sistema()
                    registrar_alerta(f"Músico cadastrado: {nome_musico} ({instrumento_principal}).")
                    st.success(f"Músico {nome_musico} adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Por favor, selecione o nome do músico.")

        if st.session_state.musicos:
            st.markdown("---")
            st.markdown("### 🛠️ Gerenciar / Editar / Excluir Músico")
            
            opcoes_musicos = {f"ID {m['ID']} - {m['Nome']} ({m['Instrumento']})": m for m in st.session_state.musicos}
            escolha_musico_str = st.selectbox("Selecione o Músico para Editar ou Excluir", list(opcoes_musicos.keys()), key="select_gerenciar_musico")
            
            musico_selecionado = opcoes_musicos[escolha_musico_str]

            with st.form("form_editar_excluir_musico"):
                ed_nome = st.text_input("Nome do Músico", value=musico_selecionado["Nome"])
                ed_cat = st.selectbox("Categoria", lista_categorias_exatas, index=lista_categorias_exatas.index(musico_selecionado["Categoria"]) if musico_selecionado["Categoria"] in lista_categorias_exatas else 0)
                
                # Lista de instrumentos para edição com base na categoria atual selecionada
                ed_inst_lista = mapa_instrumentos_igreja.get(ed_cat, ["Outro"])
                ed_inst = st.selectbox("Instrumento Principal", ed_inst_lista, index=ed_inst_lista.index(musico_selecionado["Instrumento"]) if musico_selecionado["Instrumento"] in ed_inst_lista else 0)

                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    btn_salvar_edicao = st.form_submit_button("💾 Salvar Alterações")
                with col_b2:
                    btn_excluir_musico = st.form_submit_button("🗑️ Excluir Músico")

                if btn_salvar_edicao:
                    for m in st.session_state.musicos:
                        if m["ID"] == musico_selecionado["ID"]:
                            m["Nome"] = ed_nome
                            m["Categoria"] = ed_cat
                            m["Instrumento"] = ed_inst
                            break
                    salvar_dados_sistema()
                    registrar_alerta(f"Músico atualizado: {ed_nome}.")
                    st.success("Músico atualizado com sucesso!")
                    st.rerun()

                if btn_excluir_musico:
                    st.session_state.musicos = [m for m in st.session_state.musicos if m["ID"] != musico_selecionado["ID"]]
                    salvar_dados_sistema()
                    registrar_alerta(f"Músico removido: {musico_selecionado['Nome']}.")
                    st.success("Músico excluído com sucesso!")
                    st.rerun()

# 3. ABA DE REPERTÓRIO
with aba_repertorio:
    st.subheader("🎶 Repertório de Cifras e Músicas")
    for musica, dados in st.session_state.repertorio.items():
        with st.expander(f"{musica} — Artista: {dados['Artista']}"):
            st.markdown(f"**Cifra / Letra:**\n\n{dados['Cifra']}")
            if st.session_state.logado:
                if st.button(f"🗑️ Excluir Música: {musica}", key=f"del_musica_{musica}"):
                    del st.session_state.repertorio[musica]
                    salvar_dados_sistema()
                    registrar_alerta(f"Música excluída do repertório: {musica}.")
                    st.success("Música removida!")
                    st.rerun()

    if st.session_state.logado:
        st.markdown("---")
        st.markdown("### ➕ Adicionar Nova Música")
        with st.form("form_nova_musica"):
            m_nome = st.text_input("Nome da Música")
            m_artista = st.text_input("Artista / Banda")
            m_cifra = st.text_area("Cifra Completa")
            if st.form_submit_button("Cadastrar Música"):
                if m_nome and m_cifra:
                    st.session_state.repertorio[m_nome] = {"Artista": m_artista, "Cifra": m_cifra}
                    salvar_dados_sistema()
                    registrar_alerta(f"Nova música adicionada ao repertório: {m_nome}.")
                    st.success("Música cadastrada!")
                    st.rerun()

# 4. ABA DE DANÇAS
with aba_danca:
    st.subheader("🩰 Ministério de Dança - Escalas e Ensaios")
    if st.session_state.danca:
        df_danca = pd.DataFrame(st.session_state.danca)
        st.dataframe(df_danca, use_container_width=True)
    else:
        st.info("Nenhum registro no Ministério de Dança cadastrado.")

    if st.session_state.logado:
        st.markdown("---")
        st.markdown("### 🛠️ Adicionar Registro de Dança")
        
        nomes_participantes_danca = [p["Nome"] for p in st.session_state.participantes] if st.session_state.participantes else ["Ana Souza", "Beatriz Lima"]

        with st.form("form_danca"):
            d_data = st.date_input("Data do Evento/Ensaio")
            d_responsaveis = st.selectbox("Selecione o Responsável / Coreógrafa", [""] + nomes_participantes_danca)
            d_obs = st.text_input("Observações / Coreografia")
            if st.form_submit_button("➕ Adicionar Registro de Dança"):
                novo_registro_danca = {
                    "ID": len(st.session_state.danca) + 1,
                    "Data": d_data.strftime("%d/%m/%Y"),
                    "Responsáveis": d_responsaveis,
                    "Observações": d_obs
                }
                st.session_state.danca.append(novo_registro_danca)
                salvar_dados_sistema()
                registrar_alerta(f"Registro de dança adicionado para o dia {d_data.strftime('%d/%m/%Y')}.")
                st.success("Registro adicionado com sucesso!")
                st.rerun()

        if st.session_state.danca:
            ids_danca = [d["ID"] for d in st.session_state.danca]
            id_del_d = st.selectbox("Selecione o ID do registro de dança para excluir", ids_danca)
            if st.button("🗑️ Excluir Registro de Dança"):
                st.session_state.danca = [d for d in st.session_state.danca if d["ID"] != id_del_d]
                salvar_dados_sistema()
                registrar_alerta(f"Registro de dança ID {id_del_d} removido.")
                st.success("Registro removido com sucesso!")
                st.rerun()

# 5. ABA DE DEVOCIONAL & BÍBLIA (SINCRONIZADA COM O SITE DA BÍBLIA ONLINE)
with aba_devocional:
    st.subheader("📖 Devocional, Versículo & Bíblia Online")
    
    lista_versiculos_bkj1611 = [
        {
            "texto": "Ó Deus, tu és o meu Deus; de madrugada te busco; a minha alma tem sede de ti; a minha carne te deseja em uma terra seca e cansada, onde não há água.",
            "referencia": "Salmos 63:1 (BKJ 1611)"
        },
        {
            "texto": "Cantai ao Senhor um cântico novo; cantai ao Senhor, toda a terra. Cantai ao Senhor, bendizei o seu nome; anunciai a sua salvação de dia em dia.",
            "referencia": "Salmos 96:1-2 (BKJ 1611)"
        },
        {
            "texto": "E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor, e não aos homens; sabendo que recebereis do Senhor o galardão da herança, porque a Cristo, o Senhor, servis.",
            "referencia": "Colossenses 3:23-24 (BKJ 1611)"
        }
    ]

    total_minutos_atual = int(datetime.now().timestamp() // 60)
    bloco_index = (total_minutos_atual // 90) % len(lista_versiculos_bkj1611)
    versiculo_da_vez = lista_versiculos_bkj1611[bloco_index]

    st.markdown(f"""
        <div class='bloco-versiculo'>
            <h3 style='margin-bottom: 5px; color: #ffffff;'>📖 Palavra para Edificação (Versão BKJ 1611)</h3>
            <p style='font-size: 16px; font-style: italic; margin-bottom: 8px; color: #f0fdf4;'>“{versiculo_da_vez['texto']}”</p>
            <p style='text-align: right; font-weight: bold; margin: 0; color: #bbf7d0;'>— {versiculo_da_vez['referencia']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌐 Seletor de Traduções da Bíblia (Sincronizado)")
    st.info("💡 Este menu de traduções fica aberto e acessível a todos os usuários para escolher a versão desejada da Bíblia.")

    col_t, col_b = st.columns([3, 1])
    with col_t:
        traducao_biblia_escolhida = st.selectbox(
            "Selecione a Tradução da Bíblia",
            options=[
                "Almeida Corrigida Fiel (ACF)",
                "Nova Versão Internacional (NVI)",
                "Almeida Revista e Atualizada (ARA)",
                "Nova Almeida Atualizada (NAA)",
                "Nova Tradução na Linguagem de Hoje (NTLH)",
                "Almeida Revista e Corrigida (ARC)",
                "King James Atualizada (KJA)"
            ],
            index=0
        )
    with col_b:
        st.write("")
        st.write("")
        if st.button("🔄 Atualizar Versículo"):
            st.rerun()

    sigla_map_site = {
        "Almeida Corrigida Fiel (ACF)": "acf",
        "Nova Versão Internacional (NVI)": "nvi",
        "Almeida Revista e Atualizada (ARA)": "ara",
        "Nova Almeida Atualizada (NAA)": "naa",
        "Nova Tradução na Linguagem de Hoje (NTLH)": "ntlh",
        "Almeida Revista e Corrigida (ARC)": "arc",
        "King James Atualizada (KJA)": "kja"
    }
    sigla_escolhida = sigla_map_site.get(traducao_biblia_escolhida, "acf")

    link_biblia_online = f"https://www.bibliaonline.com.br/{sigla_escolhida}/sl/119/105"

    st.markdown(f"""
        <div class="bloco-admin">
            <h4>📖 Passagem de Referência ({traducao_biblia_escolhida})</h4>
            <p style="font-size: 16px; font-style: italic;">“Lâmpada para os meus pés é tua palavra, e luz para o meu caminho.” — Salmos 119:105</p>
            <br>
            <a href="{link_biblia_online}" target="_blank" style="background-color: #16a34a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold;">🔗 Abrir Salmos 119:105 na Bíblia Online ({traducao_biblia_escolhida})</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔔 Histórico de Alertas e Notificações do Sistema")
    if st.session_state.logs_notificacoes:
        for log in st.session_state.logs_notificacoes[:10]:
            st.markdown(f"""
                <div class='alerta-item'>
                    <small style='color: #4ade80; font-weight: bold;'>📅 {log['data']}</small><br>
                    <span style='color: #f8fafc;'>{log['mensagem']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum registro de alerta recente.")
