import streamlit as st

# --- Configuração da Página ---
st.set_page_config(page_title="MI Grade Calculator v1.0", layout="wide")

# --- CSS Customizado para Estilo Skeuomorphic (2010) ---
st.markdown("""
<style>
    /* Chassi Principal (Alumínio Escovado) */
    .stApp {
        background-color: #2b2b2b;
        background-image: url('https://www.transparenttextures.com/patterns/brushed-alum.png');
        font-family: 'Courier New', Courier, monospace;
    }

    /* Painel de Conteúdo Recuado */
    .st-emotion-cache-z5fcl4 {
        background-color: #d8d0c3;
        border-radius: 15px;
        padding: 30px;
        box-shadow: inset 5px 5px 15px rgba(0,0,0,0.4), 
                    inset -5px -5px 15px rgba(255,255,255,0.1),
                    5px 5px 10px rgba(0,0,0,0.5);
        border: 2px solid #555;
    }

    /* Títulos e Texto (Visual de Tela Antiga) */
    h1, h2, h3, .stMarkdown {
        color: #111;
        text-shadow: 1px 1px 0px rgba(255,255,255,0.3);
    }

    /* Displays LCD (Segmentos) */
    .stNumberInput input, .stDisplay {
        background-color: #9ab39a !important; /* Cor LCD */
        color: #000 !important;
        font-family: 'IDAutomationHC39M', 'Courier New', monospace; /* Fonte Segmentada se possível */
        font-size: 2.5rem !important;
        border: 4px solid #444 !important;
        border-radius: 5px !important;
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.6) !important;
        text-align: center;
        padding: 10px !important;
    }

    /* Botão Rotativo (Simulado com Slider customizado) */
    .stSlider > div > div > div > div {
        background: linear-gradient(145deg, #ddd, #bbb);
        border: 3px solid #666;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.5);
    }

    /* Botões Físicos (Segmentados e Calculadoras) */
    .stButton>button {
        background: linear-gradient(145deg, #e6e6e6, #c0c0c0) !important;
        color: #222 !important;
        border: 2px solid #777 !important;
        border-radius: 8px !important;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.4), inset 1px 1px 2px rgba(255,255,255,0.5) !important;
        font-weight: bold;
        transition: all 0.1s ease;
    }
    .stButton>button:active {
        box-shadow: inset 3px 3px 6px rgba(0,0,0,0.6) !important;
        transform: translateY(2px);
    }
    .stButton>button:hover {
        background: linear-gradient(145deg, #f0f0f0, #d0d0d0) !important;
    }
</style>
""", unsafe_allow_stdio=True)

# --- Título e Logo ---
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown('<div style="font-size: 4rem; text-align: center;">🎓</div>', unsafe_allow_stdio=True)
with col2:
    st.title("MI Grade Calculator v1.0")

# --- Estrutura da Interface (3 Colunas) ---
col_setup, col_entry, col_results = st.columns([2, 3, 3])

# --- COLUNA 1: Setup ---
with col_setup:
    st.subheader("Setup")
    with st.container():
        st.markdown("**Unidades**")
        unidades = st.slider("", 1, 3, 2, help="Selecione o número de unidades concluídas (1-3).")
        st.write(f"Unidades definidas: **{unidades}**")

        st.markdown("---")
        st.markdown("**Calculation Mode**")
        # Botões físicos para o modo
        modo = st.radio("", ["Parcial (Até 2)", "Final (3)"], index=0 if unidades < 3 else 1, horizontal=True)

# --- COLUNA 2: Grade Entry ---
with col_entry:
    st.subheader("Grade Entry - Unit 1")
    notas_praticas = []
    notas_teoricas = []
    soma_mi = 0.0

    for i in range(unidades):
        with st.container():
            st.markdown(f"**Unidade {i+1}**")
            col_p, col_t = st.columns(2)
            with col_p:
                p = st.number_input(f"MI (Prática) {i+1}", min_value=0.0, max_value=10.0, value=8.0, step=0.1, key=f"p_{i}")
                notas_praticas.append(p)
            with col_t:
                t = st.number_input(f"Teórica {i+1}", min_value=0.0, max_value=10.0, value=6.5, step=0.1, key=f"t_{i}")
                notas_teoricas.append(t)
            
            # Cálculo instantâneo da unidade
            nota_unidade = (p * 0.7) + (t * 0.3)
            soma_mi += nota_unidade
            st.write(f"Nota Unidade {i+1}: **{nota_unidade:.2f}**")

# --- COLUNA 3: Results & Predictions ---
with col_results:
    st.subheader("Results & Predictions")
    with st.container():
        # Display LCD principal da média atual
        st.markdown("**Current MI Parcial**")
        media_parcial = soma_mi / unidades
        st.markdown(f'<div class="stDisplay">{media_parcial:.2f}</div>', unsafe_allow_stdio=True)

        if modo == "Parcial (Até 2)":
            st.markdown("---")
            # Previsões
            st.markdown("**Previsões (Média 7.0)**")
            pontos_passar = 21.0 - soma_mi
            unidades_rest = 3 - unidades

            if pontos_passar <= 0:
                st.success("🎯 Você já atingiu os pontos necessários para passar direto!")
            else:
                col_pre_p, col_gauge = st.columns([2, 1])
                with col_pre_p:
                    st.write(f"Points Needed: **{pontos_passar:.2f}**")
                    st.write(f"Next Unit Min. Avg: **{(pontos_passar/unidades_rest):.2f}**")
                with col_gauge:
                    # Simulação tátil do medidor
                    st.markdown(f'<div style="width: 80px; height: 80px; border-radius: 50%; border: 5px solid #555; background: #9ab39a; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; box-shadow: inset 3px 3px 5px rgba(0,0,0,0.5);">{(pontos_passar/unidades_rest):.1f}</div>', unsafe_allow_stdio=True)

            st.markdown("---")
            st.markdown("**Previsões (Média 3.0)**")
            pontos_final = 9.0 - soma_mi
            if pontos_final <= 0:
                st.info("🛡️ Você já garantiu no mínimo a ida para a Final.")
            else:
                st.write(f"Points Needed for Final: **{pontos_final:.2f}**")

        else: # Modo FINAL (3 Unidades)
            st.markdown("---")
            st.markdown("**STATUS FINAL**")
            if media_parcial >= 7.0:
                st.success(f"✅ APROVADO!🎉")
            elif media_parcial >= 3.0:
                st.warning(f"📚 FINAL. Foca nos estudos!")
            else:
                st.error(f"😔 PERDEU NO MI.")

    # Botão de Calcular (Estilo Tátil)
    st.markdown("---")
    if st.button("Calculate Units", type="primary"):
        st.balloons()
