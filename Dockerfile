FROM python:3.9.6-slim
LABEL authors="Kater_kcl"

COPY src /sarina/src
COPY requirements.txt /sarina
WORKDIR /sarina/src
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /sarina/requirements.txt

EXPOSE 1717

ENTRYPOINT ["gunicorn", "-k", "flask_sockets.worker", "-b", "0.0.0.0:1717", "main:app"]
