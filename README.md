# Eventex

Sistema de Eventos

## Como desenvolver ?

1. Clone o repositório
2. Crie uma virtualenv com python 3.8
3. Ative o virtualenv
4. Instale as dependências
5. Configura a instância com o .env || settings.ini
6. Execute os testes

```console
git clone https://github.com/victorvf/welcome-to-the-django.git
cd wttd
python3 -m venv .env-wttd
source .env-wttd/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer o deploy ?

1. Crie uma instância no Heroku
2. Envie as configurações para o heroku
3. Defina uma SECRET_KEY segura para a instância
4. Defina DEBUG=False
5. Configure o serviço de Email
6. Envie o código para o Heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
# Configure o Email
git push heroku master --force
```
