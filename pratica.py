import pyodbc
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dotenv import load_dotenv
import os
# pip install pyodbc pandas sqlalchemy plotly dash dash-bootstrap-components dash-iconify
load_dotenv()

# Configuración de conexión
direccion_servidor = os.getenv('DB_SERVER')
nombre_bd = os.getenv('DB_NAME')
nombre_usuario = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# Conexión a la base de datos
conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + direccion_servidor +
                          ';DATABASE=' + nombre_bd + ';UID=' + nombre_usuario + ';PWD=' + password)

# Creación de un motor para SQLAlchemy
engine = create_engine(f'mssql+pyodbc://{nombre_usuario}:{password}@{direccion_servidor}/{nombre_bd}?driver=ODBC+Driver+17+for+SQL+Server')

# Consulta SQL y creación del DataFrame
query_ventas_fecha = """
SELECT fecha, SUM(monto) as total_ventas
FROM notaventa
GROUP BY fecha
ORDER BY fecha;
"""
df_ventas_fecha = pd.read_sql(query_ventas_fecha, engine)

# Crear un gráfico de líneas en 3D
fig = px.line(df_ventas_fecha, x='fecha', y='total_ventas', title='Ventas Totales por Fecha')

# Personalización del diseño del gráfico
fig.update_layout(
    plot_bgcolor='rgba(10,10,10,10)',   # Fondo del gráfico
    paper_bgcolor='rgba(20,20,20,20)',  # Fondo del papel
    font=dict(color="white"),           # Color de la fuente
)

# Mostrar el gráfico
fig.show()


# 3D
# Consulta SQL
query_ventas_fecha = """
SELECT fecha,
       SUM(monto) as total_ventas,
       AVG(monto) as promedio_ventas
FROM notaventa
GROUP BY fecha
ORDER BY fecha;
"""

# Crear DataFrame y Gráfico
df_ventas_fecha = pd.read_sql(query_ventas_fecha, engine)
fig1 = px.scatter_3d(df_ventas_fecha, x='fecha', y='total_ventas', z='promedio_ventas', title='Ventas Totales y Promedio por Fecha')
fig1.update_traces(marker=dict(size=5, color='blue'))
fig1.show()


# Consulta SQL
query_ventas_cliente_fecha = """
SELECT c.nombre AS cliente, nv.fecha, nv.monto
FROM notaventa nv
JOIN cliente c ON nv.id_cliente = c.id_cliente
ORDER BY c.nombre, nv.fecha;
"""

# Crear DataFrame y Gráfico
df_ventas_cliente_fecha = pd.read_sql(query_ventas_cliente_fecha, engine)
fig2 = px.scatter_3d(df_ventas_cliente_fecha, x='cliente', y='fecha', z='monto', title='Ventas por Cliente y Fecha')
fig2.update_traces(marker=dict(size=5, color='green'))
fig2.show()


# Consulta SQL
query_inventario_categoria_precio = """
SELECT cat.nombre AS categoria, p.precio, p.stock
FROM producto p
JOIN categoria cat ON p.id_categoria = cat.id_categoria;
"""

# Crear DataFrame y Gráfico
df_inventario_categoria_precio = pd.read_sql(query_inventario_categoria_precio, engine)
fig3 = px.scatter_3d(df_inventario_categoria_precio, x='categoria', y='precio', z='stock', title='Inventario por Categoría y Precio de Producto')
fig3.update_traces(marker=dict(size=5, color='orange'))
fig3.show()

# Consulta SQL
query_productos_fecha_cantidad = """
SELECT nv.fecha, p.descripcion AS producto, dv.cantidad
FROM detalleventa dv
JOIN producto p ON dv.id_producto = p.id_producto
JOIN notaventa nv ON dv.id_venta = nv.id_venta
ORDER BY nv.fecha, p.descripcion;
"""

# Crear DataFrame y Gráfico
df_productos_fecha_cantidad = pd.read_sql(query_productos_fecha_cantidad, engine)
fig4 = px.scatter_3d(df_productos_fecha_cantidad, x='fecha', y='producto', z='cantidad', title='Productos Más Vendidos por Fecha y Cantidad Vendida')
fig4.update_traces(marker=dict(size=5, color='purple'))
fig4.show()

# Consulta SQL
query_ventas_categoria_cantidad = """
SELECT cat.nombre AS categoria, SUM(dv.cantidad) AS total_cantidad, SUM(nv.monto) AS total_ventas
FROM detalleventa dv
JOIN producto p ON dv.id_producto = p.id_producto
JOIN categoria cat ON p.id_categoria = cat.id_categoria
JOIN notaventa nv ON dv.id_venta = nv.id_venta
GROUP BY cat.nombre;
"""

# Crear DataFrame y Gráfico
df_ventas_categoria_cantidad = pd.read_sql(query_ventas_categoria_cantidad, engine)
fig5 = px.scatter_3d(df_ventas_categoria_cantidad, x='categoria', y='total_cantidad', z='total_ventas', title='Total de Ventas por Categoría y Cantidad de Productos Vendidos')
fig5.update_traces(marker=dict(size=5, color='red'))
fig5.show()