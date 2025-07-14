import { useState } from "react";
// Local para outros imports

function cadastroVendedor(){
    const [mostrarOutros, setMostrarOutros] = useState(false);
    return(
        <>
            {/* Local para o Nav */}
            <h1>Insira as informações da empresa</h1>
            <form action=""> {/* Os "" que for deixando em branco é os que não sei/decedi o que colocar */}

                <label htmlFor="nome">Qual é o nome?</label>
                <input type="text" id="nome" name="nome" placeholder="Nome" />

                <fieldset>

                    <legend>Qual é a localização?</legend>

                    <input type="text" name="pais" placeholder="País" />
                    <input type="text" name="estado" placeholder="Estado" />
                    <input type="text" name="cidade" placeholder="Cidade" />
                    <input type="text" name="rua" placeholder="Rua" />
                    <input type="number" name="numero" min={0} placeholder="Número" />

                </fieldset>
                

                <label htmlFor="telefone">Qual é o telefone?</label>
                <input type="tel" id="telefone" name="telefone" pattern="^\([0-9]{2}\) [0-9]{5}-[0-9]{4}$" title="Formato esperado: (99) 99999-9999" placeholder="Telefone" /> {/* É para funcionar s´´o com números do Brasil, para mais países tem que ajeitar */}

                <label htmlFor="email">Qual é o email?</label>
                <input type="email" id="email" name="email" placeholder="Email" />

                <fieldset>

                    <legend>Quais são as infraestruturas de carregamento que possui?</legend>

                    <label>
                        <input type="checkbox" name="infraestrutura" value="nao" /> Não possuo
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="barco" /> Barcos de carga
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="trem" /> Trens de carga
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="aviao" /> Avião de carga
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="guindaste" /> Guindaste
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="paleteira" /> Paleteira manual
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="esteira" /> Esteira de carregamento
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="automovel" /> Automóveis de transporte {/* Me refiro a veículos como caminhão, nome pode mudar */}
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="armazem" /> Armazém
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="porto" /> Porto
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="aeroporto" /> Aeroporto
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="terminalRodoviario" /> Terminal rodoviário
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="terminalFerroviario" /> Terminal ferroviário
                    </label>
                    <label>
                        <input type="checkbox" name="infraestrutura" value="outros" onChange={e => setMostrarOutros(e.target.checked)} /> Outros
                    </label>
                    {mostrarOutros && <input type="text" name="infraestrutura_outros" placeholder="Especifique" />} {/* Para isso, e fazer umas correções, eu usei o GPT */}
                
                </fieldset>

                <button type="submit">Enviar informações</button>
            </form>
        </>
    );
}

export default cadastroVendedor;