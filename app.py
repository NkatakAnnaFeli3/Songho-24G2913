import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Songo Pro - Anna", layout="centered")

# --- 1. LOGIQUE ET ÉTAT DU JEU PYTHON ---
if "board" not in st.session_state:
    st.session_state.board = [7] * 14
    st.session_state.scores = [0, 0]
    st.session_state.tour = 0  # 0 = Joueur 1 (bas), 1 = Joueur 2 (haut)
    st.session_state.message = "Le Joueur 1 commence !"

def jouer_coup(pit):
    board = st.session_state.board
    tour = st.session_state.tour
    
    if (tour == 0 and pit > 6) or (tour == 1 and pit < 7):
        st.session_state.message = "❌ Ce n'est pas votre camp !"
        return
    if board[pit] == 0:
        st.session_state.message = "❌ Cette case est vide !"
        return
        
    seeds = board[pit]
    board[pit] = 0
    current = pit
    while seeds > 0:
        current = (current + 1) % 14
        if current == pit:
            current = (current + 1) % 14
        board[current] += 1
        seeds -= 1
        
    captured = 0
    while True:
        in_adversary_camp = (tour == 0 and 7 <= current <= 13) or (tour == 1 and 0 <= current <= 6)
        if in_adversary_camp and (board[current] in [2, 3, 4]):
            captured += board[current]
            board[current] = 0
            current = (current - 1 + 14) % 14
        else:
            break
            
    st.session_state.scores[tour] += captured
    st.session_state.tour = 1 - tour
    st.session_state.message = f"Au tour du Joueur {st.session_state.tour + 1}"

# --- 2. STYLE CSS IDENTIQUE À L'IMAGE 2 (COULEUR LIMITÉE + CADRE VERT) ---
st.markdown("""
<style>
    /* L'arrière-plan extérieur reste noir/sombre et ne déborde pas en vert */
    .stApp {
        background-color: #0f172a !important;
    }
    
    /* Le cadre de la console de jeu : Vert émeraude délimité exactement comme l'image 2 */
    .main-box {
        text-align: center;
        background: linear-gradient(135deg, #022c22 0%, #064e3b 50%, #022c22 100%) !important;
        padding: 30px 25px;
        border-radius: 16px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        border: 1px solid rgba(52, 211, 153, 0.2);
        max-width: 650px;
        margin: 20px auto;
    }
    
    .header-area {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    
    .game-title {
        color: #ffffff;
        margin: 0;
        font-size: 1.9rem;
        font-weight: bold;
        letter-spacing: 0.5px;
    }
    
    .timer-box {
        background: #022c22;
        padding: 5px 15px;
        border-radius: 20px;
        color: #34d399;
        font-weight: bold;
        font-family: monospace;
        font-size: 1.1rem;
        border: 1px solid #047857;
    }
    
    /* Style des métriques de score à l'intérieur du cadre vert */
    div[data-testid="stMetricValue"] {
        color: #f59e0b !important;
        font-weight: bold !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;
    }
    
    /* Plateau en bois traditionnel */
    .wood-board {
        background: #5c3a21;
        border: 8px solid #362213;
        border-radius: 20px;
        padding: 25px 15px;
        box-shadow: inset 0 0 25px rgba(0,0,0,0.9);
        margin: 20px 0;
    }
    
    /* Les trous du Songo */
    div.stButton > button {
        background: #1c0d04 !important;
        color: #fbbf24 !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border: 3px solid #2b160a !important;
        border-radius: 50% !important;
        width: 64px !important;
        height: 64px !important;
        margin: 0 auto !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-shadow: inset 0 6px 12px rgba(0,0,0,0.9) !important;
        transition: all 0.15s ease !important;
    }
    
    div.stButton > button:hover:not([disabled]) {
        background: #2b160a !important;
        border-color: #34d399 !important;
        transform: scale(1.05) !important;
    }
    
    div.stButton > button:disabled {
        opacity: 0.4 !important;
        border-color: #2b160a !important;
    }

    /* Bouton Réinitialiser d'origine à l'extérieur (Gris, Centré, Style Image 2) */
    .reset-zone {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    
    .reset-zone div.stButton > button {
        background: #1e293b !important; /* Couleur sombre d'origine */
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
        border-radius: 6px !important; /* Forme rectangulaire classique */
        width: 240px !important;
        height: 40px !important;
        border: 1px solid #475569 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
    }
    
    .reset-zone div.stButton > button:hover {
        background: #334155 !important;
        border-color: #64748b !important;
    }
    
    .footer-text {
        margin-top: 25px;
        font-size: 0.85rem;
        color: #94a3b8;
        font-style: italic;
    }
    
    .footer-text span {
        color: #10b981;
        font-weight: bold;
        font-style: normal;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. RENDU DE L'INTERFACE DE JEU ---
with st.container():
    # Tout le bloc visuel est englobé dans "main-box" (la boîte verte)
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    
    # En-tête : Titre et Chrono
    st.markdown(f"""
    <div class="header-area">
        <div class="game-title">🔴 Songo Master</div>
        <div class="timer-box">⏱️ <span id="custom-timer">00:00</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Zone des Scores
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="Joueur 2 (Haut)", value=st.session_state.scores[1])
    with col_s2:
        st.metric(label="Joueur 1 (Bas)", value=st.session_state.scores[0])
        
    # Message de statut
    st.markdown(f'<h3 style="color: white; margin-top: 15px; font-size: 1.3rem;">{st.session_state.message}</h3>', unsafe_allow_html=True)
    
    # Le Plateau en bois
    st.markdown('<div class="wood-board">', unsafe_allow_html=True)
    
    # Rangée du Haut (Joueur 2)
    cols_top = st.columns(7)
    for i, idx in enumerate(range(13, 6, -1)):
        with cols_top[i]:
            valeur_case = str(st.session_state.board[idx])
            if st.button(valeur_case, key=f"hole_{idx}", disabled=(st.session_state.tour == 0)):
                jouer_coup(idx)
                st.rerun()
                
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    
    # Rangée du Bas (Joueur 1)
    cols_bottom = st.columns(7)
    for idx in range(0, 7):
        with cols_bottom[idx]:
            valeur_case = str(st.session_state.board[idx])
            if st.button(valeur_case, key=f"hole_{idx}", disabled=(st.session_state.tour == 1)):
                jouer_coup(idx)
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Signature Anna intégrée au bas de la zone verte
    st.markdown('<div class="footer-text">Développé avec passion par <span>Anna</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. BOUTON RÉINITIALISER (À L'EXTÉRIEUR DU BLOC VERT COMME SUR L'IMAGE 2) ---
st.markdown('<div class="reset-zone">', unsafe_allow_html=True)
if st.button("🔄 Réinitialiser la partie", key="btn_reset_global"):
    st.session_state.board = [7] * 14
    st.session_state.scores = [0, 0]
    st.session_state.tour = 0
    st.session_state.message = "Partie réinitialisée. Joueur 1 commence !"
    st.markdown("<script>window.parent.songoStartTime = Date.now();</script>", unsafe_allow_html=True)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Chronomètre JavaScript autonome
components.html("""
<script>
    if (!window.parent.songoStartTime) window.parent.songoStartTime = Date.now();
    setInterval(() => {
        const elapsed = Math.floor((Date.now() - window.parent.songoStartTime) / 1000);
        const minutes = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const seconds = String(elapsed % 60).padStart(2, '0');
        const display = window.parent.document.getElementById('custom-timer');
        if (display) display.innerText = minutes + ':' + seconds;
    }, 1000);
</script>
""", height=0)