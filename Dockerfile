FROM python:3.9-slim
RUN apt-get update && apt-get install -y libc-dev build-essential libatlas3-base libgfortran5
RUN pip install --upgrade pip setuptools wheel
ADD requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip pip install -v -r requirements.txt
COPY . .
CMD ["python", "TestConversation.py"]