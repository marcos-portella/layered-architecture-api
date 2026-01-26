// Variável que representa a previsão do tempo
// Pode ser "rainy" (chuvoso), "sunny" (ensolarado) ou "cloudy" (nublado)

let weatherForecast = "sunny";

// Analogia com a vida real: Decidindo se devemos levar um guarda-chuva
// Vamos adicionar uma condição extra para cobrir outro cenário

if (weatherForecast === "rainy") {
  // se
  console.log("devemos levar um guarda-chuva");
} else if (weatherForecast === "cloudy") {
  // senão se
  console.log("devemos levar um guarda-chuva, só por segurança");
} else {
  // senão
  console.log("NÃO devemos levar um guarda-chuva");
}

// Função que recebe a cor do semáforo e decide a ação do pedestre
function checkTrafficLight(lightColor) {
  switch (lightColor) {
    case "verde":
      console.log("Pode atravessar a rua.");
      break;
    case "amarelo":
      console.log("Prepare-se para parar.");
      break;
    case "vermelho":
      console.log("Pare! Não atravesse a rua.");
      break;
    default:
      console.log(
        "Cor inválida! Aguarde até que o semáforo",
        "esteja em uma cor válida.",
      );
  }
}

// Exemplos de uso
checkTrafficLight("verde");
//checkTrafficLight('amarelo');
//checkTrafficLight('vermelho');
//checkTrafficLight('azul');

// Imagine que você é um entregador de pizzas em uma cidade com várias ruas numeradas de 1 a 10.
// Você tem que entregar uma pizza em cada rua, começando da rua 1 até a rua 10.

// Aqui, usaremos um loop for para simular esse processo:

for (let rua = 1; rua <=10; rua++) {
    console.log("Entrega feita na rua: ", rua);
}

// Imagine que você está fazendo exercícios físicos para se manter saudável.
// Você decide fazer flexões até ficar cansado.

// Aqui, usaremos um loop while para simular esse processo:

let quantidadeFlexoes = 0;
let cansaco = false;

while (!cansaco) {
    quantidadeFlexoes++;
    console.log("eu fiz ", quantidadeFlexoes, "flexoes!");

    if (quantidadeFlexoes === 10) {
        cansaco = true;
    }
}

// Imagine que você está tentando aprender a andar de bicicleta.
// Você decide praticar até conseguir andar por pelo menos 1 minuto sem cair.

// Aqui, usaremos um loop do...while para simular esse processo:

let tempoDeAndar = 0;
let caiu = false;

do {
    tempoDeAndar++;
    console.log("andei de bicicleta por ", tempoDeAndar, "minutos...");

    if (tempoDeAndar === 8) {
        caiu = true;
    }

} while (!caiu && tempoDeAndar < 10);


// Imagine que você está organizando uma festa de aniversário.
// Os blocos de código são como diferentes áreas da festa, onde diferentes atividades acontecem.
// Por exemplo, você pode ter uma área para dançar, uma área para jogos e uma área para comer.

{
    // Área para dançar
    console.log("Hora de dançar!");
    // Aqui vão as instruções para a pista de dança
}

{
    // Área para jogos
    console.log("Vamos jogar!");
    // Aqui vão as instruções para os jogos
}

{
    // Área para comer
    console.log("Hora de comer!");
    // Aqui vão as instruções para o buffet
}

// Os rótulos são como etiquetas que você coloca em diferentes atividades durante a festa, para identificá-las.

// Imagine que você tem uma competição de dança e uma competição de jogos acontecendo ao mesmo tempo.

danca:
for (let i = 0; i < 3; i++) {
    jogos:
    for (let j = 0; j < 3; j++) {
        if (i === 1 && j === 1) {
            console.log("A competição de dança foi interrompida!"); // Sai da competição de dança
            break danca;
        }
        console.log("Competidor " + (i+1) + " está dançando enquanto o competidor " + (j+1) + " está jogando.");
    }
}

/*
    O código simula uma situação em que há uma competição de dança e uma competição de jogos acontecendo simultaneamente.
    Os loops for aninhados representam as duas competições,
    onde cada competidor está envolvido tanto na dança quanto nos jogos.
    Quando uma condição específica é atendida (no caso, i === 1 && j === 1),
    a competição de dança é interrompida e uma mensagem é exibida,
    utilizando o rótulo danca para sair do loop da competição de dança.
    Isso demonstra o uso dos rótulos para controlar o fluxo do código em situações específicas.
 */