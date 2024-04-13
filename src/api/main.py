from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Instancia de FastAPI
app = FastAPI()

# Archivos estaticos (front)
app.mount("/static", StaticFiles(directory="static/landing_page"), name="static")
templates_landing = Jinja2Templates(directory="static/landing_page")
templates_home_control = Jinja2Templates(directory="static/home_templates")

# Carga de la landing page
@app.get("/")
async def root(request: Request):
    return templates_landing.TemplateResponse("index.html", {"request": request})

# Carga de pagina home_control (a traves de "index.html")
@app.get("/home")
async def home(request: Request):
    return templates_home_control.TemplateResponse("control_index.html", {"request": request})

# Endpoint para el botón de guardar CV
@app.post("/save-cv")
async def save_cv():
    # Aquí puedes agregar la lógica para guardar el CV
    return {"message": "CV guardado"}

# Endpoint para el botón de guardar oferta de trabajo
@app.post("/save-job-offer")
async def save_job_offer():
    # Aquí puedes agregar la lógica para guardar la oferta de trabajo y extraer los CVs
    return {"message": "Oferta de trabajo guardada y CVs extraídos"}