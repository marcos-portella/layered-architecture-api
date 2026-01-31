// exemplosArray.js

// Criar um Array
let array1 = [];
let array2 = new Array();
let array3 = ["maçã", "banana", "uva"];

console.log("Array 1", array1);
console.log("Array 2", array2);
console.log("Array 3", array3);

// Adicionando elementos ao array
//array1 = ["teste"];
//array2 = ["teste2"];
//array3 = ["teste3"];

console.log("\nArray após adicionar elementos:", array1);
array1.push("el1");
array2.push("el2");
array3.push("el3");

console.log("\nNovo Array 1", array1);
console.log("Novo Array 2", array2);
console.log("Novo Array 3", array3);

// Acessar elementos de um array
let primeiroElemento = array1[0];
let erro = array1[1];
let segundoElemento = array2[0];
let terceiroElemento = array3[3];

console.log("\nPrimeiro elemento:", primeiroElemento);
console.log("Erro:", erro);
console.log("Segundo elemento:", segundoElemento);
console.log("Terceira elemento:", terceiroElemento);

// Modificar elementos de um array
array1[0] = "novo elemento";
console.log("\nArray após modificar elementos:", array1);

// Criando um array inicial
let frutas = ["maçã", "banana", "laranja", "uva"]; // pos: 0 .. 3

console.log("Array inicial: " + frutas);
console.log("Comprimento do array: " + frutas.length);

// Usando o método push() para adicionar elementos ao final do array
let novoComprimento = frutas.push("manga", "abacate");
console.log("\nArray atualizado push: " + frutas);
console.log("Novo comprimento do array: " + novoComprimento);

// Usando o método pop() para remover o último elemento do array
let ultimaFruta = frutas.pop();
console.log("\nArray atualizado pop: " + frutas);
console.log("Última fruta removida: " + ultimaFruta);

// Usando o método shift() para remover o primeiro elemento do array
let primeiraFruta = frutas.shift();
console.log("\nArray atualizado shift: " + frutas);
console.log("Primeira fruta removida: " + primeiraFruta);

// Métodos Avançados de Array

let array11 = [3, 4, 5]; // 0, 1 , 2
let array22 = [6, 7, 8]; // 0, 1 , 2

console.log("Array original:", array11);

// Método unshift(): adiciona um ou mais elementos ao início do array
array11.unshift(1, 2);
console.log("\nApós unshift(1, 2):", array11);

// Método concat(): retorna um novo array resultante da concatenação de dois ou mais arrays
let array33 = array11.concat(array22);
console.log("\nArray concatenado:", array33);

// Método splice(): altera o conteúdo de um array removendo, substituindo ou adicionando elementos
array33.splice(5, 2, 'a', 'b');
console.log("\nApós splice(5, 2, 'a', 'b'):", array33);

// Método slice(): retorna uma cópia superficial de uma parte do array em um novo array
let array44 = array33.slice(3,6);
console.log("\nApós slice(3, 6):", array44);

// Mostrar o array3 original após todas as operações
console.log("\nArray3 original após todas as operações:", array33);
