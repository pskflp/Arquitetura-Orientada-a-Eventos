class SagaOrquestradaPedido:
    """
    Saga Pattern:
    Gerencia transacoes distribuidas com acoes de compensacao (rollback).
    """
    def executar(self, pedido):
        print(f"--- Iniciando Saga para o Pedido {pedido['id']} ---")
        
        steps = [
            (self.reservar_estoque, self.cancelar_estoque),
            (self.processar_pagamento, self.estornar_pagamento),
            (self.agendar_entrega, lambda p: print("Logistica: Nao precisa compensar entrega ainda"))
        ]

        historico_sucesso = []

        try:
            for acao, compensacao in steps:
                if acao(pedido):
                    historico_sucesso.append(compensacao)
                else:
                    raise Exception("Falha no passo da Saga")
            print("Saga concluida com sucesso!")
            
        except Exception as e:
            print(f"Saga interrompida: {e}. Iniciando compensacoes...")
            for compensacao in reversed(historico_sucesso):
                compensacao(pedido)

    def reservar_estoque(self, p):
        print("Passo 1: Estoque reservado")
        return True

    def cancelar_estoque(self, p):
        print("Compensacao 1: Estoque liberado")

    def processar_pagamento(self, p):
        print("Passo 2: Tentando cobrar... FALHOU!")
        return False # Simulando erro

    def estornar_pagamento(self, p):
        print("Compensacao 2: Pagamento estornado")

    def agendar_entrega(self, p):
        print("Passo 3: Entrega agendada")
        return True

if __name__ == "__main__":
    saga = SagaOrquestradaPedido()
    saga.executar({"id": 404})
