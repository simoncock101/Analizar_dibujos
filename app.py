import base64
import streamlit as st
import numpy as np
from PIL import Image
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Boceto IA",
    page_icon="✏️",
    layout="wide"
)


# =========================================================
# ESTILO
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
}

.titulo {
    font-size: 40px;
    font-weight: 700;
    color: #202124;
}

.subtitulo {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 30px;
}

.seccion {
    font-size: 22px;
    font-weight: 700;
    color: #202124;
}

.descripcion {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 12px;
}

.info {
    background-color: #f1f3f4;
    border-radius: 12px;
    padding: 20px;
    color: #202124;
    margin-top: 15px;
    border: 1px solid #e0e0e0;
}

.info h4 {
    color: #202124;
    margin-top: 0;
}

.info p {
    color: #4b5563;
    margin: 8px 0;
}

.resultado {
    background-color: #f1f3f4;
    border-radius: 12px;
    padding: 20px;
    margin-top: 25px;
    color: #202124;
    border: 1px solid #e0e0e0;
}

.exito {
    background-color: #e8f5e9;
    color: #1b5e20;
    padding: 12px;
    border-radius: 8px;
    margin-top: 10px;
}

.error-clave {
    background-color: #ffebee;
    color: #b71c1c;
    padding: 12px;
    border-radius: 8px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown(
    '<div class="titulo">✏️ Boceto IA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">'
    'Dibuja una idea y deja que la inteligencia artificial la interprete.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Configuración")

    st.write(
        "Personaliza tu tablero antes de comenzar."
    )

    st.divider()

    stroke_width = st.slider(
        "Tamaño del pincel",
        1,
        20,
        5
    )

    stroke_color = st.color_picker(
        "Color del dibujo",
        "#222222"
    )

    st.divider()

    st.subheader("Ideas para dibujar")

    st.write("Una casa")
    st.write("Un celular")
    st.write("Un carro")
    st.write("Una silla")
    st.write("Un animal")
    st.write("Un objeto inventado")


# =========================================================
# COLUMNAS
# =========================================================

col1, col2 = st.columns(
    [1.1, 0.9],
    gap="large"
)


# =========================================================
# TABLERO
# =========================================================

with col1:

    st.markdown(
        '<div class="seccion">🎨 Tu boceto</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="descripcion">'
        'Dibuja cualquier objeto utilizando el mouse o trackpad.'
        '</div>',
        unsafe_allow_html=True
    )

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#FFFFFF",
        height=350,
        width=650,
        drawing_mode="freedraw",
        display_toolbar=True,
        key="canvas_boceto"
    )

    st.write("")

    analizar = st.button(
        "🔍 Interpretar boceto",
        type="primary"
    )


# =========================================================
# PANEL DERECHO
# =========================================================

with col2:

    st.markdown(
        '<div class="seccion">Análisis con IA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="descripcion">'
        'La inteligencia artificial analizará el dibujo.'
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # API KEY
    # -----------------------------------------------------

    api_key = st.text_input(
        "API Key",
        type="password",
        placeholder="sk-..."
    )

    # -----------------------------------------------------
    # BOTÓN VALIDAR
    # -----------------------------------------------------

    validar = st.button(
        "✓ Validar clave"
    )

    if validar:

        if not api_key.strip():

            st.error(
                "Primero ingresa una API Key."
            )

            st.session_state["clave_valida"] = False

        else:

            try:

                # Crear cliente con la clave ingresada
                cliente_validacion = OpenAI(
                    api_key=api_key.strip()
                )

                # Petición sencilla para comprobar autenticación
                cliente_validacion.models.list()

                st.session_state["clave_valida"] = True

                st.success(
                    "✓ La API Key es válida."
                )

            except Exception as e:

                st.session_state["clave_valida"] = False

                st.error(
                    "✗ La API Key no es válida."
                )

                st.caption(
                    str(e)
                )


    # -----------------------------------------------------
    # INFORMACIÓN
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="info">

        <h4>¿Qué hará la inteligencia artificial?</h4>

        <p>Identificará el objeto que dibujaste.</p>

        <p>Indicará qué tan segura es su interpretación.</p>

        <p>Describirá los elementos principales del dibujo.</p>

        <p>Propondrá tres posibles usos.</p>

        <p>Generará una idea creativa relacionada con el objeto.</p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FUNCIÓN BASE64
# =========================================================

def encode_image_to_base64(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# =========================================================
# ANALIZAR DIBUJO
# =========================================================

if analizar:

    if not api_key:

        st.warning(
            "Primero debes ingresar tu API Key."
        )

    else:

        with st.spinner(
            "La inteligencia artificial esta interpretando tu dibujo..."
        ):

            try:

                # -----------------------------------------
                # Crear cliente
                # -----------------------------------------

                client = OpenAI(
                    api_key=api_key.strip()
                )


                # -----------------------------------------
                # Convertir canvas en imagen
                # -----------------------------------------

                image_array = np.array(
                    canvas_result.image_data
                )

                image = Image.fromarray(
                    image_array.astype("uint8"),
                    "RGBA"
                )

                image_path = "boceto.png"

                image.save(
                    image_path
                )


                # -----------------------------------------
                # Convertir imagen a Base64
                # -----------------------------------------

                base64_image = encode_image_to_base64(
                    image_path
                )


                # -----------------------------------------
                # Prompt
                # -----------------------------------------

                prompt = """
Analyze the drawing made by the user.

The drawing can be simple, incomplete, or hand drawn.

Answer in Spanish using this structure:

OBJETO IDENTIFICADO:
Indica que objeto representa probablemente.

SEGURIDAD:
Indica Bajo, Medio o Alto.

DESCRIPCION:
Describe brevemente lo que observas.

POSIBLES USOS:
Propone 3 posibles usos para el objeto.

IDEA CREATIVA:
Propone una idea interesante relacionada con el objeto.

If the drawing is unclear, say so.
"""


                # -----------------------------------------
                # Solicitud a OpenAI
                # -----------------------------------------

                response = client.chat.completions.create(

                    model="gpt-4o-mini",

                    messages=[

                        {
                            "role": "user",

                            "content": [

                                {
                                    "type": "text",
                                    "text": prompt
                                },

                                {
                                    "type": "image_url",

                                    "image_url": {
                                        "url":
                                        f"data:image/png;base64,{base64_image}"
                                    }
                                }

                            ]

                        }

                    ],

                    max_tokens=500

                )


                # -----------------------------------------
                # Obtener respuesta
                # -----------------------------------------

                resultado = response.choices[
                    0
                ].message.content


                # -----------------------------------------
                # Mostrar resultado
                # -----------------------------------------

                st.markdown(
                    '<div class="resultado">',
                    unsafe_allow_html=True
                )

                st.subheader(
                    "Resultado del análisis"
                )

                st.write(
                    resultado
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    f"Ocurrió un error al analizar el dibujo: {e}"
                )


# =========================================================
# PIE DE PÁGINA
# =========================================================

st.divider()

st.caption(
    "Boceto IA · Interpretación de dibujos mediante inteligencia artificial"
)
