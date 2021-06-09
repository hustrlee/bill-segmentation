FROM python:3-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN pip3 install opencv-python -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN apt update
RUN apt install -y libgl1-mesa-glx

COPY . /usr/src/app

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["-m", "bill_segmentation"]