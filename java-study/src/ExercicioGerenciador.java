// Regras de Negócio:

// O peso permitido é entre 2.000kg e 10.000kg.

// Se o usuário digitar um peso inválido, o programa deve exibir uma mensagem 
// de erro: "Peso inválido! O caminhão deve ter entre 2000kg e 10000kg.".

// O pulo do gato: O programa não deve avançar para o próximo caminhão enquanto 
// o peso atual não for válido. (Dica: você vai precisar de um loop dentro do 
// outro ou de uma lógica de repetição específica).

import java.io.IOException;
import java.util.InputMismatchException;
import java.util.Scanner;

public class ExercicioGerenciador {
    public static void limparConsole(){
        try {
            if (
                System.getProperty("os.name")
                    .contains("Windows")
            ) {
                new ProcessBuilder("cmd", "/c", "cls")
                    .inheritIO()
                    .start()
                    .waitFor();
            } else {
                    new ProcessBuilder("clear")
                        .inheritIO()
                        .start()
                        .waitFor();
            }
        } catch (IOException | InterruptedException e) {
            System.out.println("Erro ao limpar o console: " + e.getMessage());
        }
    }
    
    public static double calcularMedia(double[] pesos) {
        double soma = 0.0;
        for (double peso : pesos) {
            soma += peso;
        }
        return soma / pesos.length;
    }
    
    public static void main(String[] args) {

        double[] pesos = new double[4];
        Scanner leitor = new Scanner(System.in);

        for (int i = 0; i < pesos.length; i++) {
            boolean trava = false;
            while(!trava) {
                try {
                    System.out.println("Valores válidos: 2000 á 10000.");
                    System.out.print("Qual o peso do caminhão? ");
                    double valor = leitor.nextDouble();
                    
                    if (valor < 2000 || valor > 10000) {
                        limparConsole();
                        System.out.println("Valor não válido.");
                    } else {
                        limparConsole();
                        pesos[i] = valor;
                        System.out.println("Peso válido!");
                        trava = true;
                        System.out.println(
                            "Vagas disponíveis: " + (pesos.length - (i + 1))
                        );
                    }
                }catch (InputMismatchException e) {
                    limparConsole();
                    System.out.println(
                        "Erro: Você deve digitar apenas números!"
                    );
                    leitor.next();
                }
            }
        }

        int i = 1;
        limparConsole();

        for (double peso : pesos) {

            System.out.println(
                "O peso do caminhão no °" + i + " espaço é: " + peso
            );

            i += 1;
        }

        double resultado = calcularMedia(pesos);
        System.out.print("A media do peso dos caminhões é: " + resultado);
        leitor.close();
    }
}
