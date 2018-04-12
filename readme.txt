Trabalho  1 de Criptografia - Parte 1

Egon Nathan Bittencourt Araujo, GRR20142125
Marcela Ribeiro de Oliveira, GRR20157372

Ideia: Transformar o texto de entrada em uma imagem RGB.
Tamanho do bloco: 64 bytes.
Limitações: O texto que será cifrado é apenas caracteres do alfabeto maiúsculas
e minúsculas (52 letras) e números de 0 a 9. Sendo caracteres especiais como
(#, *, &, %,` ', `\n') excluídos. Caracteres com acento são substituídos por seu
respectivo caracter sem acento, por exemplo á será trocado para a, ã será
trocado para a. Além disso o caracter ç será trocado por c.

1) Chave
Consiste de uma matriz NxN, sendo 1 <= N <= 8, preenchida com valores K_{N,N}
sendo 1 <= K_{N,N} <= 255. Por exemplo
| 1 | 2 | 3 |
| 3 | 2 | 1 |
| 2 | 1 | 3 |.

2) Cifrador
O cifrador consiste nos seguintes passos:
a- Pegar blocos de 64 caracteres do texto claro, converter os caracteres usando
ASCII para decimal, e coloca-los numa matriz zerada de tamanho 8x8.

Exemplo:
abcd efghij klmnopq rst uvxwyz 1234567890

   ---->
ASCII char:
| a | b | c | d | e | f | g | h |
| i | j | k | l | m | n | o | p |
| q | r | s | t | u | v | x | w |
| y | z | 1 | 2 | 3 | 4 | 5 | 6 |
| 7 | 8 | 9 | 0 |0x0|0x0|0x0|0x0|
|0x0|0x0|0x0|0x0|0x0|0x0|0x0|0x0|
|0x0|0x0|0x0|0x0|0x0|0x0|0x0|0x0|
|0x0|0x0|0x0|0x0|0x0|0x0|0x0|0x0|

   ---->
Decimal:
| 97| 98| 99|100|101|102|103|104|
|105|106|107|108|109|110|111|112|
|113|114|115|116|117|118|119|120|
|121|122| 49| 50| 51| 52| 53| 54|
| 55| 56| 57| 48| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

b- Aplicar a chave como um estêncil, multiplicando cada valor da tabela pelo
valor da chave nas posições especificas. Caso parte da chave fique para fora
da tabela, esse passo é ignorado:

Exemplo:

| 97| 98| 99|100|101|102|103|104|   | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 |*3 |
|105|106|107|108|109|110|111|112|   | 3 | 2 | 1 | 3 | 2 | 1 | 3 | 2 |*1 |
|113|114|115|116|117|118|119|120|   | 2 | 1 | 3 | 2 | 1 | 3 | 2 | 1 |*3 |
|121|122| 49| 50| 51| 52| 53| 54|   | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 |*3 |
| 55| 56| 57| 48| 0 | 0 | 0 | 0 |   | 3 | 2 | 1 | 3 | 2 | 1 | 3 | 2 |*1 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |   | 2 | 1 | 3 | 2 | 1 | 3 | 2 | 1 |*3 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |   | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 |*3 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |   | 3 | 2 | 1 | 3 | 2 | 1 | 3 | 2 |*1 |
                                    |*2 |*1 |*3 |*2 |*1 |*3 |*2 |*1 |*3 |

PS. Os valores com asterisco não são utilizados nesse passo

| 97|196|297|100|202|306|103|208|
|315|212|107|324|218|110|333|224|
|226|114|345|232|117|354|238|120|
|121|244|147| 50|102|156| 53|108|
|165|112| 57|144| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

c- Montar imagem rgb seguindo a regra para cada elemento M_{i,j} da matriz.
Sendo as variaveis r_{i,j}, g_{i,j} e b_{i,j} valores inteiros:
r_{i,j} = M_{i,j} / 255 [Esse valor sempre é menor que 255]
g_{i,j} = M_{i,j} % 255
b_{i,j} = rand() % 255

Concatenar os blocos de imagem para cada bloco adicional, gerando assim uma
imagem em linha, com largura 8 e altura B*8 sendo B o numero de blocos.

Exemplo:

M_{0,0} = 97

r_{0,0} = 0
g_{0,0} = 97
b_{0,0} = 249 // RAND, não importante


3) Decifrador
O decifrador consiste nos seguintes passos:
a- Ler os canais de cor da imagem separadamente para cada pixel. Montar uma
matriz C a partir dos valores de cada pixel. Seguindo a regra abaixo:

C_{i,j} = (( r_{i,j} * 255 ) + g_{i,j} ) / K_{p,q}

Sendo K a chave e o índice (p,q) a posição relativa do estêncil durante a cifra.

b- Converter os valores obtidos para ASCII e concatená-los em uma string. O
texto claro não possuirá espaços nem caracteres especiais.


