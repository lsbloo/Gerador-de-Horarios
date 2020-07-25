
## Table of content
- [Iniciando]
- [Dependencias](
- [Como Compilar]
- [Como Executar]

https://youtu.be/eut2DwJIDP4

## Iniciando

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Dependencias

Para a criação da aplicação e execução você deve primeiro instalar as dependencias:

Passo 1
- Encontre o diretorio env/bin
  * aplique: . activate
Passo 2
- Encontre o diretorio dependencies/requeriments.txt 
  * aplique o comando pip3 install -r requeriments.txt

#### Variaveis de Ambiente

- SERVER.PORT=8084
- SERVER.HOST=0.0.0.0
- SERVER_DIRECTORY_SAVE=/home/osvaldoairon/

#### Como Executar

- Encontre o arquivo initserver.py.
  * aplique python3 initserver.py
  * Ao final serão levantados 3 endpoints.
    0.0.0.0:8084/discipline (POST)
    0.0.0.0:8084/horario (POST)
    0.0.0.0:8084/sala (POST)
-  No diretorio dependencies/inputs/ ; cotém os 3 arquivos .json correspondentes aos endpoints, feito a população dos arquivos não sera necessario fazer novamente.

Por fim: python3 main.py ;]

