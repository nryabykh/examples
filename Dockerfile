FROM python:3.8

RUN mkdir -p /usr/src/asum/
WORKDIR /usr/src/asum/

COPY . /usr/src/asum/

ENV VIRTUAL_ENV=env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 9030

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]