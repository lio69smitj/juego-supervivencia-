import streamlit as st
import random

st.set_page_config(page_title="Oxide Mini Survival", layout="centered")

# --- INICIALIZACIÓN DE ESTADO ---
if 'hp' not in st.session_state:
    st.session_state.update({
        'hp': 100, 'dia': 1, 'comida': 5, 
        'madera': 0, 'piedra': 0, 'metal': 0,
        'lanza': False, 'pico': False, 'log': []
    })

def log(msg): st.session_state.log.insert(0, msg)

st.title("🛡️ Oxide: Mini Survival")

# --- ESTADÍSTICAS ---
st.progress(st.session_state.hp / 100)
col_stats = st.columns(4)
col_stats[0].metric("HP", f"{st.session_state.hp}")
col_stats[1].metric("Madera", st.session_state.madera)
col_stats[2].metric("Piedra", st.session_state.piedra)
col_stats[3].metric("Metal", st.session_state.metal)

# --- ACCIONES DE RECOLECCIÓN ---
st.subheader("⛏️ Recolección")
c1, c2, c3 = st.columns(3)

if c1.button("🌲 Talar"):
    cant = random.randint(3, 7)
    st.session_state.madera += cant
    log(f"Recogiste {cant} de madera.")
    st.rerun()

if c2.button("🪨 Picar Piedra"):
    cant = random.randint(2, 5)
    st.session_state.piedra += cant
    log(f"Picaste {cant} de piedra.")
    st.rerun()

if c3.button("🥫 Buscar Comida"):
    st.session_state.comida += random.randint(1, 3)
    log("Encontraste suministros.")
    st.rerun()

# --- SISTEMA DE CRAFTEO ---
st.subheader("🔨 Fabricación (Crafting)")
col_craft = st.columns(2)

if not st.session_state.lanza:
    if col_craft[0].button("🛠️ Lanza (10 Mad/5 Piedra)"):
        if st.session_state.madera >= 10 and st.session_state.piedra >= 5:
            st.session_state.madera -= 10
            st.session_state.piedra -= 5
            st.session_state.lanza = True
            log("¡Fabricaste una Lanza! (+ Defensa)")
            st.rerun()
        else: st.error("Faltan materiales")

# --- PASAR DÍA ---
st.divider()
if st.button("💤 PASAR NOCHE", use_container_width=True):
    st.session_state.dia += 1
    # Costo de hambre
    if st.session_state.comida > 0:
        st.session_state.comida -= 1
    else:
        st.session_state.hp -= 20
        log("⚠️ Hambriento. HP bajando.")
    
    # Ataque nocturno (PVP/Animales)
    if random.random() < 0.4:
        daño = random.randint(20, 40)
        if st.session_state.lanza:
            daño -= 15
            log("⚔️ Te defendiste con la lanza.")
        st.session_state.hp -= max(0, daño)
        log(f"💥 Te atacaron. Perdiste {daño} HP.")
    st.rerun()

# Historial
for m in st.session_state.log[:3]: st.caption(m)

if st.session_state.hp <= 0:
    st.error("FUISTE RAIDEADO (Moriste)")
    if st.button("Reiniciar"): st.session_state.clear(); st.rerun()
