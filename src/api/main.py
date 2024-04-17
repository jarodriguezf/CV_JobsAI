import sys
sys.path.append('../../data/automation_scripts_data/')
sys.path.append('../modelling/')
from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fastapi import Request
from joblib import Memory
from automation_data_save import run_automation_save_data# type: ignore
from automation_cv_data_processing import run_processing_data_cv# type: ignore
from automation_job_data_processing import run_processing_data_job # type: ignore
from automation_scripts_model.automation_cv_modelling import run_automation_modelling_cv# type: ignore
from automation_scripts_model.automation_job_modelling import run_automation_modelling_job# type: ignore

# -- GUARDAR SCRIPTS EN CACHE --
cachedir = '/cache'
memory = Memory(cachedir, verbose=0)

run_processing_data_cv = memory.cache(run_processing_data_cv)
run_processing_data_job = memory.cache(run_processing_data_job)
run_automation_modelling_cv = memory.cache(run_automation_modelling_cv)
run_automation_modelling_job = memory.cache(run_automation_modelling_job)

# -- INICIO DE VARIABLES GLOBALES Y INSTANCIAS DE PROCESAMIENTO Y CARGA

# Instancia de FastAPI
app = FastAPI()

# Archivos estaticos (front)
app.mount("/static", StaticFiles(directory="static/landing_page"), name="static")

templates_landing = Jinja2Templates(directory="static/landing_page")
insert_data_template = Jinja2Templates(directory="static/insert-data-pages")
mostrar_cribar = Jinja2Templates(directory="static/show-similarities-page")


# Carga modelo y generar embeddings
def generate_embeddings():
    # Obtén los resultados almacenados en caché de run_processing_data_cv
    df_cv_processed, df_cv_raw = run_processing_data_cv(*load_txt('CV'))
    df_jobs_processed, _ = run_processing_data_job(*load_txt('Jobs'))

    embeddings_cv = run_automation_modelling_cv(df_cv_processed)
    embeddings_job= run_automation_modelling_job(df_jobs_processed)

    return embeddings_cv, embeddings_job, df_cv_raw

# -- INICIO DE ENDPOINTS --

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



# Endpoint para el botón de guardar datos
@app.post("/save-data/{data_type}")
async def save_data(data_type: str, data: bytes = Form(...), opcion: bytes = Form(...)):
    try:
        # Llamada al script de automatizacion del guardado de datos
        data_str = data.decode("utf-8")
        opcion_str = opcion.decode("utf-8")
  
        run_automation_save_data(data_str, data_type, opcion_str)
        return {"message": f"{data_type} guardado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Funcion para obtener los txt segun el tipo de dato (CV/Jobs)
def const_file_path(id_name):
    # Cargamos los txt de CVs
    file_paths = [f'../../data/raw_data/Data_{id_name}_SoftwareDeveloper.txt', 
                  f'../../data/raw_data/Data_{id_name}_NetworkEngineer.txt', 
                  f'../../data/raw_data/Data_{id_name}_IADeveloper.txt']
    return file_paths

# Abrimos los txt y almacenamos todos en el vector
def load_txt(id_name):
    raw_cvs = []
    for file_path in const_file_path(id_name):
        try:
            with open(file_path, encoding='utf-8') as f:
                raw_cvs.append(f.read())
        except IOError:
            print(f"Error: No se pudo abrir o leer el archivo {file_path}")
    return raw_cvs

# Cargamos datos y procesamos a html
def get_data(id_name, processing_function):
    try:
        # Llamamos al procesamiento de datos (retorna dos df, uno con los datos procesados semanticamente y otro en bruto)
        _, df_raw = processing_function(*load_txt(id_name))

        # Remover caracteres '\n' salto de lineas
        df_raw.iloc[:, 1] = df_raw.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))

        # Convertir el DataFrame a HTML
        html = df_raw.to_html(index=False)
        html = html.strip()
        html_encoded = html.encode('utf-8')
        return html_encoded # Retornamos a cliente para ser mostrado
    except Exception as e:
        print(f'Error. Se produjo un error al obtener los {id_name}')
        raise HTTPException(status_code=400, detail=str(e))



# Cargamos los datos de CV y convertimos a html
@app.get('/get-cvs')
async def get_all_cvs():   
    return get_data('CV', run_processing_data_cv)
   
    

# Cargamos los datos de Ofertas y convertimos a html
@app.get('/get-jobs')
async def get_all_jobs():
    return get_data('Jobs', run_processing_data_job)



# Funciones y endpoint para calcular la similitud de CVs para una oferta dada
def clean_df_original(df_cv):
    df_cv.iloc[:, 1] = df_cv.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))
    return df_cv 

def mean_embedding_job_id(id_job, embeddings_job):
    # Calcular la media de los embeddings
    mean_embedding_job = np.mean(embeddings_job[id_job], axis=0)
    return mean_embedding_job

def id_to_textCV(list_cv_id_simil, df_cvs):
    id_cv = [id_[0] for id_ in list_cv_id_simil]
    text_cv = df_cvs.loc[id_cv, 'cv']
    return text_cv

def insert_list_cosine_similarities(embeddings_cv, embedding_job):
    # Iteramos sobre todos los cv de nuestros embeddings, almacenando la similitud dada por la oferta pasada por parametro
    list_cosine_cv = []
    for cv in range(len(embeddings_cv)):
        # Calcular la media de los embeddings
        mean_embedding_cv = np.mean(embeddings_cv[cv], axis=0)
        list_cosine_cv.append(cosine_similarity([embedding_job], [mean_embedding_cv])[0, 0])
    return list_cosine_cv

def sorted_threshold_cv(list_cosine_cv, similarity):
    values_cv_threshold = sorted([[i,value] for i,value in enumerate(list_cosine_cv) if value >= similarity],
                                    key=lambda x: x[1], reverse=True)
    return values_cv_threshold

# Llamada al modelo (calcula y retorna el id con el texto de los cv mas similares)
@app.post('/call_model_to_similarities')
async def calculate_model(id: int = Form(...), similarity: float = Form(...)):
    try:
        # Generamos los embeddings correspondientes (ademas de el procesamiento de los df)
        embeddings_cv, embeddings_job, df_cv_raw=generate_embeddings()

        # retornamos el embedding de la oferta de trabajo con id dado
        embeddings_job=mean_embedding_job_id(id, embeddings_job)

        # Añadimos a una lista el calculo de las similitudes
        list_cosine_cv= insert_list_cosine_similarities(embeddings_cv, embeddings_job)

        # Almacenamos unicamente los cv cuya similitud sea mayor o igual al umbral dado por parametro, ordenado descendentemente
        values_cv_threshold= sorted_threshold_cv(list_cosine_cv, similarity)
    
        # Limpiamos los saltos de lineas '\n' de los dataframes originales (sin procesar previamente)
        df_cvs= clean_df_original(df_cv_raw)

        # Extraemos el texto correspondiente al id de los cv con el umbral retornado
        text_cv = id_to_textCV(values_cv_threshold, df_cvs)

        print('Longitud de cvs',len(text_cv))

        return [{"id": id, "cv": cv} for id, cv in text_cv.items()] # convertimos a array antes de pasar al front
    
    except Exception as e:
        print('Error. No se ha podido procesar correctamente el calculo de similitud.')
        raise HTTPException(status_code=400, detail=str(e))