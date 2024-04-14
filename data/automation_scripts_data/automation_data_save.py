import re

# Constantes de categorias tanto para CV como ofertas de trabajo, rutas de guardado para CV y ofertas.
FILE_PATHS = {
    'software': '../../data/raw_data/Data_{id_name}_SoftwareDeveloper.txt',
    'ia': '../../data/raw_data/Data_{id_name}_IADeveloper.txt',
    'network': '../../data/raw_data/Data_{id_name}_NetworkEngineer.txt'
}
 
# Recorremos cada txt correspondiente a la ruta seleccionada y devolvemos id ultimo registro.
def insert_position_txt(filename, id_name):
    try:
        with open(filename, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
    except Exception as e:
        print(f"Error al leer el archivo {filename}: {e}")
        return None
    
    # Extraemos el id de cada registro
    numeros = re.findall(f'{id_name} (\d+)', contenido)
    if numeros:
        return int(numeros[-1]) # Obtenemos el ultido id
    else:
        print(f"No se encontraron números de {id_name} en el archivo.")
        return None
    
# Guarda los datos en funcion de si es una oferta o un cv. Además de la categoria de cada uno de ellos.
def save_data(data, id_name, categories):
    if not isinstance(id_name, str) or not isinstance(data, str):
        print('Error. Solo se puede introducir cadenas de texto')
    else:
        option_cv_job = id_name.lower()
        option_categories = categories.lower()

        # Comprobamos si el nombre de la oferta o cv es igual al pasado por parametros.
        # Comprobamos si la clave del FILE_PATHS es igual a las categorias elegidas en las opciones del menu
        if option_cv_job == id_name.lower() and option_categories in FILE_PATHS:

            #Contruimos el filename con el nombre correspondiente a la ruta elegida
            filename = FILE_PATHS[option_categories].format(id_name=id_name)

            position = insert_position_txt(filename, id_name)# funcion de calculo id ultimo registro
            if position is not None:
                position += 1
                try:
                    with open(filename, 'a', encoding='utf-8') as archivo:
                        archivo.write(f'\n\n\n{id_name} {str(position)}: {data}') # añadimos nuevos datos
                    print(f"Los datos se han añadido correctamente en {filename}")
                except Exception as e:
                    print(f"Error al añadir los datos en {filename}: {e}")
        else:
            print(f"Opción de {id_name} o categoría no válida.")

def run_automation_save_data(data, type, categories):
    save_data(data, type, categories) # Guarda Curriculums o ofertas de trabajo (CV/Jobs)