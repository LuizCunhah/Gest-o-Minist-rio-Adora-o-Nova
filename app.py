import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Gestão do Ministério de Adoração", layout="wide"
)

# Estilização CSS corrigida com aspas triplas para evitar erros de sintaxe
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #7c3aed;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #6d28d9;
        }
        .verse-box {
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            border-left: 5px solid #7c3aed;
            font-size: 18px;
            color: #e0e0e0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎵 Gestão do Ministério de Adoração")

# Criação das abas principais (incluindo a nova aba de versículo)
aba_musicos, aba_versiculo = st.tabs(
    ["Cadastrar Músicos", "📖 Versículo & Bíblia"]
)

# ==================== ABA 1: CADASTRAR MÚSICOS ====================
with aba_musicos:
  st.subheader("➕ Cadastrar Novo Músico")

  col1, col2, col3 = st.columns(3)

  with col1:
    nome_musico = st.text_input(
        "Nome do Músico", placeholder="Digite o nome completo"
    )

  with col2:
    # Mapeamento automatizado de categorias e seus instrumentos principais
    mapa_instrumentos = {
        "Teclados / Piano": [
            "Teclado",
            "Piano",
            "Órgão",
            "Synthesizer",
            "Órgão Eletrônico",
        ],
        "Percussão / Bateria": [
            "Bateria",
            "Percussão",
            "Cajón",
            "Bongô",
            "Timbales",
        ],
        "Cordas": [
            "Violão",
            "Guitarra",
            "Contrabaixo",
            "Violino",
            "Viola",
            "Ukulele",
            "Cello",
        ],
        "Geral": ["Músico / Vocal", "Ministro de Louvor", "Backing Vocal"],
    }

    categoria_selecionada = st.selectbox(
        "Categoria", options=["Selecione"] + list(mapa_instrumentos.keys())
    )

  with col3:
    # Lógica de automação: altera o menu de instrumento baseado na categoria escolhida
    if (
        categoria_selecionada
        and categoria_selecionada != "Selecione"
        and categoria_selecionada in mapa_instrumentos
    ):
      opcoes_instrumentos = mapa_instrumentos[categoria_selecionada]
    else:
      opcoes_instrumentos = ["Selecione a Categoria primeiro"]

    instrumento_principal = st.selectbox(
        "Instrumento Principal", options=opcoes_instrumentos
    )

  st.write("")
  if st.button("➕ Cadastrar Música / Músico"):
    if (
        not nome_musico
        or categoria_selecionada == "Selecione"
        or "primeiro" in instrumento_principal
    ):
      st.error(
          "Por favor, preencha o nome e selecione corretamente a categoria e o"
          " instrumento."
      )
    else:
      st.success(
          f"Músico **{nome_musico}** cadastrado com sucesso! Categoria:"
          f" **{categoria_selecionada}** | Instrumento: **{instrumento_principal}**"
      )

# ==================== ABA 2: VERSÍCULO & BÍBLIA ====================
with aba_versiculo:
  st.subheader("📖 Versículo do Dia & Leitura Bíblica")

  # Barra de ferramentas com traduções abertas e acessíveis a todos os usuários
  col_trad, col_btn = st.columns([3, 1])

  with col_trad:
    traducao_selecionada = st.selectbox(
        "Selecione a Tradução da Bíblia",
        options=[
            "Almeida Corrigida Fiel (ACF)",
            "Nova Versão Internacional (NVI)",
            "Almeida Revista e Atualizada (ARA)",
            "Nova Almeida Atualizada (NAA)",
            "Nova Tradução na Linguagem de Hoje (NTLH)",
            "Almeida Revista e Corrigida (ARC)",
            "King James Atualizada (KJA)",
        ],
        index=0,
    )

  with col_btn:
    st.write("")  # Alinhamento visual com o selectbox
    botao_atualizar = st.button("🔄 Atualizar Versículo")

  # Dicionário de siglas para sincronização com o site oficial
  sigla_map = {
      "Almeida Corrigida Fiel (ACF)": "acf",
      "Nova Versão Internacional (NVI)": "nvi",
      "Almeida Revista e Atualizada (ARA)": "ara",
      "Nova Almeida Atualizada (NAA)": "naa",
      "Nova Tradução na Linguagem de Hoje (NTLH)": "ntlh",
      "Almeida Revista e Corrigida (ARC)": "arc",
      "King James Atualizada (KJA)": "kja",
  }
  sigla = sigla_map.get(traducao_selecionada, "acf")

  # Exibição do versículo sincronizado
  st.markdown(
      f"""
    <div class="verse-box">
        <b>Salmos 119:105</b><br><br>
        <i>“Lâmpada para os meus pés é tua palavra, e luz para o meu caminho.”</i><br><br>
        <small style="color: #aaa;">Traduzido via: {traducao_selecionada}</small>
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.write("")
  # Botão com link direto sincronizado com as traduções oficiais do site solicitado
  link_site = f"https://www.bibliaonline.com.br/{sigla}/sl/119/105"
  st.markdown(
      f"🔗 **[Abrir esta passagem diretamente no site oficial da Bíblia"
      f" Online]({link_site})**",
      unsafe_allow_html=True,
  )
