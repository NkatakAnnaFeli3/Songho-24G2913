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

# --- 2. STYLE ET DESIGN DE L'INTERFACE VERTE ---
st.markdown("""
<style>
    /* Application du fond vert global */
    .stApp {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 50%, #065f46 100%) !important;
    }
    
    /* Conteneur principal de l'application */
    .main-box {
        text-align: center;
        background: rgba(0, 0, 0, 0.5);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 10px;
    }
    
    .header-area {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }
    
    .game-title {
        color: #f1f5f9;
        margin: 0;
        font-size: 1.8rem;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    .timer-box {
        background: #022c22;
        padding: 6px 15px;
        border-radius: 20px;
        color: #34d399;
        font-weight: bold;
        font-family: monospace;
        font-size: 1.1rem;
        border: 1px solid #059669;
    }
    
    /* Plateau de jeu en bois traditionnel style Songo creusé */
    .wood-board {
        background: #5c3a21;
        border: 10px solid #362213;
        border-radius: 25px;
        padding: 25px 20px;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.95), 0 5px 15px rgba(0,0,0,0.5);
        margin: 20px 0;
    }
    
    /* Transformation des boutons en trous de Songo réalistes */
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
        box-shadow: inset 0 6px 12px rgba(0,0,0,0.9), 0 2px 4px rgba(255,255,255,0.05) !important;
        transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Effet d'illumination verte discrète au survol d'une case jouable */
    div.stButton > button:hover:not([disabled]) {
        background: #2b160a !important;
        border-color: #34d399 !important;
        transform: scale(1.06) !important;
        box-shadow: inset 0 4px 8px rgba(0,0,0,0.8), 0 0 15px rgba(52, 211, 153, 0.6) !important;
    }
    
    /* Style pour les trous inactifs (pas le tour du joueur) */
    div.stButton > button:disabled {
        opacity: 0.4 !important;
        border-color: #2b160a !important;
        box-shadow: inset 0 6px 12px rgba(0,0,0,0.9) !important;
    }
    
    /* Centrage parfait et harmonisation du bouton Réinitialiser */
    .reset-container {
        display: flex;
        justify-content: center;
        margin-top: 25px;
        margin-bottom: 5px;
    }
    
    .reset-container div.stButton > button {
        background: #059669 !important;
        color: white !important;
        font-size: 0.95rem !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        width: 240px !important;
        height: 42px !important;
        padding: 0 15px !important;
        border: 1px solid #34d399 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    
    .reset-container div.stButton > button:hover {
        background: #10b981 !important;
        box-shadow: 0 0 15px rgba(52, 211, 153, 0.5) !important;
        transform: translateY(-1px) !important;
    }
    
    .footer-text {
        margin-top: 20px;
        font-size: 0.85rem;
        color: #cbd5e1;
        font-style: italic;
    }
    
    .footer-text span {
        color: #34d399;
        font-weight: bold;
        font-style: normal;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. AFFICHAGE DES ÉLÉMENTS DE L'INTERFACE ---
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    
    # En-tête avec Titre et Chronomètre
    st.markdown(f"""
    <div class="header-area">
        <div class="game-title">🎴 Songo Master</div>
        <div class="timer-box">⏱️ <span id="custom-timer">00:00</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Section des scores
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="Joueur 2 (Haut)", value=st.session_state.scores[1])
    with col_s2:
        st.metric(label="Joueur 1 (Bas)", value=st.session_state.scores[0])
        
    st.subheader(st.session_state.message)
    
    # Début du plateau en bois
    st.markdown('<div class="wood-board">', unsafe_allow_html=True)
    
    # Rangée du Haut (Indices 13 à 7)
    cols_top = st.columns(7)
    for i, idx in enumerate(range(13, 6, -1)):
        with cols_top[i]:
            valeur_case = str(st.session_state.board[idx])
            if st.button(valeur_case, key=f"hole_{idx}", disabled=(st.session_state.tour == 0)):
                jouer_coup(idx)
                st.rerun()
                
    st.markdown('<div style="margin-top: 24px;"></div>', unsafe_allow_html=True)
    
    # Rangée du Bas (Indices 0 à 6)
    cols_bottom = st.columns(7)
    for idx in range(0, 7):
        with cols_bottom[idx]:
            valeur_case = str(st.session_state.board[idx])
            if st.button(valeur_case, key=f"hole_{idx}", disabled=(st.session_state.tour == 1)):
                jouer_coup(idx)
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Zone de réinitialisation parfaitement centrée
    st.markdown('<div class="reset-container">', unsafe_allow_html=True)
    if st.button("🔄 Réinitialiser la partie", key="btn_reset_global"):
        st.session_state.board = [7] * 14
        st.session_state.scores = [0, 0]
        st.session_state.tour = 0
        st.session_state.message = "Partie réinitialisée. Joueur 1 commence !"
        st.markdown("<script>window.parent.songoStartTime = Date.now();</script>", unsafe_allow_html=True)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Signature
    st.markdown('<div class="footer-text">Développé avec passion par <span>Anna</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Script JavaScript autonome pour animer le chronomètre
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