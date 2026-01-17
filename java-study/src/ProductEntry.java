import java.util.Scanner; // We need to import the tool to read inputs

public class ProductEntry {
    public static void main(String[] args) {
        // Create a Scanner object to read from the terminal (System.in)
        Scanner reader = new Scanner(System.in);

        System.out.println("--- Product Entry ---");

        // Reading a String (Text)
        System.out.print("Enter product name: ");
        String productName = reader.nextLine();

        // Reading an int (Integer)
        System.out.print("Enter quantity: ");
        int quantity = reader.nextInt();

        // Reading a double (Decimal)
        System.out.print("Enter unit price: ");
        double price = reader.nextDouble();

        // Processing
        double totalInventoryValue = quantity * price;

        // Output
        System.out.println("\n--- Summary ---");
        System.out.println("Product: " + productName);
        if (quantity>0){
        System.out.println("Total Value: $" + totalInventoryValue);
        } else {
            System.out.println("\nO estoque está inválido");
        }

        // Good practice: close the reader
        reader.close();
    }
}