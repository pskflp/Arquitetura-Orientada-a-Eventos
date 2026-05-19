class Broker:
    """
    Padrao Corretor (Coreografia):
    Os servicos se comunicam via eventos sem um mestre central.
    """
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def publish(self, event_type, data):
        print(f"[Broker] Evento Publicado: {event_type}")
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(data)

class ServicoPedido:
    def __init__(self, broker):
        self.broker = broker

    def criar_pedido(self, pedido):
        print(f"Pedido: Criando pedido {pedido['id']}")
        self.broker.publish("PedidoCriado", pedido)

class ServicoEstoque:
    def __init__(self, broker):
        self.broker = broker
        self.broker.subscribe("PedidoCriado", self.reservar)

    def reservar(self, pedido):
        print("Estoque: Validando e reservando...")
        self.broker.publish("EstoqueReservado", pedido)

class ServicoPagamento:
    def __init__(self, broker):
        self.broker = broker
        self.broker.subscribe("EstoqueReservado", self.cobrar)

    def cobrar(self, pedido):
        print("Pagamento: Processando cobranca...")
        self.broker.publish("PagamentoConcluido", pedido)

class ServicoLogistica:
    def __init__(self, broker):
        self.broker = broker
        self.broker.subscribe("PagamentoConcluido", self.enviar)

    def enviar(self, pedido):
        print("Logistica: Despachando mercadoria...")

if __name__ == "__main__":
    hub = Broker()
    
    # Inicializando servicos (eles se auto-inscrevem no broker)
    estoque = ServicoEstoque(hub)
    pagamento = ServicoPagamento(hub)
    logistica = ServicoLogistica(hub)
    vendas = ServicoPedido(hub)

    vendas.criar_pedido({"id": 202, "cliente": "Jose"})
