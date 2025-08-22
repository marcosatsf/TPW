FROM jupyter/pyspark-notebook:x86_64-spark-3.5.0

RUN pip install jupyterlab-execute-time
RUN pip install prophet==1.1.7
RUN pip install psycopg2-binary==2.9.10
LABEL authors="Marcos Aurélio"

ENTRYPOINT ["start-notebook.sh", "--NotebookApp.token=''"]