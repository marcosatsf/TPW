docker run -d -p 9999:8888 -p 4040:4040 -p 4041:4041 -v /mnt/c/Users/Marcos/Documents/dev/XPE/TPW/git_folder/TPW/environments/pyspark_env/workspace:/home/jovyan/work --network=custom_network  --name pyspark_jup jupyter/pyspark-notebook:x86_64-spark-3.5.0


