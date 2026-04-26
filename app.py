import streamlit as st
import re
import unicodedata

st.set_page_config(page_title="Radio SLB", page_icon="📻")

# LISTA NEGRA (Añade las palabras que quieras bloquear aquí)
BLOQUEADAS = ["palabra1", "palabra2", "sexo", "droga"] 

def blindar(texto):
    if not texto: return ""
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', texto.lower())

st.title("📻 Radio San Luis Beltrán")
st.subheader("Envía tu pedido musical")

with st.form("pedidos", clear_on_submit=True):
    nombre = st.text_input("Nombre:")
    curso = st.text_input("Curso:")
    artista = st.text_input("Artista:")
    cancion = st.text_input("Canción:")
    enviar = st.form_submit_button("Enviar a Cabina 🚀")

    if enviar:
        clean = blindar(artista + cancion)
        if any(p in clean for p in BLOQUEADAS):
            st.error("⚠️ Contenido no permitido.")
        else:
            st.success("✅ ¡Pedido enviado!")
            # Esto guarda los pedidos en un registro interno de la web
            st.write(f"Registro: {nombre} ({curso}) - {cancion}")
