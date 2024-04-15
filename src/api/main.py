import sys
from io import BytesIO
sys.path.append('../../data/automation_scripts_data/')
from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt
from fastapi import Request
from automation_data_save import run_automation_save_data
from automation_cv_data_processing import run_processing_data_cv
from automation_job_data_processing import run_processing_data_job

# Instancia de FastAPI
app = FastAPI()

# Archivos estaticos (front)
app.mount("/static", StaticFiles(directory="static/landing_page"), name="static")

templates_landing = Jinja2Templates(directory="static/landing_page")
insert_data_template = Jinja2Templates(directory="static/insert-data-pages")
mostrar_cribar = Jinja2Templates(directory="static/show-similarities-page")

# Cargamos los txt de CVs
raw_cvs_SoftwareDev = open('../../data/raw_data/Data_CV_SoftwareDeveloper.txt',encoding='utf-8').read()
raw_cvs_NetworkEng = open('../../data/raw_data/Data_CV_NetworkEngineer.txt',encoding='utf-8').read()
raw_cvs_IADev= open('../../data/raw_data/Data_CV_IADeveloper.txt',encoding='utf-8').read()
# Cargamos los txt de Ofertas laborales
raw_jobs_SoftwareDev = open('../../data/raw_data/Data_Jobs_SoftwareDeveloper.txt',encoding='utf-8').read()
raw_jobs_NetworkEng = open('../../data/raw_data/Data_Jobs_NetworkEngineer.txt',encoding='utf-8').read()
raw_jobs_IADev= open('../../data/raw_data/Data_Jobs_IADeveloper.txt',encoding='utf-8').read()

# Carga de la landing page
@app.get("/")
async def root(request: Request):
    return templates_landing.TemplateResponse("index.html", {"request": request})


# Carga de pagina insercion de datos (a traves de "index.html")
@app.get("/insert-data")
async def home(request: Request):
    return insert_data_template.TemplateResponse("control_index.html", {"request": request})

# Carga de pagina mostrar informacion y criba (a traves de "control_index.html")
@app.get("/show-similarities")
async def home(request: Request):
    return mostrar_cribar.TemplateResponse("similarities.html", {"request": request})


# Endpoint para el botón de guardar CV
@app.post("/save-cv")
async def save_cv(data: bytes = Form(...), opcion: bytes = Form(...)):
    try:
        # Llamada al script de automatizacion del guardado de datos
        data_str = data.decode("utf-8")
        opcion_str = opcion.decode("utf-8")
  
        run_automation_save_data(data_str, 'CV',opcion_str)
        return {"message": "CV guardado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint para el botón de guardar oferta de trabajo
@app.post("/save-job-offer")
async def save_job_offer(data: bytes = Form(...), opcion: bytes = Form(...)):
    try:
        # Llamada al script de automatizacion del guardado de datos
        data_str = data.decode("utf-8")
        opcion_str = opcion.decode("utf-8")
       
        run_automation_save_data(data_str, 'Jobs',opcion_str)
        return {"message": "Oferta guardada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Cargamos los datos de CV y convertimos a html
@app.get('/get-cvs')
async def get_all_cvs():
    # Llamamos al procesamiento de datos (extraemos tanto un df con datos procesados como en bruto)
    _, df_cv_raw = run_processing_data_cv(raw_cvs_SoftwareDev, raw_cvs_NetworkEng, raw_cvs_IADev)
    
    # Remover caracteres '\n' salto de lineas
    df_cv_raw.iloc[:, 1] = df_cv_raw.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))

    # Convertir el DataFrame a HTML
    html = df_cv_raw.to_html(index=False)
    html = html.strip()
    html_encoded = html.encode('utf-8')
    return html_encoded


# Cargamos los datos de Ofertas y convertimos a html
@app.get('/get-jobs')
async def get_all_jobs():
    # Llamamos al procesamiento de datos (extraemos tanto un df con datos procesados como en bruto)
    _, df_jobs_raw = run_processing_data_job(raw_jobs_SoftwareDev, raw_jobs_NetworkEng, raw_jobs_IADev)
    
    # Remover caracteres '\n' salto de lineas
    df_jobs_raw.iloc[:, 1] = df_jobs_raw.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))

    # Convertir el DataFrame a HTML
    html = df_jobs_raw.to_html(index=False)
    html = html.strip()
    html_encoded = html.encode('utf-8')
    return html_encoded