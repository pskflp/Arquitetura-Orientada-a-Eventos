class EventStore:
    """
    Event Sourcing:
    O estado nao eh salvo diretamente, mas sim a sequencia de eventos.
    """
    def __init__(self):
        self.events = []

    def save_event(self, event):
        self.events.append(event)
        print(f"EventStore: Evento gravado -> {event['type']}")

class PedidoWriteModel:
    """
    CQRS - Lado de Escrita (Command)
    """
    def __init__(self, event_store):
        self.event_store = event_store

    def criar_pedido(self, pedido_id, itens):
        # Valida regra de negocio e gera evento
        evento = {"type": "PedidoCriado", "id": pedido_id, "itens": itens}
        self.event_store.save_event(evento)

class PedidoReadModel:
    """
    CQRS - Lado de Leitura (Query)
    Mantem uma projecao otimizada para consulta.
    """
    def __init__(self, event_store):
        self.event_store = event_store

    def total_pedidos_realizados(self):
        # Na vida real, isso seria uma tabela SQL otimizada
        # Aqui simulamos a reconstrucao via eventos
        count = sum(1 for e in self.event_store.events if e['type'] == "PedidoCriado")
        return count

if __name__ == "__main__":
    store = EventStore()
    escrita = PedidoWriteModel(store)
    leitura = PedidoReadModel(store)

    escrita.criar_pedido(1, ["Notebook"])
    escrita.criar_pedido(2, ["Mouse"])

    print(f"Consulta (Read Model): Total de pedidos = {leitura.total_pedidos_realizados()}")
