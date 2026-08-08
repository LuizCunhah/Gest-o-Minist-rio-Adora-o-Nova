import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import base64

# Configuração da Página Web
st.set_page_config(
    page_title="Gestão de Louvor Matriz",
    page_icon="🎵",
    layout="wide"
)

# --- CONVERSÃO DA IMAGEM PARA BASE64 (ESTABILIZAÇÃO DO FUNDO SEM PISCAR) ---
def obter_base64_imagem(caminho_imagem):
    if os.path.exists(caminho_imagem):
        with open(caminho_imagem, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

# Salvando a imagem de fundo de referência enviada pelo usuário
CAMINHO_FUNDO_FOTO = "fundo_folhas_orvalho.jpg"
with open(CAMINHO_FUNDO_FOTO, "wb") as f_img:
    f_img.write(b"") # Placeholder interno para persistência do ambiente

img_base64 = obter_base64_imagem(CAMINHO_FUNDO_FOTO)

# --- ESTILOS CSS DEFINITIVOS (FUNDO DISCRETO COM A FOTO, SEM REFLOW/PISCAR) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(240, 244, 240, 0.88), rgba(240, 244, 240, 0.88)), url("data:image/jpeg;base64,{img_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        color: #1e293b !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {{
        color: #1e293b !important;
    }
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label {{
        color: #14532d !important;
        font-weight: 600 !important;
    }
    
    /* CORREÇÃO DOS CAMPOS DE ENTRADA */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #0f172a !important;
        border: 1px solid #86efac !important;
        border-radius: 6px !important;
    }
    
    .titulo-principal {{
        font-size: 38px !important;
        font-weight: bold !important;
        color: #14532d !important;
        text-align: center;
        margin-top: 10px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.9);
    }
    .sub-titulo {{
        font-size: 18px !important;
        color: #166534 !important;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 500;
    }
    div.stButton > button:first-child {{
        background-color: #15803d !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }
    .bloco-admin {{
        background-color: rgba(255, 255, 255, 0.92);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #22c55e;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .bloco-versiculo {{
        background: linear-gradient(135deg, #14532d 0%, #166534 100%);
        color: white !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .bloco-versiculo *, .bloco-versiculo p, .bloco-versiculo h3 {{
        color: white !important;
    }
    .alerta-item {{
        background-color: rgba(255, 255, 255, 0.92);
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 5px solid #22c55e;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS PERMANENTES (JSON) ---
ARQUIVO_CONFIG = "dados_config.json"
ARQUIVO_ESCALAS = "dados_escalas.json"
ARQUIVO_REPERTORIO = "dados_repertorio.json"
ARQUIVO_LOGS = "dados_logs.json"
ARQUIVO_DANCA = "dados_danca.json"
ARQUIVO_MUSICOS = "dados_musicos.json"

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
            {"ID": 1, "Nome": "João Silva", "Instrumento": "Guitarra Base/Solo", "Categoria": "Cordas"},
            {"ID": 2, "Nome": "Maria Oliveira", "Instrumento": "Teclado / Piano", "Categoria": "Teclas"}
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

# --- EXIBIÇÃO DO BANNER OU TÍTULO NO TOPO ---
if st.session_state.banner_path and os.path.exists(st.session_state.banner_path):
    st.image(st.session_state.banner_path, use_container_width=True)
else:
    st.markdown(f"<div class='titulo-principal'>{st.session_state.titulo_app}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-titulo'>{st.session_state.sub_titulo_app}</div>", unsafe_allow_html=True)

# --- BLOCO DE VERSÍCULO AUTOMÁTICO (VERSÃO BKJ 1611 - MUDANÇA A CADA 1H30) ---
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
    },
    {
        "texto": "Alegrei-me quando me disseram: Vamos à casa do Senhor. Os nossos pés pararão dentro das tuas portas, ó Jerusalém.",
        "referencia": "Salmos 122:1-2 (BKJ 1611)"
    },
    {
        "texto": "Louvai ao Senhor, porque ele é bom; porque a sua misericórdia dura para sempre.",
        "referencia": "Salmos 136:1 (BKJ 1611)"
    },
    {
        "texto": "Eu te exaltarei, ó Deus, meu Rei; e bendirei o teu nome para todo o sempre. Todos os dias te bendirei, e louvarei o teu nome para todo o sempre.",
        "referencia": "Salmos 145:1-2 (BKJ 1611)"
    },
    {
        "texto": "Mas a hora vem, e agora é, em que os verdadeiros adoradores adorarão o Pai em espírito e em verdade; porque o Pai procura a tais que assim o adorem.",
        "referencia": "João 4:23 (BKJ 1611)"
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

# --- SISTEMA DE LOGIN PÚBLICO / ADM ---
st.markdown("<div class='bloco-admin'>", unsafe_allow_html=True)
if not st.session_state.logado:
    st.markdown("### 🔒 Acesso Público (Visualização Livre) / Painel Administrativo")
    st.info("💡 Todos podem navegar livremente pelo aplicativo. Insira as credenciais abaixo apenas se precisar alterar, cadastrar ou excluir dados:")
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
        st.markdown(f"🟢 **Modo Administrador Ativo (Logado como: {st.session_state.usuario_atual})**. Funções de edição e exclusão liberadas.")
    with col_inf2:
        if st.button("🚪 Sair do Modo ADM", use_container_width=True):
            st.session_state.logado = False
            st.session_state.usuario_atual = None
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- PAINEL DE CONFIGURAÇÕES GLOBAIS E UPLOAD DE BANNER (APENAS ADM) ---
if st.session_state.logado:
    with st.container():
        st.markdown("<div class='bloco-admin'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Painel de Configurações, Capa e ADMs")
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            edt_titulo = st.text_input("Editar Título do Aplicativo", value=st.session_state.titulo_app)
        with col_t2:
            edt_sub = st.text_input("Editar Subtítulo do Aplicativo", value=st.session_state.sub_titulo_app)

        st.markdown("#### 🖼️ Inserir Imagem de Capa (Banner Superior)")
        arquivo_banner = st.file_uploader("Escolha uma imagem (PNG, JPG, JPEG) para usar como banner de capa", type=["png", "jpg", "jpeg"])
        
        if arquivo_banner is not None:
            caminho_salvar = "banner_capa.png"
            with open(caminho_salvar, "wb") as f:
                f.write(arquivo_banner.getbuffer())
            st.session_state.banner_path = caminho_salvar
            st.success("Banner enviado com sucesso! Clique em salvar alterações abaixo para aplicar.")

        st.markdown("**Nomes das 3 Extensões Cadastradas:**")
        col_ex0, col_ex1, col_ex2 = st.columns(3)
        with col_ex0:
            nome_ext0 = st.text_input("Extensão 1", value=st.session_state.nomes_extensoes[0])
        with col_ex1:
            nome_ext1 = st.text_input("Extensão 2", value=st.session_state.nomes_extensoes[1])
        with col_ex2:
            nome_ext2 = st.text_input("Extensão 3", value=st.session_state.nomes_extensoes[2])

        if st.button("💾 SALVAR ALTERAÇÕES GLOBAIS"):
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
        st.markdown("</div>", unsafe_allow_html=True)

# --- NAVEGAÇÃO POR ABAS ---
aba_escalas, aba_musicos, aba_repertorio, aba_danca, aba_devocional = st.tabs([
    "📊 Escalas Sincronizadas", "🎸 Gestão de Músicos", "🎶 Repertório & Cifras", "🩰 Ministério de Dança", "📖 Devocional & Alertas"
])

# 1. ABA DE ESCALAS
with aba_escalas:
    sub_abas_locais = st.tabs([f"📍 {nome}" for nome in st.session_state.nomes_extensoes])

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
                        inp_vocal = st.text_input("Vocais", key=f"vocal_{i}")
                    with c_musicos:
                        inp_musicos = st.text_input("Músicos", key=f"musicos_{i}")

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

# 2. ABA DE MÚSICOS
with aba_musicos:
    st.subheader("🎸 Equipe de Músicos & Instrumentos")
    if st.session_state.musicos:
        df_musicos = pd.DataFrame(st.session_state.musicos)
        st.dataframe(df_musicos, use_container_width=True)
    else:
        st.info("Nenhum músico cadastrado.")

    if st.session_state.logado:
        st.markdown("---")
        st.markdown("### 🛠️ Adicionar ou Alterar Músico")
        with st.form("form_novo_musico"):
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                nome_musico = st.text_input("Nome do Músico")
            with col_m2:
                categoria_inst = st.selectbox("Categoria", ["Cordas", "Teclas", "Percussão / Bateria", "Outros"])
            with col_m3:
                instrumento_especifico = st.text_input("Instrumento Principal")

            if st.form_submit_button("➕ Cadastrar Músico"):
                if nome_musico:
                    novo_id = len(st.session_state.musicos) + 1
                    st.session_state.musicos.append({
                        "ID": novo_id,
                        "Nome": nome_musico,
                        "Instrumento": instrumento_especifico,
                        "Categoria": categoria_inst
                    })
                    salvar_dados_sistema()
                    registrar_alerta(f"Músico cadastrado/atualizado: {nome_musico}.")
                    st.success(f"Músico {nome_musico} adicionado com sucesso!")
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

# 4. ABA DE DANÇAS (COM BOTÃO DE EXCLUIR)
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
        with st.form("form_danca"):
            d_data = st.date_input("Data do Evento/Ensaio")
            d_responsaveis = st.text_input("Responsáveis / Coreógrafas")
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
                registrar_alerta(f"Novo registro adicionado no Ministério de Dança para {d_data.strftime('%d/%m/%Y')}.")
                st.success("Registro de dança adicionado!")
                st.rerun()

        if st.session_state.danca:
            st.markdown("---")
            st.markdown("### 🗑️ Excluir Registro de Dança")
            ids_danca_disponiveis = [item["ID"] for item in st.session_state.danca]
            id_danca_para_excluir = st.selectbox("Selecione o ID do registro de dança para excluir", ids_danca_disponiveis, key="del_danca_select")
            if st.button("🗑️ Excluir Registro de Dança Selecionado", key="btn_del_danca"):
                st.session_state.danca = [item for item in st.session_state.danca if item["ID"] != id_danca_para_excluir]
                salvar_dados_sistema()
                registrar_alerta(f"Registro de dança ID {id_danca_para_excluir} foi removido.")
                st.success("Registro de dança excluído com sucesso!")
                st.rerun()

# 5. ABA DE DEVOCIONAL E ALERTAS
with aba_devocional:
    st.subheader("📖 Histórico de Modificações & Alertas")
    st.info("💡 Sempre que abrir o link do aplicativo, esta aba exibirá o histórico completo e cronológico de todas as modificações feitas pela liderança, garantindo que você veja o que mudou desde o último acesso.")
    
    if st.session_state.logs_notificacoes:
        st.markdown("---")
        for log in st.session_state.logs_notificacoes:
            if isinstance(log, dict):
                data_log = log.get("data", "")
                msg_log = log.get("mensagem", "")
            else:
                data_log = "Registro anterior"
                msg_log = str(log)
                
            st.markdown(f"""
                <div class='alerta-item'>
                    <span style='font-size: 12px; color: #64748b; font-weight: bold;'>🕒 {data_log}</span><br>
                    <span style='font-size: 15px; color: #1e293b;'>{msg_log}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("Nenhuma alteração registrada recentemente no sistema.")
