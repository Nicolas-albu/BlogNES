def generate_id():
    """
    Gera IDs sequenciais infinitamente a partir de zero.

    Esta função é um gerador infinito que inicia em zero e gera IDs sequenciais
    infinitamente à medida que é iterada.

    Yields:
        int: Um ID sequencial gerado a partir de zero em diante.
    """
    number = 0
    while True:
        yield number
        number += 1
