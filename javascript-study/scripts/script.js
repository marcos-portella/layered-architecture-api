// Definindo outra função regular com dois parâmetros
function soma(a, b) {
  return a + b;
}

// Chamando a função soma e armazenando o resultado em uma variável
let resultado = soma(13, 29);

// Exibindo o resultado da função soma
console.log("O resultado da soma é: " + resultado);

// Definindo uma função regular usando a palavra-chave 'function'
function saudacao(nome) {
  console.log("Olá " + nome);
}

// Chamando a função saudacao e passando um argumento
saudacao("Ana teixeira");

// Definindo uma função regular sem parâmetros e sem retorno
function mensagem() {
  console.log("Esta é uma mensagem de boass vindas");
}

// Chamando a função mensagem
mensagem();

// Declaração de uma variável chamada resultado e atribuição de uma função anônima a ela

let somarParametros = function (parametro1, parametro2) {
  console.log("Parâmetro 1: " + parametro1);
  console.log("Parâmetro 2: " + parametro2);

  let resultado = parametro1 + parametro2;

  console.log("Resultado: " + resultado);

  return resultado;
};

// Chamada da função anônima através da variável
let resultado2 = somarParametros(5, 10);
console.log("Resultado da chamada da função somarParametros: " + resultado2);

// Definindo uma função que aceita outra função como argumento
function executarFuncao(funcao, valor1, valor2) {
  console.log("\nExecutando a função passada como argumento: ");
  return funcao(valor1, valor2);
}

// Passando a função anônima como argumento para outra função
let resultadoExecucao = executarFuncao(somarParametros, 7, 3);
console.log(
  "Resultado da execução da função passada como argumento: " +
    resultadoExecucao,
);

// Definindo e chamando uma função anônima imediatamente
let resultadoImediato = (function (a, b) {
  console.log("\nFunção de chamada imediata: ");
  return a * b;
})(4, 6);
console.log(
  "Resultado da função anônima chamada imediatamente: " + resultadoImediato,
);

// Arrow functions

// Exemplo básico de uma arrow function que soma dois números
let somar = (a, b) => {
  return a + b;
};

// Chamando a função e exibindo o resultado no console
console.log(somar(5, 3));

// Exemplo de arrow function com um único parâmetro (não precisa de parênteses)
let dobrar = (n) => n * 2;

// Chamando a função e exibindo o resultado no console
console.log(dobrar(5));

// Exemplo de uma arrow function usada como callback
let numeros = [1, 2, 3, 4, 5];

// Usando arrow function com o método map para dobrar os valores do array
let numerosDobrados = numeros.map((n) => n * 2);

// Exibindo o array resultante no console
console.log(numerosDobrados);

// Arrow function com corpo de função mais complexo
let saudacao = (nome, idade) => {
  let mensagem = `Olá, meu nome é ${nome} e eu tenho ${idade} anos.`;
  return mensagem;
};

// Chamando a função e exibindo o resultado no console
console.log(saudacao("Ana", 25));

let soma = (num1, num2) => {
  return num1 + num2;
};

console.log(soma(2, 4));
console.log(soma(3, 7));
console.log(soma(1, 5));
