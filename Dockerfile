FROM python:3.11-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt

COPY store_locator /src/store_locator
CMD ["uvicorn", "store_locator.main:app", "--host", "0.0.0.0", "--port", "8000"]
