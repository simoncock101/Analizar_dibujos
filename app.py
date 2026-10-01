import base64
import html
import streamlit as st
import numpy as np
from PIL import Image
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas


# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------

st.set_page_config(
    page_title="Boceto IA",
    page_icon="✏️",
    layout="wide"
)


# ---------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
}

/* Título principal */
.titulo {
    font-size: 40px;
    font-weight: 700;
    color: #202124 !important;
}

/* Subtítulo */
.subtitulo {
    font-size: 17px;
    color: #6b7280 !important;
    margin-bottom: 30px;
}

/* Títulos de sección */
.seccion {
    font-size: 22px;
    font-weight: 700;
    color: #202124 !important;
}

/* Texto descriptivo */
.descripcion {
    font-size: 14px;
    color: #6b7280 !important;
    margin-bottom: 12px;
}


/* ---------------------------------------------------------
   TARJETA DE INFORMACIÓN
   --------------------------------------------------------- */

.info {
    background-color: #f1f3f4;
    border-radius: 12px;
    padding: 20px;
    color: #202124 !important;
    margin-top: 15px;
    border: 1px solid #e0e0e0;
}

.info h4 {
    color: #202124 !important;
    margin-top: 0;
}

.info p {
    color: #4b5563 !important;
    margin: 8px 0;
}


/* ---------------------------------------------------------
   RESULTADO
   --------------------------------------------------------- */

.resultado {
    background-color: #f5f6f7;
    border-radius: 12px;
    padding: 22px;
    margin-top: 25px;
    border: 1px solid #d9dce1;
}

.resultado-titulo {
    color: #202124 !important;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 18px;
}

.texto-resultado {
    color: #202124 !important;
    font-size: 15px;
    line-height: 1.7;
}

.texto-resultado strong {
    color: #111827 !important;
}


/* ---------------------------------------------------------
   ESTADO DE LA API KEY
   --------------------------------------------------------- */

.estado-exito {
    background-color: #e8f5e9;
    color: #1b5e20 !important;
    padding: 10px 14px;
    border-radius: 8px;
    margin-top: 10px;
    border: 1px solid #c8e6c9;
}

.estado-error {
    background-color: #ffebee;
    color: #b71c1c !important;
    padding: 10px 14px;
    border-radius: 8px;
    margin-top: 10px;
    border: 1px solid #ffcdd2;
}


/* ---------------------------------------------------------
   SIDEBAR
   --------------------------------------------------------- */

