# FrontPersonas

Aplicación web en **Streamlit** para consultar datos de personas por número de cédula usando autenticación JWT.

## Características

- Inicio de sesión contra API externa (`/auth/login`)
- Consulta por cédula (`/padron/{cedula}`)
- Estado de sesión con contador de vencimiento del token
- Historial de consultas recientes
- Vista de resultados con diseño responsive
- Expansor para ver respuesta JSON completa

## Requisitos

- Python 3.10+
- pip

## Instalación

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

La app abrirá en `http://localhost:8501`.

## Dependencias principales

- `streamlit`
- `requests`
- `streamlit-autorefresh`

## Estructura

```text
frontpersonas/
  app.py
  requirements.txt
  README.md
  .gitignore
```

## Notas

- La aplicación consume la API `https://personas-api.vercel.app`.
- No se expone el valor del token en la UI.
- Si cambias dependencias, actualiza `requirements.txt`.

## Licencia

Uso interno / privado (ajustar según necesidad).
