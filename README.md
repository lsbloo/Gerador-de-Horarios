<!--
Copyright (c) 2020 Osvaldo Airon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->
Têmis
====

[![Documentation](https://img.shields.io/badge/docs-apache.org-blue.svg)](https://superset.incubator.apache.org)


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