[data-testid="stSidebar"] {
    background-color: #252630;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}


/* ---------------------------------------------------------
   BOTÓN PRINCIPAL
   --------------------------------------------------------- */

div.stButton > button[kind="primary"] {
    background-color: #ff4b4b;
    border: none;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 18px;
}

div.stButton > button[kind="primary"]:hover {
    background-color: #e63e3e;
}


/* ---------------------------------------------------------
   INPUT DE API KEY
   --------------------------------------------------------- */

div[data-testid="stTextInput"] label {
    color: #202124 !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "clave_valida" not in st.session_state:
    st.session_state["clave_valida"] = False

if "clave_validada" not in st.session_state:
    st.session_state["clave_validada"] = ""


# ---------------------------------------------------------
# TÍTULO
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# COLUMNAS PRINCIPALES
# ---------------------------------------------------------

col1, col2 = st.columns(
    [1.1, 0.9],
    gap="large"
)


# =========================================================
# COLUMNA IZQUIERDA
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


    # -----------------------------------------------------
    # CANVAS
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # BOTÓN INTERPRETAR
    # -----------------------------------------------------

    analizar = st.button(
        "🔍 Interpretar boceto",
        type="primary"
    )


# =========================================================
# COLUMNA DERECHA
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
    # SI EL USUARIO CAMBIA LA CLAVE,
    # VOLVEMOS A PEDIR VALIDACIÓN
    # -----------------------------------------------------

    if api_key.strip() != st.session_state["clave_validada"]:

        st.session_state["clave_valida"] = False


    # -----------------------------------------------------
    # BOTÓN VALIDAR
    # -----------------------------------------------------

    validar = st.button(
        "✓ Validar clave"
    )


    if validar:

        if not api_key.strip():

            st.session_state["clave_valida"] = False

            st.error(
                "Primero ingresa una API Key."
            )

        else:

            try:

                cliente_validacion = OpenAI(
                    api_key=api_key.strip()
                )

                # Comprobamos que la API Key funcione
                cliente_validacion.models.list()


                st.session_state["clave_valida"] = True

                st.session_state["clave_validada"] = api_key.strip()


                st.markdown(
                    """
                    <div class="estado-exito">
                        ✓ La API Key es válida y está lista para utilizarse.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.session_state["clave_valida"] = False

                st.session_state["clave_validada"] = ""


                st.markdown(
                    """
                    <div class="estado-error">
                        ✗ La API Key no es válida o no está disponible.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.caption(str(e))


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


# ---------------------------------------------------------
# FUNCIÓN PARA CONVERTIR IMAGEN A BASE64
# ---------------------------------------------------------

def encode_image_to_base64(image_path):

    with open(image_path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


# =========================================================
# ANÁLISIS DEL BOCETO
# =========================================================

if analizar:

    # -----------------------------------------------------
    # COMPROBAR API KEY
    # -----------------------------------------------------

    if not api_key.strip():

        st.warning(
            "Primero debes ingresar una API Key."
        )


    elif not st.session_state.get(
        "clave_valida",
        False
    ):

        st.warning(
            "Primero debes validar la API Key."
        )


    else:

        with st.spinner(
            "La inteligencia artificial está interpretando tu dibujo..."
        ):

            try:

                # -------------------------------------------------
                # CONECTAR CON OPENAI
                # -------------------------------------------------

                client = OpenAI(
                    api_key=api_key.strip()
                )


                # -------------------------------------------------
                # OBTENER IMAGEN DEL CANVAS
                # -------------------------------------------------

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


                # -------------------------------------------------
                # CONVERTIR IMAGEN A BASE64
                # -------------------------------------------------

                base64_image = encode_image_to_base64(
                    image_path
                )


                # -------------------------------------------------
                # PROMPT
                # -------------------------------------------------

                prompt = """
Analiza el dibujo realizado por el usuario.

El dibujo puede ser simple, incompleto o estar hecho a mano.

Responde en español siguiendo exactamente esta estructura:

OBJETO IDENTIFICADO:
Indica qué objeto representa probablemente.

SEGURIDAD:
Indica Bajo, Medio o Alto.

DESCRIPCIÓN:
Describe brevemente lo que observas en el dibujo.

POSIBLES USOS:
Propón 3 posibles usos para el objeto.

IDEA CREATIVA:
Propón una idea interesante relacionada con el objeto.

Si el dibujo no es claro, indícalo.
"""


                # -------------------------------------------------
                # SOLICITAR ANÁLISIS
                # -------------------------------------------------

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


                # -------------------------------------------------
                # OBTENER RESULTADO
                # -------------------------------------------------

                resultado = response.choices[0].message.content


                # -------------------------------------------------
                # PROTEGER EL TEXTO PARA HTML
                # -------------------------------------------------

                resultado_seguro = html.escape(
                    resultado
                )


                resultado_seguro = (
                    resultado_seguro
                    .replace(
                        "\n",
                        "<br>"
                    )
                )


                # -------------------------------------------------
                # MOSTRAR RESULTADO
                # -------------------------------------------------

                st.markdown(
                    f"""
                    <div class="resultado">

                        <div class="resultado-titulo">
                            Resultado del análisis
                        </div>

                        <div class="texto-resultado">
                            {resultado_seguro}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -----------------------------------------------------
            # MANEJO DE ERRORES
            # -----------------------------------------------------

            except Exception as e:

                st.error(
                    f"Ocurrió un error al analizar el dibujo: {e}"
                )


# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------

st.divider()

st.caption(
    "Boceto IA · Interpretación de dibujos mediante inteligencia artificial"
)
