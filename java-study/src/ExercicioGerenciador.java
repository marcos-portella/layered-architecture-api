import java.io.IOException;
import java.util.InputMismatchException;
import java.util.Scanner;
import java.util.ArrayList;

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

    public static double calcularMedia(ArrayList<Double> pesos) {
        if (pesos.isEmpty()) return 0.0;
        double soma = 0.0;
        for (double peso : pesos) {
            soma += peso;
        }
        return soma / pesos.size();
    }

    public static void main(String[] args) {
        ArrayList<Double> listaDePesos = new ArrayList<>();
        Scanner leitor = new Scanner(System.in);
        boolean sim = true;

        while(sim) {
            System.out.println("\n--- MENU DE LOGÍSTICA ---");
            System.out.println("Opções: (adicionar) | (deletar) | (listar) | (media) | (sair)");
            System.out.print("Comando: ");
            String esc = leitor.nextLine().trim().toLowerCase();

            if (esc.equals("adicionar")) {
                boolean conti = true;
                while (conti) {
                    boolean trava = false;
                    while (!trava) {
                        try {
                            System.out.print("Peso do caminhão (2000-10000): ");
                            double valor = leitor.nextDouble();
                            leitor.nextLine();

                            if (valor < 2000 || valor > 10000) {
                                System.out.println("Valor inválido.");
                            } else {
                                listaDePesos.add(valor);
                                System.out.println("✅ Adicionado!");
                                trava = true;
                            }
                        } catch (InputMismatchException e) {
                            System.out.println("Erro: Use apenas números!");
                            leitor.nextLine();
                        }
                    }
                    System.out.print("Adicionar outro? (s/n): ");
                    String resposta = leitor.nextLine();
                    if (resposta.equalsIgnoreCase("n")) conti = false;
                }
            } 
            else if (esc.equals("deletar")) {
                if (listaDePesos.isEmpty()) {
                    System.out.println("Lista vazia!");
                } else {
                    System.out.print("Qual o índice (0 a " + (listaDePesos.size()-1) + ")? ");
                    int n = leitor.nextInt();
                    leitor.nextLine();
                    if (n >= 0 && n < listaDePesos.size()) {
                        listaDePesos.remove(n);
                        System.out.println("🗑️ Removido!");
                    } else {
                        System.out.println("Índice inexistente.");
                    }
                }
            } 
            else if (esc.equals("listar")) {
                limparConsole();
                for (int i = 0; i < listaDePesos.size(); i++) {
                    System.out.println("Vaga " + i + ": " + listaDePesos.get(i) + "kg");
                }
            } 
            else if (esc.equals("media")) {
                System.out.println("Média: " + calcularMedia(listaDePesos) + "kg");
            } 
            else if (esc.equals("sair")) {
                sim = false;
            } 
            else {
                System.out.println("Comando inválido.");
            }
        }
        System.out.println("Programa encerrado.");
        leitor.close();
    }
}
