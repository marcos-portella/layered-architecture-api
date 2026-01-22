// Exemplo de de uso de var, let, const em JavaScript
const externo = "Olá, eu sou uma constante global!";

// Declaração de uma variável usando var
function exemploVar() {
    if (true) {
        var mensagem = "Olá, faculdade descomplica! Eu sou uma var...";
    }
    console.log(mensagem);  // em var console.log() pode ser usasdo fora do if
}

// Chamando a função exemploVar
exemploVar();

// Exemplo de erro e correção
var mensagem = "Olá, Faculdade Descomplica!" // Tem que ser definida no mesmo 
// escopo do console.log que a chamar
console.log(mensagem);

// Declaração de variável com let
 function exemploLet() {
    if (true) {
        let mensagem = "Olá, faculdade descomplica! Eu sou uma var...";
        console.log(mensagem);  // em let console.log() não pode ser usasdo 
        // fora do if
    }
 }

 // chamando o exemploLet
exemploLet();

// Exemplo de erro e correção
let mensagem2 = "Olá, Descomplica! Let externo!";
console.log(mensagem2);

function exemploConstante() {
    const mensagem = "Olá, Faculdade descomplica! Eu sou uma constante...";
    console.log(mensagem);
}

// Chamando a  função exemploConst
exemploConstante();

// Exemplo externo de const
console.log(externo);

// Tipos de comentários

// Uma linha

/* 
Várias linhas
*/

/**
 * Subtari o segundo número do primeiro.
 * 
 * @param {} a - O número do qual subitrair.
 * @param {} b - O número a ser subtraido.
 * @return {} - O resultado da subtração.
 * 
 * @example
 * //Exemplo de uso:
 * let resultado = subtrair(10,4);
 * console.log(resultado); // 6
 */
function subtrair(a, b) {
    return a - b;
}