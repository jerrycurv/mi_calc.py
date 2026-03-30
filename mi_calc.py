import streamlit as st

# Configuração focada em mobile (layout centrado)
st.set_page_config(page_title="Calculadora MI", page_icon="📱", layout="centered")

# CSS Minimalista para destacar os resultados
st.markdown("""
<style>
    .status-aprovado { color: #15803d; font-weight: bold; font-size: 1.2rem; background-color: #dcfce7; padding: 10px; border-radius: 8px; text-align: center;}
    .status-final { color: #b45309; font-weight: bold; font-size: 1.2rem; background-color: #fef3c7; padding: 10px; border-radius: 8px; text-align: center;}
    .status-perdeu { color: #b91c1c; font-weight: bold; font-size: 1.2rem; background-color: #fee2e2; padding: 10px; border-radius: 8px; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Calculadora de MI")
st.markdown("Descubra sua média do Módulo Interdisciplinar de forma rápida e direta.")

# 1. Simplificação: O usuário só escolhe quantas notas já tem.
unidades_concluidas = st.radio(
    "Quantas unidades você já concluiu?",
    options=[1, 2, 3],
    horizontal=True
)

st.divider()

notas = []
soma_mi = 0.0

# 2. Coleta de Notas (Design limpo, colunas se empilham no mobile)
st.subheader("📝 Suas Notas")

for i in range(unidades_concluidas):
    st.markdown(f"**Unidade {i+1}**")
    col1, col2 = st.columns(2)
    
    with col1:
        pratica = st.number_input(f"MI (Prática 70%) - U{i+1}", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key=f"p_{i}")
    with col2:
        teorica = st.number_input(f"Teórica (30%) - U{i+1}", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key=f"t_{i}")
    
    nota_unidade = (pratica * 0.7) + (teorica * 0.3)
    soma_mi += nota_unidade
    notas.append(nota_unidade)
    
    st.caption(f"Nota final da Unidade {i+1}: **{nota_unidade:.2f}**")
    st.write("") # Pequeno espaço

st.divider()

# 3. Resultados Diretos ao Ponto
st.subheader("📊 Resultado")

if unidades_concluidas == 3:
    media_final = soma_mi / 3
    st.metric(label="Sua Média Final", value=f"{media_final:.2f}")
    
    if media_final >= 7.0:
        st.markdown('<div class="status-aprovado">✅ APROVADO! Parabéns, passou direto!</div>', unsafe_allow_html=True)
        st.balloons()
    elif media_final >= 3.0:
        st.markdown('<div class="status-final">⚠️ FINAL. Você tem chance, foca nos estudos!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-perdeu">❌ PERDEU NO MI. Não desanime, força na próxima!</div>', unsafe_allow_html=True)
else:
    media_parcial = soma_mi / unidades_concluidas
    st.metric(label="Sua Média Parcial Atual", value=f"{media_parcial:.2f}")
    
    pontos_para_passar = 21.0 - soma_mi
    pontos_para_final = 9.0 - soma_mi
    unidades_restantes = 3 - unidades_concluidas
    
    st.markdown("**Projeção para os próximos passos:**")
    
    # Lógica para Passar Direto
    if pontos_para_passar <= 0:
        st.success("🎯 Você já tem pontos para passar direto! (Basta não zerar o resto).")
    else:
        media_necessaria = pontos_para_passar / unidades_restantes
        if media_necessaria > 10:
            st.error(f"📈 Para passar direto: Matematicamente impossível (precisaria de média {media_necessaria:.2f}).")
        else:
            st.info(f"🎯 Para passar direto: Faltam **{pontos_para_passar:.2f}** pontos (Média de **{media_necessaria:.2f}** nas próximas {unidades_restantes} unidades).")
            
    # Lógica para Ir para a Final
    if pontos_para_final <= 0:
        st.success("🛡️ Você já garantiu, no mínimo, a ida para a Final.")
    else:
        media_final_necessaria = pontos_para_final / unidades_restantes
        if media_final_necessaria > 10:
             st.error(f"📉 Para ir para a final: Matematicamente impossível (precisaria de média {media_final_necessaria:.2f}).")
        else:
            st.warning(f"⚠️ Para ir para a Final: Faltam **{pontos_para_final:.2f}** pontos (Média de **{media_final_necessaria:.2f}** nas próximas {unidades_restantes} unidades).")
