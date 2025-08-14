FROM jupyter/pyspark-notebook:x86_64-spark-3.5.0

RUN pip install jupyterlab-execute-time
RUN pip install prophet
RUN pip install holidays
LABEL authors="Marcos Aurélio"

ENTRYPOINT ["start-notebook.sh", "--NotebookApp.token=''"]