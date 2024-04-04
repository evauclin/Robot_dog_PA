#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

RUN apt update &&  apt install -y cmake g++ wget unzip
RUN apt install libopencv-dev -y
RUN dpkg -l libopencv-dev



#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]