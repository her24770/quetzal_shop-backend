-- ============================================================
-- QuetzalShop - Vistas
-- DBMS: PostgreSQL
-- ============================================================

-- Vista productos con categoria
CREATE OR REPLACE VIEW v_productos_completo AS
SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.stock_minimo,
       c.nombre AS categoria
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id;

-- Vista ventas con cliente y empleado
CREATE OR REPLACE VIEW v_ventas_completo AS
SELECT v.id, v.fecha, v.total, v.descuento,
       cl.nombre AS cliente, cl.nit,
       e.nombre AS empleado, e.cargo,
       mp.metodo AS metodo_pago
FROM ventas v
INNER JOIN clientes cl ON v.cliente_id = cl.id
INNER JOIN empleados e ON v.empleado_id = e.id
INNER JOIN metodos_pago mp ON v.metodo_pago_id = mp.id;

-- Vista stock bajo
CREATE OR REPLACE VIEW v_stock_bajo AS
SELECT p.id, p.nombre, p.stock, p.stock_minimo, c.nombre AS categoria
FROM productos p
INNER JOIN categorias c ON p.categoria_id = c.id
WHERE p.stock <= p.stock_minimo;
