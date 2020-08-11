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
Gerador de Quadro de Horários :books: :school:
====
<p> 
    Realiza o processo de criação de quadro de horários dentro de uma instituição de acordo com uma série de restrições implementadas que podem ser customizadas. A ferramenta é baseada em algoritmos genéticos e possui recursos para visualização de restrições violadas, gráfico de valores do melhor fitness do indivíduo a cada geração e importação de dados cadastrais a partir de arquivos .csv ou .json. Ao final da execução são exportados os quadros de horários do melhor indivíduo juntamente com o gráfico e o arquivo de informações adicionais.      
</p>

#### Vídeo Tutorial (Instalação e Execução). :point_down:

* https://youtu.be/eut2DwJIDP4

#### Vídeo Tutorial (Customização e Adição de Restrições). :point_down:

* https://youtu.be/KsAA7PJiZ6U

## Table of content
- [Iniciando...]
- [Depedências]
- [Variáveis de Ambiente]
- [Como Executar]
- [Exemplo Manual]
- [Gráfico Fitness]

## Iniciando...

Essas instruções fornecerão uma cópia do projeto em execução na sua máquina local para fins de desenvolvimento e teste.

### Depedências

Para compilar e executar a ferramenta você deve:

- Localizar requeriments.txt 
- Aplicar o comando pip3 install -r requeriments.txt

#### Variáveis de Ambiente

- SERVER_PORT=8080
- SERVER_HOST=0.0.0.0
- SERVER_DIRECTORY_SAVE=/home/osvaldoairon/


### Como Executar

  * First Step: Read Manual
         -> python3 main.py --man
         
### Exemplo Manual
![Screenshot](example_manual.png 'Manual')

### Gráfico Fitness

![Screenshot](grafico.jpg 'Gráfico')


