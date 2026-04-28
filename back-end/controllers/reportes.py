from database.queries import reportes as reportes_query


def get_stats() -> dict:
    return reportes_query.get_stats()


def get_top_productos() -> list:
    return reportes_query.get_top_productos()


def get_ventas_por_metodo() -> list:
    return reportes_query.get_ventas_por_metodo()


def get_clientes_activos() -> list:
    return reportes_query.get_clientes_activos()


def get_productos_bajo_vendidos() -> list:
    return reportes_query.get_productos_bajo_vendidos()
