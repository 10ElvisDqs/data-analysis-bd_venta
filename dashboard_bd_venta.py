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

# Consultas SQL y creación de DataFrames
# Gráficos de ventas y productos (los queries son los mismos que ya has definido)
# ...
# Consultas SQL y creación de DataFrames
# 1. Gráfico de Ventas por Fecha
query_ventas_fecha = """
SELECT fecha, SUM(monto) as total_ventas
FROM notaventa
GROUP BY fecha
ORDER BY fecha;
"""
df_ventas_fecha = pd.read_sql(query_ventas_fecha, engine)
print(df_ventas_fecha)
fig1 = px.line(df_ventas_fecha, x='fecha', y='total_ventas', title='Ventas Totales por Fecha')
fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)

# 2. Gráfico de Ventas por Cliente
query_ventas_cliente = """
SELECT c.nombre, SUM(nv.monto) as total_ventas
FROM notaventa nv
JOIN cliente c ON nv.id_cliente = c.id_cliente
GROUP BY c.nombre
ORDER BY total_ventas DESC;
"""
df_ventas_cliente = pd.read_sql(query_ventas_cliente, engine)
fig2 = px.bar(df_ventas_cliente, x='nombre', y='total_ventas', title='Ventas Totales por Cliente')
fig2.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)

# 3. Gráfico de Productos Más Vendidos
query_productos_vendidos = """
SELECT p.descripcion, SUM(dv.cantidad) as total_vendido
FROM detalleventa dv
JOIN producto p ON dv.id_producto = p.id_producto
GROUP BY p.descripcion
ORDER BY total_vendido DESC;
"""
df_productos_vendidos = pd.read_sql(query_productos_vendidos, engine)
fig3 = px.bar(df_productos_vendidos.head(10), x='descripcion', y='total_vendido', title='Productos Más Vendidos')
fig3.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)

# 4. Gráfico de Ventas por Categoría
query_ventas_categoria = """
SELECT cat.nombre as categoria, SUM(nv.monto) as total_ventas
FROM notaventa nv
JOIN detalleventa dv ON nv.id_venta = dv.id_venta
JOIN producto p ON dv.id_producto = p.id_producto
JOIN categoria cat ON p.id_categoria = cat.id_categoria
GROUP BY cat.nombre
ORDER BY total_ventas DESC;
"""
df_ventas_categoria = pd.read_sql(query_ventas_categoria, engine)
fig4 = px.pie(df_ventas_categoria, names='categoria', values='total_ventas', title='Ventas por Categoría')
fig4.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)

# 5. Gráfico de Ingresos Mensuales
query_ingresos_mensuales = """
SELECT YEAR(fecha) as anio, MONTH(fecha) as mes, SUM(monto) as total_ingresos
FROM notaventa
GROUP BY YEAR(fecha), MONTH(fecha)
ORDER BY anio, mes;
"""
df_ingresos_mensuales = pd.read_sql(query_ingresos_mensuales, engine)
df_ingresos_mensuales['fecha'] = pd.to_datetime(df_ingresos_mensuales['anio'].astype(str) + '-' + df_ingresos_mensuales['mes'].astype(str) + '-01')
fig5 = px.bar(df_ingresos_mensuales, x='fecha', y='total_ingresos', title='Ingresos Mensuales')
fig5.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)


# 1. Gráfico de barras: Ventas totales por cliente
query_ventas_cliente = """
SELECT cl.nombre AS cliente, SUM(nv.monto) AS total_ventas
FROM notaventa nv
JOIN cliente cl ON nv.id_cliente = cl.id_cliente
GROUP BY cl.nombre
ORDER BY total_ventas DESC;
"""
df_ventas_cliente = pd.read_sql(query_ventas_cliente, engine)
fig6 = px.bar(df_ventas_cliente, x='cliente', y='total_ventas', title='Ventas Totales por Cliente')
fig6.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)
# fig6.show()
# 2. Gráfico de líneas: Ventas totales a lo largo del tiempo
query_ventas_tiempo = """
SELECT nv.fecha, SUM(nv.monto) AS total_ventas
FROM notaventa nv
GROUP BY nv.fecha
ORDER BY nv.fecha;
"""
df_ventas_tiempo = pd.read_sql(query_ventas_tiempo, engine)
fig7 = px.line(df_ventas_tiempo, x='fecha', y='total_ventas', title='Ventas Totales a lo Largo del Tiempo')
fig7.update_layout(
    plot_bgcolor='rgba(130,50,15,80)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="red"),
)
# fig7.show()
# 3. Gráfico de dispersión: Relación entre precio y stock de productos
query_precio_stock = """
SELECT descripcion, precio, stock
FROM producto;
"""
df_precio_stock = pd.read_sql(query_precio_stock, engine)
fig8 = px.scatter(df_precio_stock, x='precio', y='stock', text='descripcion',
                  title='Relación entre Precio y Stock de Productos')
