// Definição da classe "Casa"

class Casa {

    // Construtor define as propriedades da classe
    constructor (cor, numQuarto, temGaragem) {
        this.cor = cor;
        this.numQuarto = numQuarto;
        this.temGaragem = temGaragem;
    }
    
    // Método para descrever a casa
    descrever() {
        let descricao = `Esta casa é de cor ${this.cor}, tem ${this.numQuarto} quarto(s)...`;
        if (this.temGaragem) {
            descricao += ` e tem uma garagem.`;
        } else {
            descricao += ` e não tem garagem.`;
        }
        return descricao;
    }

}

// Criação de objetos (instâncias da classe Casa)
const minhaCasa = new Casa("verde", 3, true);
const suaCasa = new Casa("roxa", 2, false);

// Manipulação dos objetos e exibição das descrições
console.log(minhaCasa.descrever());
console.log(suaCasa.descrever());

// Classe BASE "Casa"

class Casa2 {
    constructor(cor, numQuarto, temGaragem) {
        // Propriedades privadas utilizando convenção de underscore
        this._cor = cor;
        this._numQuarto = numQuarto;
        this._temGaragem = temGaragem;
    }

    // Métodos getters e setters para acessar e modificar as propriedades
    get cor() {
        return this._cor;
    }

    set cor(novaCor) {
        this._cor = novaCor;
    }

    get numQuarto() {
        return this._numQuarto;
    }

    set numQuarto(novoNumQuarto) {
        this._numQuarto = novoNumQuarto;
    }

    get temGaragem() {
        return this._temGaragem;
    }

    set temGaragem(novoTemGaragem) {
        this._temGaragem = novoTemGaragem;
    }

    // Método para descrever a casa
    descrever() {
        let descricao = `Esta casa é de cor ${this._cor}, tem ${this._numQuarto} quartos`;
        if (this._temGaragem) {
            descricao += " e tem uma garagem.";
        } else {
            descricao += " e não tem garagem.";
        }
        return descricao;
    }
}

// Classe DERIVADA "CasaLuxuosa" que HERDA de "Casa"
class CasaLuxuosa extends Casa2 {
    constructor(cor, numeroDeQuartos, temGaragem, temPiscina) {
        // Chama o construtor da classe base
        super(cor, numeroDeQuartos, temGaragem);
        // Propriedade adicional específica da classe derivada
        this._temPiscina = temPiscina;
    }

    // Getter e setter para a nova propriedade
    get temPiscina() {
        return this._temPiscina;
    }

    set temPiscina(novoTemPiscina) {
        this._temPiscina = novoTemPiscina;
    }

    // Sobrescrita do método descrever para incluir a piscina
    descrever() {
        let descricao = super.descrever(); // Chama o método descrever da classe base
        if (this._temPiscina) {
            descricao += " Também tem uma piscina.";
        } else {
            descricao += " Não tem piscina.";
        }
        return descricao;
    }
}

// Criação de objetos (instâncias das classes)
const minhaCasa2 = new Casa2("azul", 3, true);
const casaLuxuosa = new CasaLuxuosa("branca", 5, true, true);

// Manipulação dos objetos e exibição das descrições
console.log(minhaCasa2.descrever());
console.log(casaLuxuosa.descrever());

// Classe base "Imovel"
class Imovel {
    constructor(endereco, tamanho) {
        this.endereco = endereco;
        this.tamanho = tamanho;
    }

    // Método abstrato para descrever o imóvel (deve ser implementado nas subclasses)
    descrever() {
        throw new Error("Este método deve ser implementado por subclasses");
    }
}

// Classe derivada "Casa" que herda de "Imovel"
class Casa3 extends Imovel {
    constructor(endereco, tamanho, cor, numeroDeQuartos, temGaragem) {
        super(endereco, tamanho);
        this.cor = cor;
        this.numeroDeQuartos = numeroDeQuartos;
        this.temGaragem = temGaragem;
    }

    // Implementação do método descrever
    descrever() {
        let descricao = `Casa localizada em ${this.endereco},
         de cor ${this.cor}, com ${this.numeroDeQuartos} quartos, de tamanho ${this.tamanho}m²`;
        
         // operador ternário
         descricao += this.temGaragem ? " e possui garagem." : " e não possui garagem.";

        return descricao;
    }
}

// Classe derivada "Apartamento" que herda de "Imovel"
class Apartamento extends Imovel {
    constructor(endereco, tamanho, numeroDoAndar, possuiElevador) {
        super(endereco, tamanho);
        this.numeroDoAndar = numeroDoAndar;
        this.possuiElevador = possuiElevador;
    }

    // Implementação do método descrever
    descrever() {
        let descricao = `Apartamento localizado em ${this.endereco},
         no ${this.numeroDoAndar}º andar, de tamanho ${this.tamanho}m²`;
        
         descricao += this.possuiElevador ? " e possui elevador." : " e não possui elevador.";
        
         return descricao;
    }
}

// Função para descrever um imóvel (polimorfismo)
function descreverImovel(imovel) {
    console.log(imovel.descrever());
}

// Criação de objetos (instâncias das classes)
const minhaCasa3 = new Casa3("Rua A, 123", 120, "azul", 3, true);
const meuApartamento = new Apartamento("Avenida B, 456", 85, 7, true);

// Manipulação dos objetos e exibição das descrições usando polimorfismo
descreverImovel(minhaCasa3);
descreverImovel(meuApartamento);

