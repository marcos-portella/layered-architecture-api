// Exemplo de uso do método slice()
// Temos uma string com várias frutas
let frutas = "maçã, banana, laranja, uva, abacaxi";
console.log("Frutas:", frutas);
console.log("Tamanho da string frutas: ", frutas.length);

// Queremos obter uma parte da string, por exemplo, apenas "banana, laranja"
let parteFrutas = frutas.slice(5, 21);
console.log("Resultado do slice(): ", parteFrutas);

// Exemplo de uso do método trim()
// Temos uma string com espaços em branco no início e no final
let frutaComEspaco = "            abacate           ";

// Queremos remover os espaços em branco do início e do final da string
let frutaSemEspaco = frutaComEspaco.trim();
console.log("Resultado do trim():", frutaSemEspaco);

// Exemplo de uso do método split()
// Temos uma string com várias frutas separadas por vírgulas
let listaDeFrutas = "maçã,banana,laranja,uva,abacaxi";

// Queremos dividir a string em um array de substrings, usando a vírgula como separador
let arrayDeFrutas = listaDeFrutas.split(",");
console.log("Resultado do split()", arrayDeFrutas);

// Testando cada fruta separadamente
// usando um método avançado: for each

arrayDeFrutas.forEach((fruta, index) => {
  console.log(`Fruta ${index + 1}: ${fruta.trim()}`); // Usa trim() para garantir que não há espaços em cada elemento
});

// Criação de strings com nomes de animais
let animal1 = "Elefante";
let animal2 = "Girafa";
let animal3 = "Zebra";

// Exemplo do método substring()
// Pega parte da string 'Elefante', começando no índice 3 até o índice 7
let parteAnimal1 = animal1.substring(3, 7);
console.log("Resultado substring()", parteAnimal1);

// Exemplo do método replace()
// Substitui a substring 'ra' por 're' em 'Girafa'
let novoAnimal2 = animal2.replace("ra", "re");
console.log("Resultado replace()", novoAnimal2);

// Exemplo do método concat()
// Concatena as strings 'Elefante', 'Girafa' e 'Zebra' com espaços entre elas
let animaisJuntos = animal1.concat(" ", animal2, " ", animal3);
console.log("Resultado concat()", animaisJuntos);

// Código json
const jsonObject = { name: "John", age: 30, city: "New York" };
console.log(jsonObject)

// Exemplo: Manipulação de Dados JSON

// Objeto JSON inicial
let pessoa = {
    "nome": "João",
    "idade": 30,
    "endereco": {
        "rua": "Rua Principal",
        "numero": 123
    },
    "telefones": ["1234-5678", "8765-4321"]
};

console.log(pessoa);

// Acessar Dados
console.log("\nAcessar Dados:");
console.log(pessoa.nome);
console.log(pessoa["idade"]);
console.log(pessoa.endereco.rua);
console.log(pessoa["telefones"][0]);
console.log(pessoa["telefones"][1]);

// Adicionar Dados
console.log("\nAdicionar Dados:");
pessoa.email = "joao@example.com";
console.log(pessoa);

// Modificar Dados
console.log("\nModificar Dados:");
pessoa.idade = 31;
pessoa.endereco.rua = "Rua Secundária";
console.log(pessoa);

// Remover Dados
console.log("\nRemover Dados:");
delete pessoa.telefones;

// Existência da Propriedade: Se a propriedade não existir no objeto,
// o operador delete não causará um erro, apenas não fará nada.
// O operador delete não pode ser usado para remover variáveis declaradas com var, let ou const
// Ele só funciona para propriedades de objetos.

console.log(pessoa);

// Operações com Arrays
console.log("\nOperações com Arrays:");
pessoa.hobbies = ["leitura", "esportes"];
console.log(pessoa.hobbies[1]);
pessoa.hobbies.push("viagens");
console.log(pessoa.hobbies);

// Iterar sobre as Propriedades do Objeto
console.log("\nIterar sobre as Propriedades do Objeto:");

// for...in não deve ser usado para iterar sobre arrays se a ordem dos elementos for importante
// pois a ordem de iteração não é garantida.
for (let chave in pessoa) {
    console.log(chave + ": " + pessoa[chave]);
}

// Converter de e para JSON
console.log("\nConverter de e para JSON:");
let jsonTexto = JSON.stringify(pessoa);

console.log(jsonTexto);

let objetoPessoa = JSON.parse(jsonTexto);
console.log(objetoPessoa);
