class MediadorPedido:
    """
    Padrao Mediador (Orquestracao):
    Um componente central controla o fluxo e sabe quais servicos chamar.
    """
    def processar_pedido(self, pedido):
        print(f"--- Mediador: Iniciando pedido {pedido['id']} ---")
        
        # O Mediador comanda o fluxo passo a passo
        if ServicoEstoque.reservar(pedido):
            if ServicoPagamento.cobrar(pedido):
                ServicoLogistica.enviar(pedido)
                print("Pedido finalizado com sucesso!")
            else:
                print("Pagamento falhou. Solicitando estorno de estoque...")
                ServicoEstoque.cancelar_reserva(pedido)
        else:
            print("Estoque insuficiente.")

class ServicoEstoque:
    @staticmethod
    def reservar(pedido):
        print("Estoque: Reservando itens...")
        return True

    @staticmethod
    def cancelar_reserva(pedido):
        print("Estoque: Reserva cancelada.")

class ServicoPagamento:
    @staticmethod
    def cobrar(pedido):
        print("Pagamento: Cobrando cliente...")
        return True

class ServicoLogistica:
    @staticmethod
    def enviar(pedido):
        print("Logistica: Enviando pedido para entrega...")

if __name__ == "__main__":
    mediador = MediadorPedido()
    pedido_exemplo = {"id": 101, "valor": 250.0}
    mediador.processar_pedido(pedido_exemplo)
