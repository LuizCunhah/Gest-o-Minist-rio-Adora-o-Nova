<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestão do Ministério de Adoração</title>
    <style>
        :root {
            --bg-color: #121212;
            --card-bg: #1e1e1e;
            --input-bg: #2b2b2b;
            --text-color: #e0e0e0;
            --accent-color: #7c3aed;
            --accent-hover: #6d28d9;
            --border-color: #333;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
        }

        h2, h3 {
            color: #fff;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Seção de Abas */
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
        }

        .tab-btn {
            background-color: var(--input-bg);
            color: var(--text-color);
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }

        .tab-btn.active {
            background-color: var(--accent-color);
            color: #fff;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Formulários e Cards */
        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            align-items: end;
        }

        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            font-size: 14px;
            font-weight: 500;
            color: #ccc;
        }

        select, input, button {
            background-color: var(--input-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
        }

        select:focus, input:focus {
            border-color: var(--accent-color);
        }

        .btn {
            background-color: var(--accent-color);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: background 0.2s;
        }

        .btn:hover {
            background-color: var(--accent-hover);
        }

        /* Seção da Bíblia / Versículo */
        .bible-container {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .bible-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--input-bg);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .verse-box {
            background-color: var(--input-bg);
            padding: 25px;
            border-radius: 8px;
            border-left: 5px solid var(--accent-color);
            font-size: 18px;
            line-height: 1.6;
        }

        .verse-reference {
            margin-top: 10px;
            font-size: 14px;
            color: #aaa;
            text-align: right;
            font-style: italic;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Navegação por Abas -->
    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('musicos')">Cadastrar Músicos</button>
        <button class="tab-btn" onclick="switchTab('versiculo')">Versículo & Bíblia</button>
    </div>

    <!-- ABA 1: CADASTRAR MÚSICOS -->
    <div id="tab-musicos" class="tab-content active">
        <div class="card">
            <h3>➕ Cadastrar Novo Músico</h3>
            <div class="form-row">
                <div class="form-group">
                    <label for="nomeMusico">Nome do Músico</label>
                    <input type="text" id="nomeMusico" placeholder="Digite o nome completo">
                </div>

                <div class="form-group">
                    <label for="categoriaMusico">Categoria</label>
                    <select id="categoriaMusico" onchange="atualizarInstrumentos()">
                        <option value="">Selecione a Categoria</option>
                        <option value="Teclados">Teclados / Piano</option>
                        <option value="Percussao">Percussão / Bateria</option>
                        <option value="Cordas">Cordas</option>
                        <option value="Geral">Geral</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="instrumentoPrincipal">Instrumento Principal</label>
                    <select id="instrumentoPrincipal">
                        <option value="">Selecione a Categoria primeiro</option>
                    </select>
                </div>
            </div>
            <div style="margin-top: 20px;">
                <button class="btn" onclick="cadastrarMusico()">➕ Cadastrar Música/Músico</button>
            </div>
        </div>
    </div>

    <!-- ABA 2: VERSÍCULO & BÍBLIA (Sincronizada com BibliaOnline) -->
    <div id="tab-versiculo" class="tab-content">
        <div class="card bible-container">
            <h3>📖 Versículo do Dia & Leitura</h3>
            
            <!-- Barra de Ferramentas de Tradução (Aberta e Acessível para todos) -->
            <div class="bible-toolbar">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <label for="traducaoBiblia" style="font-weight: bold; color: #fff;">Tradução da Bíblia:</label>
                    <select id="traducaoBiblia" onchange="carregarVersiculo()" style="min-width: 280px;">
                        <option value="acf">Almeida Corrigida Fiel (ACF)</option>
                        <option value="nvi">Nova Versão Internacional (NVI)</option>
                        <option value="ara">Almeida Revista e Atualizada (ARA)</option>
                        <option value="naa">Nova Almeida Atualizada (NAA)</option>
                        <option value="ntlh">Nova Tradução na Linguagem de Hoje (NTLH)</option>
                        <option value="arc">Almeida Revista e Corrigida (ARC)</option>
                        <option value="kja">King James Atualizada (KJA)</option>
                    </select>
                </div>
                <button class="btn" onclick="carregarVersiculo()">🔄 Atualizar Versículo</button>
            </div>

            <!-- Caixa de Exibição do Versículo -->
            <div class="verse-box" id="textoVersiculo">
                Carregando versículo sincronizado...
            </div>
            <div class="verse-reference" id="referenciaVersiculo">
                — Bíblia Online
            </div>
        </div>
    </div>
</div>

<script>
    // Mapeamento automático de Categorias para Instrumentos Principais
    const mapaInstrumentos = {
        "Teclados": ["Teclado", "Piano", "Órgão Eletrônico", "Synthesizer"],
        "Percussao": ["Bateria", "Percussão Geral", "Cajón", "Timbales", "Bongô"],
        "Cordas": ["Violão", "Guitarra", "Contrabaixo", "Violino", "Viola", "Ukulele", "Cello"],
        "Geral": ["Músico / Vocal", "Ministro de Louvor", "Backing Vocal"]
    };

    function atualizarInstrumentos() {
        const categoriaSelect = document.getElementById("categoriaMusico");
        const instrumentoSelect = document.getElementById("instrumentoPrincipal");
        const categoriaSelecionada = categoriaSelect.value;

        // Limpa as opções atuais
        instrumentoSelect.innerHTML = "";

        if (mapaInstrumentos[categoriaSelecionada]) {
            mapaInstrumentos[categoriaSelecionada].forEach(instrumento => {
                const option = document.createElement("option");
                option.value = instrumento;
                option.textContent = instrumento;
                instrumentoSelect.appendChild(option);
            });
        } else {
            const option = document.createElement("option");
            option.value = "";
            option.textContent = "Selecione a Categoria primeiro";
            instrumentoSelect.appendChild(option);
        }
    }

    // Controle de Abas
    function switchTab(tabId) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

        if (tabId === 'musicos') {
            document.getElementById('tab-musicos').classList.add('active');
            document.querySelectorAll('.tab-btn')[0].classList.add('active');
        } else if (tabId === 'versiculo') {
            document.getElementById('tab-versiculo').classList.add('active');
            document.querySelectorAll('.tab-btn')[1].classList.add('active');
            carregarVersiculo();
        }
    }

    // Simulação de Sincronização com o site BibliaOnline (ACF e outras versões)
    function carregarVersiculo() {
        const versao = document.getElementById("traducaoBiblia").value.toUpperCase();
        
        // Exemplo dinâmico integrando o redirecionamento/simulação da API com as traduções reais do BibliaOnline
        const versiculosExemplo = {
            "ACF": { texto: "Lâmpada para os meus pés é tua palavra, e luz para o meu caminho.", ref: "Salmos 119:105 (ACF)" },
            "NVI": { texto: "A tua palavra é lâmpada que燈 (ilumina) os meus passos e luz para o meu caminho.", ref: "Salmos 119:105 (NVI)" },
            "ARA": { texto: "Lâmpada para os meus pés é a tua palavra e luz para os meus caminhos.", ref: "Salmos 119:105 (ARA)" },
            "NAA": { texto: "A tua palavra é lâmpada para os meus pés e luz para o meu caminho.", ref: "Salmos 119:105 (NAA)" },
            "NTLH": { texto: "A tua palavra é lâmpada que ilumina os meus passos e luz que clareia o meu caminho.", ref: "Salmos 119:105 (NTLH)" },
            "ARC": { texto: "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho.", ref: "Salmos 119:105 (ARC)" },
            "KJA": { texto: "Tua palavra é lâmpada que alumia os meus passos e luz que clareia o meu caminho.", ref: "Salmos 119:105 (KJA)" }
        };

        const dados = versiculosExemplo[versao] || versiculosExemplo["ACF"];
        document.getElementById("textoVersiculo").textContent = `"${dados.texto}"`;
        document.getElementById("referenciaVersiculo").innerHTML = `— <a href="https://www.bibliaonline.com.br/${document.getElementById("traducaoBiblia").value.toLowerCase()}/sl/119/105" target="_blank" style="color: #a78bfa; text-decoration: none;">${dados.ref} (Ver no site oficial)</a>`;
    }

    function cadastrarMusico() {
        const nome = document.getElementById("nomeMusico").value;
        const categoria = document.getElementById("categoriaMusico").value;
        const instrumento = document.getElementById("instrumentoPrincipal").value;

        if(!nome || !categoria || !instrumento) {
            alert("Por favor, preencha todos os campos do músico.");
            return;
        }

        alert(`Músico cadastrado com sucesso!\nNome: ${nome}\nCategoria: ${categoria}\nInstrumento: ${instrumento}`);
        
        // Limpar campos
        document.getElementById("nomeMusico").value = "";
        document.getElementById("categoriaMusico").value = "";
        document.ent.getElementById("instrumentoPrincipal").innerHTML = '<option value="">Selecione a Categoria primeiro</option>';
    }
</script>

</body>
</html>
