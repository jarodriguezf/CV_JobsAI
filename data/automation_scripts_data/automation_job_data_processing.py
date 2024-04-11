import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Instancias de nltk
stop_words = set(stopwords.words('spanish'))
lemmatizer = WordNetLemmatizer()

# Division de categorias ofertas (software, network, IA)
def division_jobs(text):
    text_div =text.split('Jobs ')
    text_div=text_div[1:]# Elimina fila vacia
    return  text_div

# Fusionar categorias en un solo vector
def merge_jobs(first_text, second_text, third_text):
    merged_texts = []
    
    # Agregar a lista nueva los datos de los trees tipos de oferta
    merged_texts.extend(first_text)
    merged_texts.extend(second_text)
    merged_texts.extend(third_text)

    return merged_texts   

# Borramos numeros correspondiente a cada job ej. 1: Desarrollador,2: Ingeniero, etc.
def delete_numbersJobs (texts):
    new_texts = []
    for text in texts:
        # Revisar si primer caracter es un digito
        if text[0].isdigit():
            # Si son dos sigitos seguidos de : eliminamos los tres primeros caracteres
            if len(text) >= 3 and text[2] == ':':
                new_texts.append(text[4:])
            # Si es un digito seguido de :, eliminamos los dos primeros caracteres
            elif len(text) >= 2 and text[1] == ':':
                new_texts.append(text[3:])
            else:
                # Si el primer caracter es un digito pero no le sigue :, mantener texto original
                new_texts.append(text)
        else:
            # Si el primer caracter no es digito, mantener texto original
            new_texts.append(text)
    return new_texts

# Agregar ID a cada registro (puesto o job)
def set_id(texts):
    new_texts = [(id_, text) for id_, text in enumerate(texts)]
    return new_texts

def clean_texts(df):
    df_copy = df.copy()
    words_split = []
    # Separamos en palabras eliminando caracteres especiales
    for text in df_copy['job']:
        words = re.split(r'\W+', text)
        words = [word.lower() for word in words]
        words_split.append(words)
    # Eliminar ultimo elemento de words_split (es un elemento vacio)
    words_split = [words[:-1] for words in words_split]
    # Eliminar columna job y añadir nueva columna con tokens limpios
    df_copy.drop('job', axis=1, inplace=True)
    df_copy['job_tokens'] = words_split

    return df_copy

def clean_data(df):
    df_copy = df.copy()
    # Convertir las cadenas de texto a lista de token real (pasamos de ["[...]"] a [[]])
    #df_copy['job_tokens'] = df_copy['job_tokens'].apply(lambda x: ast.literal_eval(x))
    # Stopwords
    df_copy['job_tokens'] = df_copy['job_tokens'].apply(lambda tokens: [token for token in tokens if token not in stop_words])
    # Lematizacion de sustantivos
    df_copy['job_tokens'] = df_copy['job_tokens'].apply(lambda tokens: [lemmatizer.lemmatize(token, pos='n') for token in tokens])
    # Lematizacion de verbos
    df_copy['job_tokens'] = df_copy['job_tokens'].apply(lambda tokens: [lemmatizer.lemmatize(token, pos='v') for token in tokens])
    return df_copy

# Unimos tokens separados por espacios ' '
def join_tokens(df):
    df_copy = df.copy()

    df_copy['job_tokens'] = df_copy['job_tokens'].apply(lambda tokens: ' '.join(tokens))
    return df_copy


def run_processing_data_job(data_job_software, data_job_network, data_job_IA):
    print('--INICIANDO PROCESAMIENTO DE DATOS JOBS--')
    print('Analizando Jobs y extraccion de categorias...')
    div_job_SoftwareDev = division_jobs(data_job_software)
    div_job_NetworkEng= division_jobs(data_job_network)
    div_job_IADev=division_jobs(data_job_IA)
    print('Fusionando categorias procesadas...')
    merged_texts = merge_jobs(div_job_SoftwareDev, div_job_NetworkEng, div_job_IADev)
    print('Eliminando valores innecesarios...')
    merged_texts= delete_numbersJobs(merged_texts)
    print('Estableciendo id de posicion...')
    texts_ = set_id(merged_texts)
    print('Convirtiendo a Dataframe...')
    df_data = pd.DataFrame(texts_, columns=['id', 'job'])
    print('Limpieza inicial de datos...')
    df_clean = clean_texts(df_data)
    print('Limpieza semantica de datos...')
    df=clean_data(df_clean)
    print('Aplicando mejoras...')
    df = join_tokens(df)
    print('--FIN DEL PROCESAMIENTO--')
    return df, df_data