public class SecurityProject {

    public static double analizarCarga(
        String nome, double peso, boolean licenca
    ) {
        System.out.println("--- Verificando credenciais de: " + nome + " ---");

        if (peso <= 5000) {
            
            if (licenca == true) {
                System.out.println("Carga liberada para o galpão A");
            } else {
                System.out.println(
                    "Carga liberada, mas deve aguardar a vistoria"
                );
            }

        } else {
            System.out.println(
                "Carga muito pesada: Encaminhar para o terminal externo"
            );
        }

        if (peso > 1000) {
            return peso * 0.10;
        } else {
            return 25.0;
        }
    }

    public static void main(String[] args) {



        double taxa = analizarCarga(
            "Portella", 6000.0, true
        );
        System.out.println("Essa é sua taxa pela carga: " + taxa);

        double taxa2 = analizarCarga(
            "Miguel", 800.0, true
        );
        System.out.println("Essa é sua taxa pela carga: " + taxa2);

        double taxa3 = analizarCarga(
            "Visitante", 4390.0, false
        );
        System.out.println("Essa é sua taxa pela carga: " + taxa3);
    }
}