fig8.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)
# fig8.show()
# 4. Mapa de calor: Ventas por mes y categoría
query_calor_categoria_mes = """
SELECT MONTH(nv.fecha) AS mes, cat.nombre AS categoria, SUM(dv.cantidad * dv.preciov) AS total_ventas
FROM notaventa nv
JOIN detalleventa dv ON nv.id_venta = dv.id_venta
JOIN producto p ON dv.id_producto = p.id_producto
JOIN categoria cat ON p.id_categoria = cat.id_categoria
GROUP BY MONTH(nv.fecha), cat.nombre;
"""
df_calor_categoria_mes = pd.read_sql(query_calor_categoria_mes, engine)
df_calor_pivot = df_calor_categoria_mes.pivot(index='mes', columns='categoria', values='total_ventas').fillna(0)
fig9 = px.imshow(df_calor_pivot, labels=dict(x="Categoría", y="Mes", color="Ventas Totales"),
                 title="Ventas por Mes y Categoría")
fig9.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)
# fig9.show()
# 5. Gráfico de barras apiladas: Cantidad de productos vendidos por categoría
query_productos_vendidos_categoria = """
SELECT cat.nombre AS categoria, SUM(dv.cantidad) AS cantidad_vendida
FROM detalleventa dv
JOIN producto p ON dv.id_producto = p.id_producto
JOIN categoria cat ON p.id_categoria = cat.id_categoria
GROUP BY cat.nombre
ORDER BY cantidad_vendida DESC;
"""
df_productos_vendidos_categoria = pd.read_sql(query_productos_vendidos_categoria, engine)
fig10 = px.bar(df_productos_vendidos_categoria, x='categoria', y='cantidad_vendida', title='Cantidad de Productos Vendidos por Categoría')
fig10.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color="white"),
)
# fig10.show()

# Creación de la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Gradiente de fondo y estilo glassmorphism para cada figura
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("Reportes de Ventas", className="text-center text-white mb-4"),
                html.P("Visualiza los datos y estadísticas de ventas en tiempo real.", className="text-center text-white mb-4"),
            ]),
            width=12,
            className="my-4",
            style={
                # "background": "linear-gradient(90deg, rgba(54, 9, 121, 1) 0%, rgba(0, 212, 255, 1) 100%)",
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.2)",  # Fondo semi-transparente
                "padding": "20px",
                "borderRadius": "8px"
            }
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig1),
            width=5,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",  # Fondo semi-transparente
                "borderRadius": "8px",
                "margin": "10px"
            }
        ),
        dbc.Col(
            dcc.Graph(figure=fig2),
            width=6,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",

                "margin": "10px"
            }
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig3),
            width=6,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",
                # "padding": "15px",
                "margin": "10px"
            }
        ),
        dbc.Col(
            dcc.Graph(figure=fig4),
            width=5,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",
                # "padding": "15px",
                "margin": "10px"
            }
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig5),
            width=6,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",
                # "padding": "15px",
                # "margin": "10px"
                "margin": "10px"
            }
        ),
        dbc.Col(
            dbc.Card(
                dash_table.DataTable(
                    data=df_ventas_categoria.to_dict('records'),
                    page_size=10,
                    style_cell={
                        'backgroundColor': 'rgba(40, 40, 40, 0.7)',
                        'color': 'white',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                        'textAlign': 'center'
                    },
                    style_header={
                        'backgroundColor': 'rgba(60, 60, 60, 0.8)',
                        'color': 'cyan',
                        'fontWeight': 'bold',
                        'border': '1px solid rgba(255, 255, 255, 0.2)'
                    },
                    style_table={
                        'overflowX': 'auto'
                    }
                ),
                body=True,
                style={
                    "backdropFilter": "blur(15px)",
                    "backgroundColor": "rgba(0, 0, 0, 0.4)",
                    "borderRadius": "8px",
                    # "padding": "15px",
                    "margin": "10px"
                }
            ),
            width=5
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig6),
            width=4,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",  # Fondo semi-transparente
                "borderRadius": "8px",
                "margin": "10px"
            }
        ),
        dbc.Col(
            dcc.Graph(figure=fig7),
            width=4,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",

                "margin": "10px"
            }
        ),
        dbc.Col(
            dcc.Graph(figure=fig8),
            width=3,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",

                "margin": "10px"
            }
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig9),
            width=6,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",
                # "padding": "15px",
                # "margin": "10px"
                "margin": "10px"
            }
        ),
        dbc.Col(
            dcc.Graph(figure=fig10),
            width=5,
            style={
                "backdropFilter": "blur(15px)",
                "backgroundColor": "rgba(0, 0, 0, 0.4)",
                "borderRadius": "8px",
                # "padding": "15px",
                # "margin": "10px"
                "margin": "10px"
            }
        ),
    ]),
], fluid=True, style={
                     "background": "radial-gradient(circle at 25% 25%, #0088B3, #001A66 35%, #3A226B 70%, #050015)",
                     "padding": "50px",
                     "borderRadius": "8px"
                     }
)

if __name__ == '__main__':
    app.run_server(debug=True)