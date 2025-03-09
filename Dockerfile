FROM python:3.9
ENV DISPLAY=:0

ADD generator.py .

RUN pip install pygame noise pygame_widgets

CMD ["python", "./generator.py"]