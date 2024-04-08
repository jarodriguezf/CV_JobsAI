import pandas as pd
import numpy as np
from transformers import AutoTokenizer, TFAutoModel

# Carga del modelo y tokenizador
model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModel.from_pretrained(model_name)

# Eliminamos salto caracter \n
def delete_line_break(df):
    df_copy = df.copy()
    df_copy.iloc[:, 1] = df_copy.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))
    return df_copy

# Iniciamos el proceso de carga y extraccion de los embeddings (correspondientes a todos las ofertas que tengamos)
def run_automation_modelling_job(data_job):
    # Eliminamos caracter '\n' salto de linea
    df_job=delete_line_break(data_job)
  
    # Tokenizamos los textos
    tokenized_inputs = tokenizer(df_job['job'].to_list(), padding=True, 
                                truncation=True, max_length=768, return_tensors="tf")
    
    # Extraemos el resultado en funcion de las representaciones de MiniLM
    outputs = model(tokenized_inputs)

    # Capturamos los embeddings
    embeddings = outputs.last_hidden_state

    # Normaliza los vectores de embedding para asegurarte de que tengan longitud unitaria
    normalized_embeddings_job = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return normalized_embeddings_job, df_job