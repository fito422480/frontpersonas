import html
import json
from datetime import datetime, timedelta

import requests
import streamlit as st
try:
    from streamlit_autorefresh import st_autorefresh
except Exception:  # noqa: BLE001
    st_autorefresh = None


API_BASE = "https://personas-api.vercel.app/api"


st.set_page_config(
    page_title="Consulta | Personas",
    page_icon="ID",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg-main: #f2f5f8;
    --bg-card: #ffffff;
    --bg-soft: #eaf0f5;
    --text-main: #182430;
    --text-muted: #5d6d7d;
    --accent: #0f9d8a;
    --accent-2: #0e7490;
    --danger: #c0362c;
    --border: #d4dde6;
    --shadow: 0 14px 32px rgba(15, 28, 40, 0.08);
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif !important;
    color: var(--text-main);
}

.stApp {
    background:
      radial-gradient(circle at 92% 6%, rgba(14, 116, 144, 0.14) 0%, rgba(14, 116, 144, 0) 34%),
      radial-gradient(circle at 7% 14%, rgba(15, 157, 138, 0.18) 0%, rgba(15, 157, 138, 0) 30%),
      var(--bg-main);
}

#MainMenu, footer {
    visibility: hidden;
}

/* Keep Streamlit's sidebar toggle available */
header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fbfd 0%, #eef3f7 100%);
    border-right: 1px solid var(--border);
    min-width: 300px !important;
    max-width: 300px !important;
}

.hero {
    background: linear-gradient(120deg, #113b58 0%, #0f9d8a 65%, #7dcfb6 100%);
    color: #f9fdff;
    border-radius: 22px;
    padding: 1.4rem 1.8rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.2rem;
}

.hero-kicker {
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.92;
    font-weight: 700;
}

.hero h1 {
    margin: 0.3rem 0 0.5rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    line-height: 1.15;
    letter-spacing: -0.02em;
    color: #ffffff;
}

.hero p {
    margin: 0;
    max-width: 780px;
    opacity: 0.9;
    font-size: 0.95rem;
}

.section-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #3f5870;
    margin-top: 0.4rem;
    margin-bottom: 0.55rem;
    font-weight: 800;
}

.section-title::before {
    content: "";
    width: 20px;
    height: 4px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
}

.panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1rem 1rem 0.8rem;
    box-shadow: 0 8px 20px rgba(15, 28, 40, 0.05);
    margin-bottom: 0.95rem;
}

.person-card {
    background: linear-gradient(150deg, #ffffff 0%, #f2f9f7 100%);
    border: 1px solid var(--border);
    border-left: 6px solid var(--accent);
    border-radius: 18px;
    padding: 1.05rem 1.15rem;
    box-shadow: 0 10px 26px rgba(14, 116, 144, 0.08);
}

.person-name {
    margin: 0;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: -0.01em;
    font-size: 2rem;
    line-height: 1.15;
    word-break: break-word;
    color: #0f2436 !important;
}

.person-meta {
    margin-top: 0.45rem;
    font-size: 1rem;
    color: #425a72 !important;
}

.token-box {
    margin-top: 0.55rem;
    padding: 0.65rem 0.7rem;
    border: 1px dashed #a8c8d5;
    border-radius: 10px;
    background: #f2faf9;
    font-size: 0.72rem;
    color: #1a5567;
    word-break: break-all;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}

.small-note {
    color: var(--text-muted);
    font-size: 0.8rem;
}

/* Global readability fixes for light background */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #23384d;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #10283a;
}

h2.person-name {
    color: #0f2436 !important;
}

[data-testid="stWidgetLabel"] p {
    color: #2b4358 !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em;
}

.stTextInput input,
.stNumberInput input {
    color: #122a3f !important;
    font-weight: 600;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #6f8192 !important;
    opacity: 1 !important;
}

[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary span {
    color: #173a53 !important;
    font-weight: 700;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    background: #ffffff !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border: 1px solid var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(15, 157, 138, 0.14) !important;
}

div[data-testid="stFormSubmitButton"] > button,
.stButton > button {
    border-radius: 10px !important;
    border: 0 !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, var(--accent), var(--accent-2)) !important;
    color: #f7feff !important;
    transition: filter 0.15s ease, transform 0.12s ease;
}

