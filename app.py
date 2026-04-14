import streamlit as st
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# ============================================================================
# 1. CONFIGURAÇÃO STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="Linux Game | por Ary Ribeiro",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 2. CUSTOM CSS - ESTILO TERMINAL MS-DOS
# ============================================================================

def inject_custom_css():
    # Adicionar áudio de fundo em looping usando base64
    try:
        with open('static/som.mp3', 'rb') as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f"""
            <audio autoplay loop id="background-music">
                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            </audio>
            """, unsafe_allow_html=True)
    except Exception as e:
        print(f"Erro ao carregar áudio: {e}")
    
    st.markdown("""
    <style>
        /* Importar fonte monoespaçada */
        @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
        
        /* Reset geral */
        .main {
            background-color: #000000;
        }
        
        /* DESABILITAR BOTÃO DE FECHAR SIDEBAR - MANTER SEMPRE ABERTO */
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        
        /* FORÇAR SIDEBAR SEMPRE VISÍVEL */
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            transform: none !important;
            transition: none !important;
        }
        
        section[data-testid="stSidebar"] {
            width: 21rem !important;
            min-width: 21rem !important;
        }
        
        section[data-testid="stSidebar"] > div {
            width: 21rem !important;
            min-width: 21rem !important;
        }
        
        /* Terminal container */
        .terminal-container {
            background-color: #000000;
            color: #00FF00;
            font-family: 'Courier Prime', 'Courier New', Consolas, monospace;
            font-size: 16px;
            padding: 20px;
            border-radius: 5px;
            border: 2px solid #00FF00;
            min-height: 500px;
            max-height: 600px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        
        /* Prompt */
        .terminal-prompt {
            color: #00FF00;
            font-weight: bold;
        }
        
        /* Comando digitado */
        .terminal-command {
            color: #00FFFF;
            font-weight: bold;
        }
        
        /* Feedback sucesso */
        .terminal-success {
            color: #00FF00;
            font-weight: bold;
        }
        
        /* Feedback erro */
        .terminal-error {
            color: #FF0000;
            font-weight: bold;
        }
        
        /* Texto normal */
        .terminal-text {
            color: #FFFFFF;
        }
        
        /* Narrativa */
        .terminal-narrative {
            color: #FFFF00;
            font-style: italic;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1a1a1a;
        }
        
        /* Input field customization */
        .stTextInput > div > div > input {
            background-color: #000000;
            color: #00FF00;
            font-family: 'Courier Prime', 'Courier New', monospace;
            font-size: 16px;
            border: 2px solid #00FF00;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #00FF00;
        }
        
        /* Botão estilo terminal */
        .stButton > button {
            background-color: #003300;
            color: #00FF00;
            border: 2px solid #00FF00;
            font-family: 'Courier Prime', monospace;
            font-weight: bold;
            padding: 10px 20px;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #00FF00;
            color: #000000;
            border-color: #00FF00;
        }
        
        /* Esconder elementos desnecessários */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # JavaScript para garantir sidebar sempre visível
    st.markdown("""
    <script>
        function keepSidebarOpen() {
            const parentDoc = window.parent.document;
            
            // Remover qualquer classe que oculte o sidebar
            const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                sidebar.style.display = 'block';
                sidebar.style.visibility = 'visible';
                sidebar.style.transform = 'none';
                sidebar.classList.remove('collapsed');
            }
            
            // Esconder botão de colapso
            const collapseBtn = parentDoc.querySelector('[data-testid="stSidebarCollapseButton"]');
            if (collapseBtn) {
                collapseBtn.style.display = 'none';
            }
        }
        
        // Executar continuamente
        setInterval(keepSidebarOpen, 50);
        
        // Observer
        const observer = new MutationObserver(keepSidebarOpen);
        if (window.parent.document.body) {
            observer.observe(window.parent.document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['class', 'style']
            });
        }
    </script>
    """, unsafe_allow_html=True)

# ============================================================================
# 3. CARREGAR DADOS
# ============================================================================

@st.cache_data
def load_commands():
    """Carrega comandos do arquivo JSON"""
    try:
        with open('comandos.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar comandos.json: {e}")
        return []

# ============================================================================
# 4. ESTRUTURA DE FASES
# ============================================================================

def create_phases(commands):
    """Cria 17 fases temáticas com narrativa"""
    
    # Garantir que temos exatamente 170 comandos divididos em 17 fases
    total_commands = len(commands)
    commands_per_phase = 10
    
    phases = [
        {
            "nome": "Primeiros Passos no Terminal",
            "narrativa": "🕵️ Detetive {nome}, você acaba de receber um chamado urgente!\n🦹 O vilão CÁLCULUS hackeou os sistemas da cidade e está deixando pistas em servidores Linux.\n🎯 MISSÃO: Dominar os comandos básicos para rastrear o vilão!",
            "comandos": commands[0:10]
        },
        {
            "nome": "Investigando Arquivos",
            "narrativa": "🔍 Ótimo trabalho! Você encontrou o primeiro servidor comprometido.\n📂 Há arquivos suspeitos espalhados. Precisamos analisá-los!\n🎯 MISSÃO: Aprenda a visualizar e manipular arquivos.",
            "comandos": commands[10:20]
        },
        {
            "nome": "Manipulação Avançada",
            "narrativa": "💾 CÁLCULUS deixou arquivos criptografados!\n🔐 Precisamos copiar, mover e criar links para preservar evidências.\n🎯 MISSÃO: Domine operações avançadas com arquivos.",
            "comandos": commands[20:30]
        },
        {
            "nome": "Gerenciamento de Processos",
            "narrativa": "⚡ Detectamos processos maliciosos rodando no sistema!\n🎭 CÁLCULUS está executando scripts em segundo plano.\n🎯 MISSÃO: Aprenda a monitorar e encerrar processos.",
            "comandos": commands[30:40]
        },
        {
            "nome": "Conexões de Rede",
            "narrativa": "🌐 Encontramos atividade de rede suspeita!\n📡 CÁLCULUS está se conectando a servidores remotos.\n🎯 MISSÃO: Domine comandos de SSH e conectividade.",
            "comandos": commands[40:50]
        },
        {
            "nome": "Busca e Pesquisa",
            "narrativa": "🔎 As pistas estão espalhadas em centenas de arquivos!\n📋 Precisamos usar buscas avançadas para encontrar evidências.\n🎯 MISSÃO: Aprenda grep, locate e find.",
            "comandos": commands[50:60]
        },
        {
            "nome": "Informações do Sistema",
            "narrativa": "🖥️ Precisamos conhecer o terreno!\n📊 Vamos coletar informações sobre o sistema comprometido.\n🎯 MISSÃO: Domine comandos de diagnóstico.",
            "comandos": commands[60:70]
        },
        {
            "nome": "Compactação e Arquivos",
            "narrativa": "📦 CÁLCULUS escondeu dados em arquivos compactados!\n🗜️ Precisamos extrair e analisar esses pacotes.\n🎯 MISSÃO: Aprenda tar, gzip e compactação.",
            "comandos": commands[70:80]
        },
        {
            "nome": "Rede Avançada",
            "narrativa": "🌐 Rastreamento de rede em andamento!\n🔌 Vamos investigar conexões e portas abertas.\n🎯 MISSÃO: Domine ping, whois, dig e wget.",
            "comandos": commands[80:90]
        },
        {
            "nome": "Instalação de Software",
            "narrativa": "💿 Precisamos instalar ferramentas forenses!\n🛠️ CÁLCULUS modificou pacotes do sistema.\n🎯 MISSÃO: Aprenda dpkg, rpm e compilação.",
            "comandos": commands[90:100]
        },
        {
            "nome": "Hardware e Arquitetura",
            "narrativa": "🔧 Análise forense do hardware!\n💻 Vamos identificar todos os componentes do sistema.\n🎯 MISSÃO: Domine comandos de diagnóstico de hardware.",
            "comandos": commands[100:110]
        },
        {
            "nome": "Armazenamento e Discos",
            "narrativa": "💾 Investigação de discos e partições!\n📊 CÁLCULUS pode ter escondido dados em partições ocultas.\n🎯 MISSÃO: Aprenda df, du e análise de espaço.",
            "comandos": commands[110:120]
        },
        {
            "nome": "Informações Detalhadas",
            "narrativa": "🔬 Análise profunda do sistema!\n📡 Vamos coletar informações sobre rede, dispositivos e processos.\n🎯 MISSÃO: Domine lspci, lsusb e proc.",
            "comandos": commands[120:130]
        },
        {
            "nome": "Data e Hora",
            "narrativa": "⏰ Precisamos estabelecer uma linha do tempo!\n📅 Quando CÁLCULUS atacou? Vamos investigar logs de tempo.\n🎯 MISSÃO: Aprenda date, cal e uptime.",
            "comandos": commands[130:140]
        },
        {
            "nome": "Controle de Sistema",
            "narrativa": "🔴 Sistema crítico! Aprenda a controlar o desligamento.\n⚡ Precisamos reiniciar servidores com segurança.\n🎯 MISSÃO: Domine shutdown, reboot e halt.",
            "comandos": commands[140:150]
        },
        {
            "nome": "Navegação Avançada e Permissões",
            "narrativa": "🗂️ Navegação avançada necessária!\n🔐 CÁLCULUS modificou permissões de arquivos críticos.\n🎯 MISSÃO: Domine navegação e sistema de permissões.",
            "comandos": commands[150:170]
        },
        {
            "nome": "CONFRONTO FINAL",
            "narrativa": "🚨 ALERTA MÁXIMO! Você está no servidor principal de CÁLCULUS!\n🦹 Este é o confronto final! Ele deixou os comandos mais complexos como última defesa.\n🎯 MISSÃO FINAL: Prove que você é um mestre Linux!",
            "comandos": commands[170:] if len(commands) > 170 else []
        }
    ]
    
    return phases

# ============================================================================
# 5. INICIALIZAR SESSION STATE
# ============================================================================

def init_session_state():
    """Inicializa todas as variáveis de sessão"""
    
    if 'comandos' not in st.session_state:
        st.session_state.comandos = load_commands()
    
    if 'phases' not in st.session_state:
        st.session_state.phases = create_phases(st.session_state.comandos)
    
    if 'nome_jogador' not in st.session_state:
        st.session_state.nome_jogador = ""
    
    if 'fase_atual' not in st.session_state:
        st.session_state.fase_atual = 0
    
    if 'comando_atual_index' not in st.session_state:
        st.session_state.comando_atual_index = 0
    
    if 'comandos_completados' not in st.session_state:
        st.session_state.comandos_completados = 0
    
    if 'historico_terminal' not in st.session_state:
        st.session_state.historico_terminal = []
    
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    
    if 'game_completed' not in st.session_state:
        st.session_state.game_completed = False
    
    if 'tentativas_erro' not in st.session_state:
        st.session_state.tentativas_erro = 0
    
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    if 'mostrar_ajuda' not in st.session_state:
        st.session_state.mostrar_ajuda = False

# ============================================================================
# 6. FUNÇÕES DO JOGO
# ============================================================================

def get_current_command():
    """Retorna o comando atual que o jogador precisa digitar"""
    if st.session_state.fase_atual < len(st.session_state.phases):
        phase = st.session_state.phases[st.session_state.fase_atual]
        if st.session_state.comando_atual_index < len(phase['comandos']):
            return phase['comandos'][st.session_state.comando_atual_index]
    return None

def validate_command(user_input):
    """Valida se o comando digitado está correto"""
    current_cmd = get_current_command()
    
    if not current_cmd:
        return False
    
    # Normalização: remover espaços extras e converter para lowercase
    user_input_clean = ' '.join(user_input.strip().lower().split())
    expected_cmd_clean = ' '.join(current_cmd['comando'].strip().lower().split())
    
    return user_input_clean == expected_cmd_clean

def add_to_terminal(message, msg_type="text"):
    """Adiciona mensagem ao histórico do terminal"""
    css_class = {
        "prompt": "terminal-prompt",
        "command": "terminal-command",
        "success": "terminal-success",
        "error": "terminal-error",
        "text": "terminal-text",
        "narrative": "terminal-narrative"
    }.get(msg_type, "terminal-text")
    
    st.session_state.historico_terminal.append(f'<span class="{css_class}">{message}</span>')

def process_command(user_input):
    """Processa o comando digitado pelo usuário"""
    if not user_input.strip():
        return
    
    current_cmd = get_current_command()
    
    # Adicionar comando ao terminal
    add_to_terminal(f"detetive@linuxgame:~$ {user_input}", "command")
    
    # Validar comando
    if validate_command(user_input):
        # SUCESSO!
        st.session_state.comandos_completados += 1
        st.session_state.comando_atual_index += 1
        st.session_state.tentativas_erro = 0
        st.session_state.mostrar_ajuda = False  # Resetar ajuda ao acertar
        
        # Feedback de sucesso - APENAS ELOGIO
        add_to_terminal("✅ COMANDO CORRETO! Excelente trabalho, Detetive!", "success")
        add_to_terminal("", "text")
        
        # VERIFICAR SE COMPLETOU TODOS OS 170 COMANDOS
        if st.session_state.comandos_completados >= 170:
            st.session_state.game_completed = True
            add_to_terminal("", "text")
            add_to_terminal("🎉🎉🎉 PARABÉNS! VOCÊ CAPTUROU O CÁLCULUS! 🎉🎉🎉", "success")
            add_to_terminal("🏆 Missão cumprida com êxito total!", "success")
            add_to_terminal("🎓 Seu certificado está pronto!", "success")
            add_to_terminal("", "text")
            return  # Sair da função
        
        # Verificar se completou a fase atual
        phase = st.session_state.phases[st.session_state.fase_atual]
        if st.session_state.comando_atual_index >= len(phase['comandos']):
            st.session_state.fase_atual += 1
            st.session_state.comando_atual_index = 0
            
            # Mensagem de fase completa (se não for a última)
            if st.session_state.fase_atual < len(st.session_state.phases):
                add_to_terminal(f"🎊 FASE {st.session_state.fase_atual} COMPLETA!", "success")
                add_to_terminal(f"🚀 Avançando para: {st.session_state.phases[st.session_state.fase_atual]['nome']}", "narrative")
        
        # Forçar atualização do input APENAS em caso de sucesso
        st.session_state.input_key += 1
        
    else:
        # ERRO! - NÃO incrementar input_key para manter o valor no campo
        st.session_state.tentativas_erro += 1
        add_to_terminal("❌ Comando incorreto!", "error")
        add_to_terminal(f"💡 Tente novamente ou clique em 'Pedir Ajuda' no painel lateral.", "error")
        add_to_terminal("", "text")

# ============================================================================
# 7. GERAÇÃO DE CERTIFICADO
# ============================================================================

def generate_certificate(nome):
    """Gera certificado de conclusão em formato de imagem"""
    
    # Criar imagem do certificado
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Tentar carregar fontes (fallback para fonte padrão)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_name = ImageFont.load_default()
    
    # Desenhar borda
    draw.rectangle([(20, 20), (width-20, height-20)], outline='#00FF00', width=5)
    draw.rectangle([(30, 30), (width-30, height-30)], outline='#003300', width=2)
    
    # CARREGAR E INSERIR LOGO.PNG NO TOPO
    try:
        logo = Image.open('static/logo.png')
        # Redimensionar logo para caber no certificado
        logo_width = 300
        logo_ratio = logo_width / logo.size[0]
        logo_height = int(logo.size[1] * logo_ratio)
        logo_resized = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        # Centralizar logo
        logo_x = (width - logo_width) // 2
        logo_y = 50
        img.paste(logo_resized, (logo_x, logo_y), logo_resized if logo_resized.mode == 'RGBA' else None)
        y_start = logo_y + logo_height + 30
    except Exception as e:
        print(f"Erro ao carregar logo: {e}")
        y_start = 100
    
    # Título
    title = "CERTIFICADO DE CONCLUSÃO"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) / 2, y_start), title, fill='#003300', font=font_title)
    
    # Texto principal
    text_lines = [
        f"Certifico que:",
        f"{nome.upper()}",
        f"concluiu com êxito o treinamento em ambiente gamificado",
        f"LINUX GAME | https://linux-game.streamlit.app/",
        f"",
        f"Carga horária estimada: 4 horas",
        f"Data de conclusão: {datetime.now().strftime('%d/%m/%Y')}",
        f"",
        f"Domínio de 170 comandos Linux",
    ]
    
    y_position = y_start + 70
    for i, line in enumerate(text_lines):
        if line == nome.upper():
            font_current = font_name
            color = '#00FF00'
        elif line == "LINUX GAME":
            font_current = font_name
            color = '#003300'
        else:
            font_current = font_text
            color = '#000000'
        
        bbox = draw.textbbox((0, 0), line, font=font_current)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, y_position), line, fill=color, font=font_current)
        y_position += 50 if line == nome.upper() or line == "LINUX GAME" else 35
    
    # CARREGAR E INSERIR ASSINATURA.PNG NO RODAPÉ
    try:
        assinatura = Image.open('static/assinatura.png')
        # Redimensionar assinatura
        assin_width = 250
        assin_ratio = assin_width / assinatura.size[0]
        assin_height = int(assinatura.size[1] * assin_ratio)
        assin_resized = assinatura.resize((assin_width, assin_height), Image.Resampling.LANCZOS)
        # Centralizar assinatura
        assin_x = (width - assin_width) // 2
        assin_y = height - 150
        img.paste(assin_resized, (assin_x, assin_y), assin_resized if assin_resized.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Erro ao carregar assinatura: {e}")
    
    # Rodapé
    footer = "."
    footer_bbox = draw.textbbox((0, 0), footer, font=font_text)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) / 2, height - 50), footer, fill='#666666', font=font_text)
    
    return img

def get_image_download_link(img, filename):
    """Gera link de download para a imagem"""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">📥 BAIXAR CERTIFICADO</a>'
    return href

# ============================================================================
# 8. RENDERIZAÇÃO DA INTERFACE
# ============================================================================

def render_sidebar():
    """Renderiza a barra lateral com informações do jogo"""
    
    with st.sidebar:
        # Status do Jogador
        st.markdown("#### 🕵️ Status do Detetive:")
        st.markdown(f"**Nome:** {st.session_state.nome_jogador}")
        st.markdown(f"**Fase:** {st.session_state.fase_atual + 1}/17")
        st.markdown(f"**Comandos:** {st.session_state.comandos_completados}/170")
        
        # Barra de Progresso
        progress = st.session_state.comandos_completados / 170
        st.progress(progress)
        st.markdown(f"**{progress*100:.1f}%** completo")
        
        st.markdown("---")
        
        # Missão Atual
        if st.session_state.fase_atual < len(st.session_state.phases):
            phase = st.session_state.phases[st.session_state.fase_atual]
            
            st.markdown("#### 🎯 Missão Atual:")
            st.markdown(f"**{phase['nome']}**")
            
            current_cmd = get_current_command()
            if current_cmd:
                # DICA (sempre visível) - PRIMEIRO
                st.markdown("#### 💡 Dica da IA:")
                st.info(current_cmd['descricao'])
                
                st.markdown("")
                
                # BOTÃO PEDIR AJUDA
                ajuda_clicked = st.button("🆘 Pedir Ajuda a IA", use_container_width=True, key="btn_ajuda")
                
                if ajuda_clicked:
                    st.session_state.mostrar_ajuda = True
                
                st.markdown("")
                
                # COMANDO ESPERADO (só mostra se pediu ajuda)
                if st.session_state.mostrar_ajuda:
                    st.markdown("#### ⚠️ Resposta:")
                    st.code(current_cmd['comando'], language='bash')
                    st.warning("⚠️ Tente memorizar este comando!")
                else:
                    st.markdown("#### 🤔 Desafio:")
                    st.markdown("Leia a **dica acima** e tente lembrar qual comando Linux você deve usar.")
                    st.markdown("😎 *Se não pedir ajuda, é sinal que aprendeu*")
            
            st.markdown("---")
            
            # História da Fase
            st.markdown("#### 📜 Contexto da Missão:")
            narrative = phase['narrativa'].format(nome=st.session_state.nome_jogador)
            st.markdown(narrative)

def render_terminal():
    """Renderiza o terminal principal"""
    
    # Construir HTML do terminal
    terminal_html = '<div class="terminal-container" id="terminal-scroll">'
    
    # Adicionar histórico
    for line in st.session_state.historico_terminal:
        terminal_html += f'{line}<br>'
    
    # Prompt atual
    current_cmd = get_current_command()
    if current_cmd and not st.session_state.game_completed:
        terminal_html += '<span class="terminal-prompt">detetive@linuxgame:~$ </span>'
    
    terminal_html += '</div>'
    
    st.markdown(terminal_html, unsafe_allow_html=True)
    
    # Input de comando (apenas se o jogo não estiver completo)
    if not st.session_state.game_completed:
        # Criar um form para capturar ENTER do teclado
        with st.form(key=f"command_form_{st.session_state.input_key}", clear_on_submit=False):
            col1, col2 = st.columns([5, 1])
            
            with col1:
                user_input = st.text_input(
                    "Digite o comando:",
                    key=f"command_input_{st.session_state.input_key}",
                    label_visibility="collapsed",
                    placeholder="Digite o comando Linux aqui e pressione ENTER...",
                    value=""
                )
            
            with col2:
                enter_pressed = st.form_submit_button("▶ ENTER", use_container_width=True)
            
            # Processar comando quando o form é submetido (ENTER ou botão)
            if enter_pressed and user_input:
                process_command(user_input)
                st.rerun()
        
        # SOLUÇÃO DEFINITIVA: HTML + JavaScript inline
        st.components.v1.html("""
        <script>
        (function() {
            // Função para executar scroll e focus
            function executeActions() {
                try {
                    // Acessa o documento pai (Streamlit)
                    const parentDoc = window.parent.document;
                    
                    // 1. SCROLL DO TERMINAL
                    const terminal = parentDoc.getElementById('terminal-scroll');
                    if (terminal) {
                        terminal.scrollTop = terminal.scrollHeight;
                    }
                    
                    // 2. FOCUS NO INPUT
                    const inputs = parentDoc.querySelectorAll('input[type="text"]');
                    if (inputs && inputs.length > 0) {
                        // Pega o último input (o do comando)
                        const lastInput = inputs[inputs.length - 1];
                        if (lastInput) {
                            lastInput.focus();
                        }
                    }
                } catch(e) {
                    console.log('Erro ao executar ações:', e);
                }
            }
            
            // Executar imediatamente
            executeActions();
            
            // Executar após 100ms
            setTimeout(executeActions, 100);
            
            // Executar após 300ms
            setTimeout(executeActions, 300);
            
            // Executar após 500ms
            setTimeout(executeActions, 500);
            
            // Continuar executando a cada 200ms
            setInterval(executeActions, 200);
        })();
        </script>
        """, height=0)

def get_logo_base64():
    """Converte logo.png em base64 para embed no HTML"""
    try:
        with open('static/logo.png', 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ''

def render_welcome_screen():
    """Renderiza a tela inicial de boas-vindas"""

    logo_b64 = get_logo_base64()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:400px; max-width:100%;"/>' if logo_b64 else ''

    st.markdown(f"""
    <style>
        .main {{ background-color: #ffffff !important; }}
        .welcome-wrapper {{
            display: flex;
            justify-content: center;
            padding: 2rem 1rem 1rem 1rem;
        }}
        .welcome-box {{
            border: 6px solid #00FF00;
            border-radius: 12px;
            padding: 2.5rem 3rem;
            background: #ffffff;
            width: 100%;
            max-width: 700px;
            text-align: center;
            font-family: sans-serif;
            color: #222;
        }}
        .welcome-box p {{ text-align: left; font-size: 1rem; line-height: 1.7; }}
        .welcome-box hr {{ border-color: #ddd; margin: 1.2rem 0; }}
    </style>
    <div class="welcome-wrapper">
      <div class="welcome-box">
        {logo_html}
        <hr/>
        <h3>🕵️ BEM-VINDO, DETETIVE!</h3>
        <p>
          Você é um <strong>Detetive</strong> convocado para uma missão urgente:<br/><br/>
          🦹 <strong>O vilão CÁLCULUS</strong> hackeou os sistemas da cidade!<br/><br/>
          Para capturá-lo, você precisará dominar <strong>170 comandos Linux</strong> através de
          <strong>17 fases progressivas</strong> repletas de desafios e investigações.<br/><br/>
          🎯 <strong>Sua missão:</strong><br/>
          &nbsp;&nbsp;• Aprender comandos Linux de forma progressiva<br/>
          &nbsp;&nbsp;• Seguir as pistas deixadas pelo vilão<br/>
          &nbsp;&nbsp;• Completar todas as fases<br/>
          &nbsp;&nbsp;• Capturar CÁLCULUS e receber seu certificado!
        </p>
        <hr/>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Widgets Streamlit nativos abaixo do HTML — centralizados via colunas
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        _, c, _ = st.columns([1, 2, 1])
        with c:
            nome = st.text_input("Digite seu nome de Detetive:", placeholder="Ex: Detetive Silva")
            if st.button("🚀 INICIAR MISSÃO", use_container_width=True):
                if nome.strip():
                    st.session_state.nome_jogador = nome.strip()
                    st.session_state.game_started = True
                    add_to_terminal("=" * 80, "text")
                    add_to_terminal(f"🕵️ DETETIVE {nome.upper()} - MISSÃO INICIADA", "success")
                    add_to_terminal("=" * 80, "text")
                    add_to_terminal("", "text")
                    phase = st.session_state.phases[0]
                    for line in phase['narrativa'].format(nome=nome).split('\n'):
                        add_to_terminal(line, "narrative")
                    add_to_terminal("", "text")
                    add_to_terminal("💻 Digite os comandos Linux para avançar na investigação!", "text")
                    add_to_terminal("", "text")
                    st.rerun()
                else:
                    st.error("⚠️ Por favor, digite seu nome para começar!")

def render_victory_screen():
    """Renderiza a tela de vitória e certificado"""
    
    # Usar logo.png na tela de vitória também
    try:
        logo = Image.open('static/logo.png')
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao carregar logo: {e}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🎉 PARABÉNS, DETETIVE!")
        
        st.success(f"""
        **🦹 VOCÊ CAPTUROU O VILÃO CÁLCULUS!**
        
        🏆 Missão cumprida com êxito total!
        
        📊 **Suas conquistas:**
        - ✅ 170 comandos Linux dominados
        - ✅ 17 fases concluídas
        - ✅ Vilão capturado e sistemas restaurados
        
        ⏱️ **Tempo de treinamento:** 4 horas equivalentes
        
        🎓 **Seu certificado está pronto!**
        """)
        
        st.markdown("---")
        
        # Gerar e exibir certificado
        st.markdown("### 📜 SEU CERTIFICADO PROFISSIONAL")
        
        cert_img = generate_certificate(st.session_state.nome_jogador)
        st.image(cert_img, use_container_width=True)
        
        # Botão de download
        st.markdown(
            get_image_download_link(
                cert_img,
                f"certificado_linux_game_{st.session_state.nome_jogador.replace(' ', '_')}.png"
            ),
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Estatísticas finais
        st.markdown("### 📈 ESTATÍSTICAS DA MISSÃO")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Comandos Aprendidos", "170")
        
        with col_b:
            st.metric("Fases Completadas", "17")
        
        with col_c:
            st.metric("Taxa de Sucesso", "100%")
        
        st.markdown("---")
        
        # Opção de reiniciar
        if st.button("🔄 NOVA MISSÃO", use_container_width=True):
            # Resetar o jogo
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("""
        ### 🌟 PRÓXIMOS PASSOS
        
        Agora que você dominou o terminal Linux, continue sua jornada:
        
        - 🐧 **Pratique** em um sistema Linux real
        - 📚 **Aprofunde-se** em shell scripting
        - 🔧 **Configure** seu próprio servidor
        - 🚀 **Explore** administração de sistemas
        
        **Obrigado por jogar Linux Game!** 🎮
        """)

# ============================================================================
# 9. FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal da aplicação"""
    
    # Injetar CSS customizado
    inject_custom_css()
    
    # Inicializar session state
    init_session_state()
    
    # Verificar estado do jogo e renderizar tela apropriada
    if not st.session_state.game_started:
        # TELA INICIAL
        render_welcome_screen()
    
    elif st.session_state.game_completed:
        # TELA DE VITÓRIA
        render_victory_screen()
    
    else:
        # JOGO EM ANDAMENTO
        render_sidebar()
        render_terminal()
        
        # Easter egg - comandos especiais
        if st.session_state.comandos_completados == 85:  # Metade do jogo
            st.balloons()

# ============================================================================
# 10. EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #333333;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Esconde completamente todos os elementos da barra padrão do Streamlit */
    header {display: none !important;}
    footer {display: none !important;}
    #MainMenu {display: none !important;}
    /* Remove qualquer espaço em branco adicional */
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Remove quaisquer margens extras */
    .element-container {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <h4>LINUX GAME🐧</h4>
    🧠 Memorize comandos Linux em ambiente gamificado - Por <strong>Ary Ribeiro</strong>: <a href="mailto:aryribeiro@gmail.com">aryribeiro@gmail.com</a><br>
    <em>Obs.: foi testado apenas em computador - Emita seu certificado de 4 horas no final</em>
</div>
""", unsafe_allow_html=True)