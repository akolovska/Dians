FROM python:3.9-slim
WORKDIR /app
#COPY requirements.txt /app/
#RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]