div[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button:hover {
    filter: brightness(1.03);
    transform: translateY(-1px);
}

div[data-testid="stFormSubmitButton"] > button:disabled,
.stButton > button:disabled {
    background: #bfd7de !important;
    color: #f5fbff !important;
    cursor: not-allowed;
    transform: none;
}

.json-expander-gap {
    margin-top: 0.95rem;
}

.data-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 0.75rem;
    margin-top: 0.85rem;
}

.data-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.75rem 0.8rem;
    box-shadow: 0 4px 14px rgba(17, 59, 88, 0.06);
    min-height: 108px;
}

.data-label {
    margin: 0;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    color: #627689;
}

.data-value {
    margin: 0.32rem 0 0;
    font-size: 1.95rem;
    font-family: 'Space Grotesk', sans-serif;
    line-height: 1.1;
    letter-spacing: -0.015em;
    color: #162f44;
    word-break: break-word;
    overflow-wrap: anywhere;
}

.data-value--sm {
    font-size: 1.45rem;
}

@media (max-width: 900px) {
    .hero h1 {
        font-size: 1.45rem;
    }
    .person-name {
        font-size: 1.55rem;
    }
    .person-meta {
        font-size: 0.9rem;
    }
    .data-value {
        font-size: 1.35rem;
    }
    .data-value--sm {
        font-size: 1.15rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


if "token" not in st.session_state:
    st.session_state.token = None
if "token_exp" not in st.session_state:
    st.session_state.token_exp = None
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = None
if "search_cedula" not in st.session_state:
    st.session_state.search_cedula = ""


if st_autorefresh and st.session_state.get("token") and st.session_state.get("token_exp"):
    st_autorefresh(interval=1000, key="token_countdown_refresh")


def token_is_valid() -> bool:
    token = st.session_state.token
    exp = st.session_state.token_exp
    if not token:
        return False
    if exp and datetime.now() > exp:
        return False
    return True


def token_time_left_text() -> str:
    exp = st.session_state.token_exp
    if not exp:
        return "0m 0s"
    remaining = max(int((exp - datetime.now()).total_seconds()), 0)
    mins, secs = divmod(remaining, 60)
    return f"{mins}m {secs}s"


def format_date(date_str: str) -> str:
    if not date_str:
        return "-"
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return date_str
    months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    return f"{d.day} {months[d.month - 1]} {d.year}"


def do_login(sub: str, name: str) -> None:
    with st.spinner("Autenticando..."):
        try:
            response = requests.get(
                f"{API_BASE}/auth/login",
                params={"sub": sub, "name": name},
                timeout=12,
            )
            response.raise_for_status()
            data = response.json()
            st.session_state.token = data.get("access_token")
            st.session_state.token_exp = datetime.now() + timedelta(seconds=int(data.get("expires_in", 0)))
            st.success(f"Sesion iniciada como {name}. Token valido por {data.get('expires_in', 0) // 60} min.")
            st.rerun()
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar al servidor de autenticacion.")
        except requests.exceptions.HTTPError as err:
            status = err.response.status_code if err.response is not None else "-"
            st.error(f"Error HTTP en login: {status}.")
        except Exception as err:  # noqa: BLE001
            st.error(f"Error inesperado en login: {err}")


def fetch_person(cedula: str):
    try:
        response = requests.get(
            f"{API_BASE}/padron/{cedula}",
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=12,
        )

        if response.status_code == 404:
            return None, "Persona no encontrada en la busqueda.."
        if response.status_code == 401:
            return None, "Token invalido o expirado."

        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar al servidor."
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code if err.response is not None else "-"
        return None, f"Error HTTP al consultar: {status}."
    except Exception as err:  # noqa: BLE001
        return None, f"Error inesperado: {err}"


def register_history(cedula: str, person: dict) -> None:
    item = {
        "cedula": cedula,
        "nombre": person.get("nombresYApellido") or "Sin nombre",
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.history = [h for h in st.session_state.history if h["cedula"] != cedula]
    st.session_state.history.append(item)


def build_data_card(label: str, value: str, small: bool = False) -> str:
    size_class = " data-value--sm" if small else ""
    safe_label = html.escape(label)
    safe_value = html.escape(value or "-")
    return (
        "<div class='data-card'>"
        f"<p class='data-label'>{safe_label}</p>"
        f"<p class='data-value{size_class}'>{safe_value}</p>"
        "</div>"
    )


with st.sidebar:
    st.markdown("### Dashboard")
    st.caption("Panel de estado y accesos rapidos")

    if token_is_valid():
        st.success(f"Token activo ({token_time_left_text()})")
    else:
        st.error("Token inactivo")

    if st.button("Limpiar resultado", use_container_width=True):
        st.session_state.last_result = None
        st.rerun()

    st.markdown("---")
    st.markdown("#### Historial")
    if st.session_state.history:
        for item in st.session_state.history[-8:][::-1]:
            label = f"{item['cedula']} | {item['timestamp']}"
            if st.button(label, key=f"hist_{item['cedula']}", use_container_width=True):
                st.session_state.search_cedula = item["cedula"]
                st.rerun()
    else:
        st.caption("Todavia no hay consultas guardadas.")

st.markdown(
    """
<div class="hero">
  <div class="hero-kicker">Sistema de consulta</div>
  <h1>Consulta de Personas por Cedula</h1>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([0.95, 2.05], gap="medium")

with left:
    st.markdown("<div class='section-title'>Autenticacion</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=False):
        sub = st.text_input("Sub / Usuario", value="dev-user", placeholder="dev-user")
        name = st.text_input("Nombre", value="Adolfo", placeholder="Nombre de operador")
        login_submit = st.form_submit_button("Conectar", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if login_submit:
        if not sub.strip() or not name.strip():
            st.warning("Completa usuario y nombre para autenticar.")
        else:
            do_login(sub.strip(), name.strip())

    st.markdown("<div class='section-title'>Busqueda</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    with st.form("search_form", clear_on_submit=False):
        cedula_input = st.text_input(
            "Numero de Cedula",
            value=st.session_state.search_cedula,
            placeholder="Ej: 1234567",
        )
        search_submit = st.form_submit_button(
            "Buscar",
            type="primary",
            use_container_width=True,
            disabled=not token_is_valid(),
        )
    if not token_is_valid():
        st.info("Inicia sesion para habilitar la consulta.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-title'>Resultado</div>", unsafe_allow_html=True)

    if search_submit:
        query = (cedula_input or "").strip()
        if not query:
            st.warning("Ingresa un numero de cedula.")
        elif not query.isdigit():
            st.warning("La cedula debe contener solo numeros.")
        elif not token_is_valid():
            st.error("El token ya no es valido. Vuelve a autenticarte.")
        else:
            with st.spinner(f"Consultando cedula {query}..."):
                person, error = fetch_person(query)
            if error:
                st.error(error)
                st.session_state.last_result = None
            else:
                st.session_state.last_result = person
                st.session_state.last_query_time = datetime.now()
                st.session_state.search_cedula = query
                register_history(query, person)

    person = st.session_state.last_result
    if not person:
        st.markdown("<div class='panel'><span class='small-note'>No hay resultados para mostrar. Realiza una consulta para ver la ficha de la persona.</span></div>", unsafe_allow_html=True)
    else:
        full_name = person.get("nombresYApellido") or "-"
        cedula = person.get("cedula")
        sexo = person.get("sexo") or "-"
        sexo_text = "Femenino" if sexo == "F" else "Masculino" if sexo == "M" else sexo

        st.markdown("<div class='person-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='person-name'>{full_name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='person-meta'>Cedula: {cedula if cedula is not None else '-'} | Sexo: {sexo_text}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        when = st.session_state.last_query_time.strftime("%d/%m/%Y %H:%M") if st.session_state.last_query_time else "-"
        cards = [
            build_data_card("Fecha de nacimiento", format_date(person.get("fec_nac"))),
            build_data_card("Departamento", person.get("departamento_nombre") or "-"),
            build_data_card("Distrito", person.get("distrito_nombre") or "-"),
            build_data_card("Zona", person.get("zona_nombre") or "-"),
            build_data_card("Ultima consulta", when, small=True),
        ]
        st.markdown(f"<div class='data-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='json-expander-gap'></div>", unsafe_allow_html=True)
        with st.expander("Ver JSON completo"):
            st.code(json.dumps(person, ensure_ascii=False, indent=2), language="json")
