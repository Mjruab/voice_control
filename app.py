"""
🎙️ Control por Voz — Interfaces Multimodales
Tema amarillo pastel coherente con WordCloud Studio
"""

import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Control por Voz",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — tema amarillo pastel (igual a WordCloud Studio)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Fondo general */
.stApp { background-color: #fffde7; color: #333333; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #fff9c4 !important;
    border-right: 1px solid #f9a825;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f57f17 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}
[data-testid="stSidebar"] label {
    color: #4a5568 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* Inputs */
textarea, input[type="text"] {
    background-color: #fffff0 !important;
    border: 1px solid #f9a825 !important;
    border-radius: 6px !important;
    color: #111827 !important;
    font-size: 0.9rem !important;
}

/* Headings */
h1 {
    color: #f57f17 !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
}
h2, h3 { color: #e65100 !important; font-weight: 600 !important; }

/* Botón principal Streamlit */
.stButton > button {
    background: #f9a825 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.4rem !important;
    width: 100% !important;
    transition: background 0.2s ease !important;
}
.stButton > button:hover {
    background: #f57f17 !important;
    box-shadow: 0 2px 12px rgba(249,168,37,0.35) !important;
}

/* Métricas */
[data-testid="metric-container"] {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-top: 3px solid #f9a825;
    border-radius: 8px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(249,168,37,0.1);
}
[data-testid="metric-container"] label {
    color: #f57f17 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #333333 !important;
    font-weight: 700 !important;
    font-size: 1.55rem !important;
}

/* Alerts / info boxes */
[data-testid="stAlert"] {
    background: #fff8e1 !important;
    border: 1px solid #ffe082 !important;
    border-radius: 8px !important;
    color: #333333 !important;
}

/* Expander */
div[data-testid="stExpander"] {
    border: 1px solid #ffe082 !important;
    border-radius: 8px !important;
    background: #fff8e1 !important;
}

hr { border-color: #ffe082 !important; }

/* ── Botón Bokeh — tema dorado ── */
.bk-btn-type-warning,
.bk-btn {
    background: #f9a825 !important;
    color: #ffffff !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1.15rem !important;
    font-family: 'Inter', sans-serif !important;
    padding: 16px 40px !important;
    cursor: pointer !important;
    transition: background 0.2s ease !important;
    width: 100% !important;
    min-height: 54px !important;
}
.bk-btn-type-warning:hover,
.bk-btn:hover {
    background: #f57f17 !important;
    box-shadow: 0 3px 14px rgba(249,168,37,0.45) !important;
}
/* Eliminar fondo blanco del iframe y contenedores Bokeh */
.bk-toolbar-box, .bk, .bk-root, .bk-canvas {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}
iframe[title="streamlit_bokeh_events"] {
    background: transparent !important;
    border: none !important;
}
/* Selector genérico para iframes de componentes Streamlit */
[data-testid="stCustomComponentV1"] iframe,
.element-container iframe {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
/* Forzar fondo del body dentro del iframe vía atributo allowtransparency */
.streamlit-bokeh-events,
.streamlit-bokeh-events > *,
.streamlit-bokeh-events iframe {
    background: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* ── Componentes personalizados ── */

.header-card {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-left: 5px solid #f9a825;
    border-radius: 8px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 1px 6px rgba(249,168,37,0.12);
}

.section-card {
    background: #fff8e1;
    border: 1px solid #ffe082;
    border-radius: 8px;
    padding: 24px 28px;
    margin-bottom: 16px;
}

.msg-bubble {
    background: #fff9c4;
    border: 1px solid #f9a825;
    border-left: 4px solid #f57f17;
    border-radius: 8px;
    padding: 14px 20px;
    margin: 8px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.92rem;
    color: #333333;
}

.status-ok {
    background: #f0fdf4;
    border: 1px solid #86efac;
    border-left: 4px solid #22c55e;
    border-radius: 8px;
    padding: 12px 18px;
    margin: 8px 0;
    font-size: 0.88rem;
    color: #166534;
    font-weight: 500;
}

.status-err {
    background: #fff7ed;
    border: 1px solid #fdba74;
    border-left: 4px solid #f97316;
    border-radius: 8px;
    padding: 12px 18px;
    margin: 8px 0;
    font-size: 0.88rem;
    color: #9a3412;
    font-weight: 500;
}

.info-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 16px;
    background: #fffde7;
    border: 1px solid #ffe082;
    border-radius: 6px;
    margin-bottom: 8px;
}

.uso-tag {
    display: inline-block;
    background: #fff3cd;
    border: 1px solid #ffe082;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.85rem;
    font-weight: 500;
    color: #e65100;
    margin: 4px 3px;
}

.log-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    margin: 4px 0;
    background: #fffde7;
    border: 1px solid #ffe082;
    border-radius: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.84rem;
    color: #4a5568;
}
.log-ts {
    color: #f57f17;
    font-weight: 600;
    min-width: 80px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MQTT — callbacks
# ─────────────────────────────────────────────
message_received = ""

def on_publish(client, userdata, result):
    print("✅ Dato publicado vía MQTT\n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# ─────────────────────────────────────────────
# CONFIGURACIÓN MQTT (sidebar)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎙️ Control por Voz")
    st.divider()

    st.markdown("### CONFIGURACIÓN MQTT")
    broker = st.text_input("Broker:", value="broker.mqttdashboard.com")
    port   = st.number_input("Puerto:", value=1883, step=1, format="%d")
    topic  = st.text_input("Topic:", value="voice_ctrl")
    client_id = st.text_input("Client ID:", value="GIT-HUBC")

    st.divider()

    st.markdown("### OPCIONES DE VOZ")
    idioma_gtts = st.selectbox("Idioma gTTS:", ["es", "en", "fr", "pt", "de"])
    traducir    = st.checkbox("Traducir mensaje antes de publicar", value=False)
    if traducir:
        idioma_dest = st.selectbox("Traducir a:", ["en", "es", "fr", "pt", "de"])

    st.divider()

    st.markdown("### INFORMACIÓN")
    st.markdown(
        '<div class="info-item">'
        '<span style="font-size:1.1rem;">📡</span>'
        '<div><strong style="color:#e65100; font-size:0.85rem;">Broker activo</strong>'
        f'<p style="margin:2px 0 0 0; color:#6b7280; font-size:0.8rem;">{broker}:{port}</p></div>'
        '</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-item">'
        '<span style="font-size:1.1rem;">📢</span>'
        '<div><strong style="color:#e65100; font-size:0.85rem;">Topic de publicación</strong>'
        f'<p style="margin:2px 0 0 0; color:#6b7280; font-size:0.8rem;">{topic}</p></div>'
        '</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">🎙️ Control por Voz</h1>
    <p style="margin:6px 0 0 0; color:#f57f17; font-size:0.97rem;">
        Interfaces Multimodales — Reconocimiento de voz y publicación MQTT en tiempo real
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
col_izq, col_der = st.columns([3, 2], gap="large")

with col_izq:
    # ── Encabezado de sección (solo HTML cerrado) ────
    st.markdown("""
        <div class="section-card">
            <h3 style="margin:0 0 6px 0;">🎤 Reconocimiento de Voz</h3>
            <p style="color:#6b7280;font-size:0.9rem;margin:0;">
                Toca el botón y habla. El texto reconocido se publicará automáticamente al broker MQTT.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Inyectar CSS en el iframe de Bokeh para quitar el fondo blanco
    import streamlit.components.v1 as components
    components.html("""
        <script>
        document.body.style.background = 'transparent';
        document.documentElement.style.background = 'transparent';
        </script>
        <style>
            html, body { background: transparent !important; margin: 0; padding: 0; }
        </style>
    """, height=0)

    stt_button = Button(
        label="▶   Iniciar escucha",
        width=700,
        button_type="warning",
    )

    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
    """))

    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=90,
        debounce_time=0,
    )

    # ── Resultado de voz ───────────────────────
    if result and "GET_TEXT" in result:
        texto_voz = result.get("GET_TEXT").strip()

        st.markdown(
            f'<div class="section-card">'
            f'<h3 style="margin:0 0 10px 0;">💬 Texto Reconocido</h3>'
            f'<div class="msg-bubble">🎙️ &nbsp;<strong>{texto_voz}</strong></div>'
            f'</div>',
            unsafe_allow_html=True)

        # Traducción opcional
        if traducir:
            try:
                translator = Translator()
                traduccion = translator.translate(texto_voz, dest=idioma_dest).text
                st.markdown(
                    f'<div class="msg-bubble" style="border-color:#fbc02d;">'
                    f'🌐 &nbsp;<em>{traduccion}</em></div>',
                    unsafe_allow_html=True)
                texto_a_publicar = traduccion
            except Exception as e:
                st.markdown(
                    f'<div class="status-err">⚠️ Error al traducir: {e}</div>',
                    unsafe_allow_html=True)
                texto_a_publicar = texto_voz
        else:
            texto_a_publicar = texto_voz

        # Publicar MQTT
        try:
            client1 = paho.Client(client_id)
            client1.on_publish = on_publish
            client1.connect(broker, int(port))
            message_payload = json.dumps({"Act1": texto_a_publicar})
            ret = client1.publish(topic, message_payload)
            st.markdown(
                f'<div class="status-ok">✅ Publicado en <strong>{topic}</strong> '
                f'— código retorno: {ret.rc}</div>',
                unsafe_allow_html=True)
        except Exception as e:
            st.markdown(
                f'<div class="status-err">❌ Error MQTT: {e}</div>',
                unsafe_allow_html=True)

        # gTTS — audio de respuesta
        try:
            os.makedirs("temp", exist_ok=True)
            tts = gTTS(text=texto_a_publicar, lang=idioma_gtts)
            audio_path = "temp/respuesta.mp3"
            tts.save(audio_path)
            with open(audio_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
        except Exception as e:
            st.markdown(
                f'<div class="status-err">⚠️ No se pudo generar audio: {e}</div>',
                unsafe_allow_html=True)

        # Guardar en historial de sesión
        if "historial" not in st.session_state:
            st.session_state["historial"] = []
        st.session_state["historial"].append({
            "ts": time.strftime("%H:%M:%S"),
            "texto": texto_voz,
            "topic": topic,
        })

with col_der:
    # ── Instrucciones — bloque HTML completo y cerrado ────────
    pasos = [
        "Configura el broker y topic en el panel lateral.",
        "Haz clic en <strong>▶ Iniciar escucha</strong> y otorga permisos de micrófono.",
        "Habla claramente; el texto aparecerá al detectar silencio.",
        "El mensaje se publica automáticamente al broker MQTT.",
        "Activa <em>Traducir</em> para enviar el texto en otro idioma.",
    ]
    items_html = "".join([
        f'<div class="info-item">'
        f'<span style="background:#f9a825;color:#fff;border-radius:50%;width:22px;height:22px;'
        f'display:inline-flex;align-items:center;justify-content:center;font-size:0.75rem;'
        f'font-weight:700;flex-shrink:0;">{i}</span>'
        f'<span style="font-size:0.88rem;color:#4a5568;">{paso}</span>'
        f'</div>'
        for i, paso in enumerate(pasos, 1)
    ])
    st.markdown(
        f'<div class="section-card">'
        f'<h3 style="margin:0 0 12px 0;">📖 Instrucciones de uso</h3>'
        f'{items_html}'
        f'</div>',
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Aplicaciones — bloque HTML completo y cerrado ─────────
    casos = [
        "🤖 Robótica por voz", "🏠 Domótica inteligente",
        "♿ Accesibilidad", "🏭 Control industrial", "📱 IoT interactivo",
    ]
    tags_html = "".join([f'<span class="uso-tag">{c}</span>' for c in casos])
    st.markdown(
        f'<div class="section-card">'
        f'<h3 style="margin:0 0 12px 0;">💡 Aplicaciones</h3>'
        f'{tags_html}'
        f'</div>',
        unsafe_allow_html=True)


st.divider()
st.markdown(
    '<p style="text-align:center; color:#9ca3af; font-size:0.8rem; font-family:IBM Plex Mono,monospace;">'
    '🎙️ Control por Voz · Interfaces Multimodales · MQTT + gTTS + WebkitSpeechRecognition'
    '</p>', unsafe_allow_html=True)
