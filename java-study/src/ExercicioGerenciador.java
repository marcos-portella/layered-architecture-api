//Desafio: O Gerenciador de Cargas do Marcos

// Você vai criar um sistema que registra o peso de 4 caminhões que estão na fila da balança.

// O que o programa deve fazer:

// Criar um array de double com 4 posições chamado pesos.

// Usar um for tradicional para perguntar ao usuário o peso de cada um dos 4 caminhões e guardar no array.

// Após os cadastros, o programa deve calcular a Média de Peso desses caminhões. (Dica: Somar todos e dividir por 4).

// Usar um For-Each para imprimir todos os pesos registrados.

// No final, imprimir a média calculada.

import java.util.Scanner;

public class ExercicioGerenciador {
    
    public static double calcularMedia(double[] pesos) {
        double soma = 0.0;
        for (double peso : pesos) {
            soma += peso;
        }
        double soma2 = soma / pesos.length;
        return soma2;
    }
    
    public static void main(String[] args) {

        double[] pesos = new double[4];
        Scanner leitor = new Scanner(System.in);

        for (int i = 0; i < pesos.length; i++) {
            System.out.print("Qual o peso do caminhão? ");
            pesos[i] = leitor.nextDouble();
        }

        int i = 1;

        for (double peso : pesos) {

            System.out.println("O peso do caminhão no °" + i + " espaço é: " + peso);

            i += 1;
        }

        double resultado = calcularMedia(pesos);
        System.out.print("A media do peso dos caminhões é: " + resultado);
        leitor.close();
    }
}
