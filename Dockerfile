FROM python:3.9

# diretório de trabalho
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copia todo o conteúdo do diretório atual para o diretório de trabalho
COPY . .

# Define as variáveis de ambiente necessárias
ENV DJANGO_SETTINGS_MODULE=e_learning.settings
#saída exibida imediatamente.
ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate

# Defina o comando padrão para iniciar o servidor Django
CMD python manage.py test -v2 --failfast && python manage.py runserver 0.0.0.0:8000
