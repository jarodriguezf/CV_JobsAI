import sys
sys.path.append('../../data/automation_scripts_data/')
from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from automation_data_save import run_automation_save_data

# Instancia de FastAPI
app = FastAPI()

# Archivos estaticos (front)
app.mount("/static", StaticFiles(directory="static/landing_page"), name="static")

templates_landing = Jinja2Templates(directory="static/landing_page")
insert_data_template = Jinja2Templates(directory="static/insert-data-pages")
mostrar_cribar = Jinja2Templates(directory="static/show-similarities-page")

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