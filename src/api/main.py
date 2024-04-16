import sys
from io import BytesIO
sys.path.append('../../data/automation_scripts_data/')
sys.path.append('../modelling/')
from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fastapi import Request
from automation_data_save import run_automation_save_data# type: ignore
from automation_cv_data_processing import run_processing_data_cv# type: ignore
from automation_job_data_processing import run_processing_data_job # type: ignore
from automation_scripts_model.automation_cv_modelling import run_automation_modelling_cv# type: ignore
from automation_scripts_model.automation_job_modelling import run_automation_modelling_job# type: ignore
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

# Llamamos al procesamiento de datos (retorna dos df, uno con los datos procesados semanticamente y otro en bruto)
df_cv_processed, df_cv_raw = run_processing_data_cv(raw_cvs_SoftwareDev, raw_cvs_NetworkEng, raw_cvs_IADev)
df_jobs_processed, df_job_raw = run_processing_data_job(raw_jobs_SoftwareDev,raw_jobs_NetworkEng,raw_jobs_IADev)

# Carga modelo y generar embeddings
embeddings_cv = run_automation_modelling_cv(df_cv_processed)
embeddings_job= run_automation_modelling_job(df_jobs_processed)

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
    try:    
        # Remover caracteres '\n' salto de lineas
        df_cv_raw.iloc[:, 1] = df_cv_raw.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))

        # Convertir el DataFrame a HTML
        html = df_cv_raw.to_html(index=False)
        html = html.strip()
        html_encoded = html.encode('utf-8')
        return html_encoded # Retornamos a cliente para ser mostrado
    except Exception as e:
        print('Error. Se produjo un error al obtener los CVs')
        raise HTTPException(status_code=400, detail=str(e))
    


# Cargamos los datos de Ofertas y convertimos a html
@app.get('/get-jobs')
async def get_all_jobs():
    try:
        # Llamamos al procesamiento de datos (retorna dos df, uno con los datos procesados semanticamente y otro en bruto)
        # Usaremos el df en bruto (cuyo texto no ha sido procesado semanticamente)
        _, df_jobs_raw = run_processing_data_job(raw_jobs_SoftwareDev, raw_jobs_NetworkEng, raw_jobs_IADev)
        
        # Remover caracteres '\n' salto de lineas
        df_jobs_raw.iloc[:, 1] = df_jobs_raw.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))

        # Convertir el DataFrame a HTML
        html = df_jobs_raw.to_html(index=False)
        html = html.strip()
        html_encoded = html.encode('utf-8')
        return html_encoded # Retornamos a cliente para ser mostrado
    except Exception as e:
        print('Error. Se produjo un error al obtener las ofertas laborales')
        raise HTTPException(status_code=400, detail=str(e))

# Funciones y endpoint para calcular la similitud de CVs para una oferta dada
def clean_df_original(df_cv):
    df_cv.iloc[:, 1] = df_cv.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))
    #df_job.iloc[:, 1] = df_job.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))
    return df_cv #df_job

def mean_embedding_job_id(id_job):
    # Calcular la media de los embeddings
    mean_embedding_job = np.mean(embeddings_job[id_job], axis=0)
    return mean_embedding_job

def id_to_textCV(list_cv_id_simil, df_cvs):
    id_cv = [id_[0] for id_ in list_cv_id_simil]
    text_cv = df_cvs.loc[id_cv, 'cv']
    return text_cv

# Llamada al modelo (calcula y retorna el id con el texto de los cv mas similares)
@app.post('/call_model_to_similarities')
async def calculate_model(id: int = Form(...), similarity: float = Form(...)):
    try:
        # retornamos el embedding de la oferta de trabajo con id dado
        embedding_job=mean_embedding_job_id(id)

        # Iteramos sobre todos los cv de nuestros embeddings, almacenando la similitud dada por la oferta pasada por parametro
        list_cosine_cv = []
        for cv in range(len(embeddings_cv)):
            # Calcular la media de los embeddings
            mean_embedding_cv = np.mean(embeddings_cv[cv], axis=0)
            list_cosine_cv.append(cosine_similarity([embedding_job], [mean_embedding_cv])[0, 0])

        # Almacenamos unicamente los cv cuya similitud sea mayor o igual al umbral dado por parametro, ordenado descendentemente
        values_cv_threshold = sorted([[i,value] for i,value in enumerate(list_cosine_cv) if value >= similarity],
                                    key=lambda x: x[1], reverse=True)
        
        # Limpiamos los saltos de lineas '\n' de los dataframes originales (sin procesar previamente)
        df_cvs= clean_df_original(df_cv_raw)

        # Extraemos el texto correspondiente al id de los cv con el umbral retornado
        text_cv = id_to_textCV(values_cv_threshold, df_cvs)
        #text_job = df_jobs['job'][id]

        print('Longitud de cvs',len(text_cv))

        return [{"id": id, "cv": cv} for id, cv in text_cv.items()] # convertimos a array antes depasar al front
    except Exception as e:
        print('Error. No se ha podido procesar correctamente el calculo de similitud.')
        raise HTTPException(status_code=400, detail=str(e))