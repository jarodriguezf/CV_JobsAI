<h1 align='center'>CV & Jobs AI</h1>

![portada_cv_job](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/d8bade8c-18e2-4598-bff9-2a98e014eff1)

*El proposito de este proyecto es realizar un sistema de emparejamiento laboral (una oferta laboral se empareja con los curriculums mas aptos segun la descripcion aportada). La idea de realizar dicho proyecto es la mejora y aprendizaje de nuevas areas de la IA (NLP). Todo se ha realizado con objetivos didacticos, por tanto, no estamos ante un sistema profesional, ni tampoco con objetivos comerciales.*

##  Estructura del proyecto  📁
![estructura_proyecto](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/1c72e7ca-c4e6-4846-a6d7-7ec08260c8eb)

- data: Contiene todo referente a los datos, tanto en crudo como archivos de procesamiento.
    - automation_scripts_data: Contiene los scripts de procesamiento de datos (se llaman en varios notebooks como forma de automatizar las tareas de procesamiento).
    - exploratory_data: En esta carpeta se ha realizado el analisis eploratorio de los datos.
    - processed_data: Contiene los notebooks donde se realizo el procesamiento de datos (antes de automatizarlo). Esto nos permite aplicar alguna correcion o mejora antes de automatizar dicha tarea.
    - raw_data: Conjunto de datos (txt, datasets).
        - baseline_model: Modelo entrenado para la baseline.
        - datasets: Conjunto de datos limpios (procesado por los notebooks y usado sobretodo para probar el modelado antes de automatizarlo).
- src: Archivos del modelado y web.
    - api: Desarrollo de la web, tanto la api como el front-end.
    - baseline: Contiene la baseline como primer calculo de similitud entre las ofertas y los curriculums.
    - modelling: COntiene los notebook del modelado, tanto individualmente como la similitud final en 'similarities_cv_job.ipynb'.
        - automation_scripts_model: Scripts de automatizacion del modelo (tanto carga como configuracion del mismo).

## Dataset 📄

Todos los datos, tanto de curriculums como de oferta laborales han sido inventados. Por tanto no estamos ante datos reales (cualquier parecido con la realidad es pura coincidencia).

Se han organizado por tipos (CV/Jobs) y además, por categoria dentro de cada tipo (Software Developer, Network Engineer y IA Developer).

Como se puede ver, el proyecto en general esta enfocado en el sector tecnologico, por tanto los datos se han procesado para dicho fin.

## Tecnologias usadas 💻

- Python (pandas, sklearn, numpy, tensorflow, nltk, spacy).
- Huggingface (transformers).
- Git (Github flow).
- Librerias de visualizacion de datos (matplotlib).
- Lenguajes propios de web (html, bootstrap, javascript).

## Funcionamiento del aplicación 🚀

- Al abrir a la app lo primero que visitaremos será la landing page, donde se presenta el proyecto y el funcionamiento del sistema.
![landing_page_1](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/f1ccd57f-2ac7-449e-a109-a6dafee5ed72)

- Hacemos click en 'Empieza ya!' y nos redirigirá a la pagina para insertar nuevos datos. Podemos añadir los curriculums o ofertas que queramos (además de poder especificar el area laboral que guardemos: Software, IA o Network).
![insert_data_page](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/0d9f1c22-acf9-481b-af1c-daf64d7fe955)
![areas_laborales](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/094c2a7b-cf97-452f-8f3a-4fa9574069d9)

- En la seccion 'Cribar CV' podremos realizar tres funciones principales:

1. Mostrar los CVs guardados en el fichero.
![shows_cv](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/54d7ac0d-c80f-4edd-b64e-9f9a3ba3f607)

2. Mostrar las ofertas laborales guardadas en el fichero:
![shows_jobs](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/89e98ab6-6cc2-402d-a3ec-824e99df6cc7)

3. A partir del ID de una oferta laboral, calcular los CVs mas aptos (mostrados de manera descendente y ajustando el umbral de similitud).
![example_similarity](https://github.com/jarodriguezf/CV_JobsAI/assets/112967594/ede82f19-c106-4a66-9bd3-878dfd9a189f)

## Conclusión 🎉

Después de completar este proyecto de CV & Jobs AI, estoy satisfecho con el progreso logrado y el desarrollo de habilidades que ha implicado, desde la exploración de datos hasta la implementación del modelo.

Este proyecto, aunque principalmente un ejercicio de aprendizaje personal, ha resultado en la creación de una herramienta funcional que demuestra la comprensión de los conceptos clave de IA y NLP. 
