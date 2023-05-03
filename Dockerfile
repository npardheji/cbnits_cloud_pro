FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY api /app/api
COPY policies /app/policies
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["api/app.py"]