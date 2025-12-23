import streamlit as st
import random

st.set_page_config(page_title="Supervivencia", layout="centered")

if 'hp' not in st.session_state:
    st.session_state.update({'hp': 100, 'dia': 1, 'comida': 3, 'madera': 0, 'log': []})

def log(msg): st.session_state.log.insert(0, msg)

st.title("🌲 Supervivencia")
st.progress(st.session_state.hp / 100)
st.write(f"❤️ Salud: {st.session_state.hp} | 🍎 Comida: {st.session_state.comida} | ☀️ Día: {st.session_state.dia}")

c1, c2 = st.columns(2)
if c1.button("🍎 Buscar Comida", use_container_width=True):
    encontrado = random.randint(1, 2)
    st.session_state.comida += encontrado
    log(f"Día {st.session_state.dia}: Encontraste {encontrado} de comida.")
    st.rerun()

if c2.button("💤 Dormir", use_container_width=True):
    st.session_state.dia += 1
    if st.session_state.comida > 0:
        st.session_state.comida -= 1
    else:
        st.session_state.hp -= 20
        log("⚠️ ¡Hambre! Perdiste salud.")
    if random.random() < 0.3:
        st.session_state.hp -= 15
        log("🐺 Un animal te atacó de noche.")
    st.rerun()

st.write("---")
for m in st.session_state.log[:3]: st.text(m)

if st.session_state.hp <= 0:
    st.error("GAME OVER")
    if st.button("Reiniciar"): st.session_state.clear(); st.rerun()

