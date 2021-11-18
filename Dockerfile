FROM python:3.7

WORKDIR 

COPY requirements.txt ./req.txt

RUN pip3 install -r req.txt

EXPOSE 8501

COPY 

ENTRYPOINT ["streamlit","run"]

CMD ["app.py"]
