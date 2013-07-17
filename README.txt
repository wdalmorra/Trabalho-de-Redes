## Universidade Federal de Pelotas
##
## Centro de Desenvolvimento Tecnológico
##
## Bacharelado em Ciência da Computação
##
## Redes de computadores
##
## Trabalho de Redes de Computadores
##
## Webcrawler
##
## Integrantes:
## Thainan Bystronski Remboski
## Lucas Mendonça de Souza Xavier
## William Dalmorra de Souza
## Alvaro Joan Gonçalves dos Santos


- Linguagem -
Este trabalho foi desenvolvido utilizando a linguagem de programação Python 2.7.3.


- Sistema -
Trabalho desenvolvido no sistema operacional Linux, distribuição Ubuntu, versões 12.04 (32 bits) e 13.04 (64 bits).


- Execução -
Para executar o webcrawler, basta executar o arquivo executeme, onde existe uma configuração exemplo que roda o seguinte comando:

python webcrawler.py 2 <site>

Ou, para escolher as opções manualmente, basta abrir o terminal na pasta do programa e escrever o seguinte comando:

python webcrawler.py <profundidade> <url>


- Usando o makefile -
O arquivo makefile foi criado à fim de facilitar o trabalho de deletar as pastas e arquivos que foram baixados pelo webcrawler.
Ele contem um simples comando que deleta a pasta "webcrawler-output", para usá-lo basta apenas entrar pelo terminal na pasta do webcrawler onde se encontra o makefile e digitar:

make clean


- Implementação e testes -
São recebidas uma profundidade e uma URL por linha de comando, sendo esta última colocada em uma fila, aguardando processamento. Para cada URL da fila, é realizada uma requisição HTTP, o código HTML (ou o arquivo de formato diverso especificado) é baixado e salvado dentro da pasta "webcrawler-output", e, em seguida, pesquisado por tags <a href>. Cada URL encontrada é colocada na fila da mesma forma que a URL inicial. O processo continua até que a profundidade da busca seja igual a profundidade especificada pela linha de comando.

A cada nível de profundidade atingido pela busca, uma série de threads é lançada. Cada thread busca URLs continuamente na fila dos arquivos ainda não solicitados até que o nível tenha sido completamente pesquisado. A fila é única e é acessada de forma bloqueante, bem como a lista de URLs já visitadas.

Antes de realizar a requisição HTTP para baixar o código HTML, é realizada uma pesquisa no arquivo "robots.txt" da página, onde os link encontrados são ingorados na pesquisa.

Após realização de testes, verificou-se melhor desempenho ao colocar as URLs já visitadas em uma estrutura de dados (lista), para não fazer consultas a uma URL já visitada.
