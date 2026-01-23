// calculadora

// Função que simula a operação de uma calculadora
function calculadora(num1, num2) {
  // Operações aritméticas básicas
  let adicao = num1 + num2;
  let subtracao = num1 - num2;
  let multiplicacao = num1 * num2;
  let divisao = num1 / num2;
  let modulo = num1 % num2;
  let exponencial = num1 ** num2;

  // Incremento e Decremento
  // Vamos incrementar num1
  let incrementar = num1;
  incrementar++;

  // Vamos decrementar num2
  let decrementar = num2;
  decrementar--;

  // Exibindo os resultados no console
  console.log(`Adição (${num1} + ${num2}) = ${adicao}`);
  console.log(`Subtração (${num1} - ${num2}) = ${subtracao}`);
  console.log(`Multiplicação (${num1} * ${num2}) = ${multiplicacao}`);
  console.log(`Divisão (${num1} / ${num2}) = ${divisao}`);
  console.log(`Módulo (${num1} % ${num2}) = ${modulo}`);
  console.log(`Exponencial (${num1} ** ${num2}) = ${exponencial}`);
  console.log(`Incrementar (${num1})++ = ${incrementar}`);
  console.log(`Decrementar (${num2})-- = ${decrementar}`);
}

// Executando a função calculadora
// calculadora();
// NaN = Not a Number -> não é número

calculadora(10, 5);

// Exemplos de Operadores Lógicos em JavaScript

// Operador E lógico (&&)
const a = true;
const b = false;

const resultadoE1 = a && b; //false
const resultadoE2 = a && true; //true

console.log(`true && false: ${resultadoE1}`); // Saída: false
console.log(`true && true: ${resultadoE2}`); // Saída: true

// Operador OU lógico (||)
const resultadoOU1 = a || b; // true
const resultadoOU2 = a || false;

console.log(`true || false: ${resultadoOU1}`); // Saída: true
console.log(`false || false: ${resultadoOU2}`);

// Operador NÃO lógico (!)
const resultadoNao1 = !a;
const resultadoNao2 = !b;

console.log(`!true: ${resultadoNao1}`); // Saída: false
console.log(`!false: ${resultadoNao2}`); // Saída: true

// Combinações de operadores lógicos
const resultadoComb1 = (a || b) && !b;
const resultadoComb2 = !(a && b) || a;

console.log(`(true || false) && !false: ${resultadoComb1}`); // Saída: true
console.log(`!(true && false) || true: ${resultadoComb2}`); // Saída: true

// Exemplos de Operadores de Atribuição em JavaScript

// Operador de Atribuição Básico (=)
let a2 = 10;
console.log(`Valor inicial de a: ${a2}`);

// Operador de Atribuição de Adição (+=)
a2 += 5; // equilavente a = a + 5
console.log(`Após a += 5, valor de a: ${a2}`);

// Operador de Atribuição de Subtração (-=)
a2 -= 3; // a = a - 3;
console.log(`Após a -= 3, valor de a: ${a2}`);

// Operador de Atribuição de Multiplicação (*=)
a2 *= 2; // a = a * 2;
console.log(`Após a *= 2, valor de a: ${a2}`);
// comparação e não atribuição: >=

// Operador de Atribuição de Divisão (/=)
a2 /= 4;
console.log(`Após a /= 4, valor de a: ${a2}`);

// Operador de Atribuição de Resto (%=)
a2 %= 4;
console.log(`Após a %= 4, valor de a: ${a2}`);

// Operador de Atribuição de Exponenciação (**=)
a2 **= 3;
console.log(`Após a **= 3, valor de a: ${a2}`);
