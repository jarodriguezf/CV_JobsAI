# Funciones comunes en la fase de modelado
import numpy as np
from transformers import AutoTokenizer, TFAutoModel

# Funcion que carga un modelo pasado por parametros, devolviendo el tokenizer propio y el modelo
def carga_modelo_tokenizer(nombre):
    model_name = nombre
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModel.from_pretrained(model_name)
    return tokenizer, model

# Funcion para eliminamos salto caracter '\n' en textos
def delete_line_break(df):
    df_copy = df.copy()
    df_copy.iloc[:, 1] = df_copy.iloc[:, 1].apply(lambda x: x.replace('\n', ' '))
    return df_copy