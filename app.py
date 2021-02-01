import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import date
from plotly.subplots import make_subplots
import os
import base64
import dash_table


PORT = 8051
HOST = "10.10.28.22"

logo = "assets/logo.jpg"
legend = "assets/legend.png"
encoded_image = base64.b64encode(open(logo, "rb").read())
legend_image = base64.b64encode(open(legend, "rb").read())
rivers = [
    "р. Ишим, выше г. Ишима",
    "р. Ишим, ниже г. Ишима",
    "р. Ишим, створ с. Абатское",
    "р. Ишим, створ с. Ильинское",
    "р. Тобол, выше г. Ялуторовска",
    "р. Тобол, ниже г. Ялуторовска",
    "р. Тобол, створ с. Иевлево",
    "р. Тобол, створ с. Коркино",
    "р. Тура, выше г. Тюмени",
    "р. Тура, ниже г. Тюмени",
    "р. Тура, створ с. Покровское",
    "р. Тура, створ с. Салаирка"
]
location_dic = {
    "р. Ишим, створ с. Абатское": ["56.296329", "70.492232", "#33FF66"],
    "р. Ишим, ниже г. Ишима": ["56.107748", "69.596043", "#33CC99"],
    "р. Ишим, выше г. Ишима": ["56.056316", "69.432672", "#43A047"],
    "р. Ишим, створ с. Ильинское": ["55.458001", "69.325830", "#006633"],
    "р. Тобол, створ с. Иевлево": ["57.559170", "67.172391", "#FDD835"],
    "р. Тобол, ниже г. Ялуторовска": ["56.710275", "66.395237", "#FFB300"],
    "р. Тобол, выше г. Ялуторовска": ["56.610472", "66.296407", "#EF6C00"],
    "р. Тобол, створ с. Коркино": ["56.085409", "65.929293", "#BF360C"],
    "р. Тура, створ с. Салаирка": ["57.369730", "65.014416", "#1A237E"],
    "р. Тура, выше г. Тюмени": ["57.240366", "65.428346", "#1565C0"],
    "р. Тура, ниже г. Тюмени": ["57.103945", "65.789079", "#039BE5"],
    "р. Тура, створ с. Покровское": ["57.236938", "66.785980", "#29B6F6"]
}
chemicals = [
    "Азот нитритный",
    "Азот аммонийный",
    "Азот нитратный",
    "Фенол",
    "Нефтепродукты",
    "Органические вещества (по ХПК)",
    "Железо",
    "Медь",
    "Цинк",
    "Марганец",
    "БПК5"
]
months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]
months_dic = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}
source = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,  
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12
]
target = [
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
    13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13
]
out_df = pd.DataFrame(
    {
        "Аббревиатура": ["ВПН", "НЗ", "ВЗ", "ЭВЗ"],
        "Числовой код": [0, 1, 2, 3],
        "Расшифровка": ["В пределах нормы",
                        "Незначительное загрязнение",
                        "Высокое загрязнение",
                        "Экстремально высоким загрязнением"]
        }
)
rivers_list = [
    "р. Тура, створ с. Салаирка", 
    "р. Тура, выше г. Тюмени", 
    "р. Тура, ниже г. Тюмени", 
    "р. Тура, створ с. Покровское", 
    "р. Тобол, створ с. Коркино", 
    "р. Тобол, выше г. Ялуторовска", 
    "р. Тобол, ниже г. Ялуторовска", 
    "р. Тобол, створ с. Иевлево", 
    "р. Тобол", 
    "р. Ишим, створ с. Ильинское", 
    "р. Ишим, выше г. Ишима", 
    "р. Ишим, ниже г. Ишима", 
    "р. Ишим, створ с. Абатское", 
    "р. Ишим"
]
colours = [
    "#9acd32",
    "#7fffd4",
    "#ffe4c4",
    "#8a2be2",
    "#000000",
    "#8fbc8f",
    "#8b4513",
    "#708090",
    "#d2b48c",
    "#1977d6",
    "#ff4500",
]
color_dict = {
    "Азот нитритный": "#9acd32",
    "Азот аммонийный": "#7fffd4",
    "Азот нитратный": "#ffe4c4",
    "Фенол": "#8a2be2",
    "Нефтепродукты": "#000000",
    "Органические вещества (по ХПК)": "#8fbc8f",
    "Железо": "#8b4513",
    "Медь": "#708090",
    "Цинк": "#d2b48c",
    "Марганец": "#1977d6",
    "БПК5": "#ff4500",
}
PDK = {
    "Азот нитритный": [10, 50],
    "Азот аммонийный": [10, 50],
    "Азот нитратный": [10, 50],
    "Фенол": [30, 50],
    "Нефтепродукты": [30, 50],
    "Органические вещества (по ХПК)": [10, 50],
    "Железо": [30, 50],
    "Медь": [30, 50],
    "Цинк": [10, 50],
    "Марганец": [30, 50],
    "БПК5": [5, 20]
}
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets)

def reader(csv):
    df = pd.read_csv(csv, encoding="cp1251", delimiter=";")
        
    for chem in ["Медь"]:
        df[chem] = df[chem].apply(lambda x: x.replace(",", "."))
        for row in range(len(df)):
            value = df.loc[row, chem]
            if (value=="в пределах нормы") or (value=="В пределах нормы ") or (value=="В пределах нормы"):
                df.loc[row, chem] = "0"
            elif (value=="Выше нормы") or (value=="выше ПДК ") or (value=="Выше ПДК") or (value=="выше ПДК"):
                df.loc[row, chem] = "1"
            elif (value==" ") or (value=="-"):
                df.loc[row, chem] = "0"
            elif (float(value)>=PDK[chem][0]) and (float(value)<=PDK[chem][1]):
                df.loc[row, chem] = "2"
            elif (float(value)>PDK[chem][1]):
                df.loc[row, chem] = "3"
            else:
                df.loc[row, chem] = "1"
        df[chem] = pd.to_numeric(df[chem], errors='coerce')
        
    for i in range(len(df)):
        df.iloc[i, 1] = df.iloc[i, 1].replace(", ПДК", "")
        df.iloc[i, 1] = df.iloc[i, 1].replace(", превышение ПДК", "")
        df.iloc[i, 1] = df.iloc[i, 1].replace("в створе", "створ")
        if df.iloc[i, 1] == "р. Тобол, с. Иевлево":
            df.iloc[i, 1] = "р. Тобол, створ с. Иевлево"
    
    df = df.loc[df['Наименование водного объекта'] != ' ']
    df["Год"] = pd.DatetimeIndex(df["Период наблюдений"]).year
    df["Месяц"] = pd.DatetimeIndex(df["Период наблюдений"]).month
    df["Период наблюдений"] = pd.to_datetime(df["Период наблюдений"]).dt.to_period('M')
    df = df.sort_values(by=["Период наблюдений"])
    df.reset_index(drop=True)
    return df

df = reader("7202136720.76.2.csv")
years = df.groupby("Год").nunique().index.to_list()

# Associating server
server = app.server
app.title = "Мониторинг загрязнения водных объектов"
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        html.Div([
            html.Img(
                src="data:image/png;base64,{}".format(encoded_image.decode()),
                style={
                    "display": "inline-block",
                    "height": "50px"
                }
            ),
            html.Div(
                "Мониторинг загрязнения водных объектов Тюменской области",
                style={
                    "display": "inline-block",
                    "font-size": "30px"
                }
            ),
        ]),
        html.Div(
            """
            В Тюменской области режимные наблюдения за качеством 
            поверхностных вод организованы на 12-ти створах 
            3-х водных объектов: р. Тура, Тобол и Ишим.
            Анализ включает в себя 12 наименований физико-химических веществ: 
            взвешенные и органические вещества, биогенные элементы (соединения азота и фосфора), 
            металлы, нефтепродукты и другие.
            Ниже представлена гистограмма с уровнем загрязнения водных объектов (Установите желаемые тип загрязнения, створ реки и период наблюдения).
            """, 
            style={
                "display": "inline-block",
                "font-size": "16px",
                "padding": "5px",
                "margin-left": "2px"
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                           html.Div(
                                [
                                    html.P("Выберите химические вещество(а):", 
                                           style={
                                               "height": "auto",
                                               "margin-bottom": "auto",
                                               "font-weight": "bold",
                                               "margin-left": "5px"
                                            }
                                    ),
                                    
                                    dcc.Dropdown(
                                        id="chemicals_dropdown_b",
                                        options=[{"label" : i, "value" : i} for i in chemicals],
                                        multi=True,
                                        value=["Нефтепродукты"],
                                    ),            
                                ]
                            )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.P("Выберите створ реки и период наблюдения:",
                                       style={
                                           "height": "auto",
                                           "margin-bottom": "auto",
                                           "font-weight": "bold"
                                        }
                                ),
                                dbc.Row(
                                    [
                                        dcc.Dropdown(
                                            id="river_dropdown_b",
                                            options=[{"label": i, "value": i} for i in rivers],
                                            multi=False,
                                            placeholder="Выберите створ реки:",
                                            style={
                                                "width": "300px",
                                                "display": "inline-block"
                                            },
                                            value="р. Тура, створ с. Салаирка",
                                        ),
                                        dcc.Dropdown(
                                            id="months_sb",
                                            options=[{"label" : i, "value" : i} for i in months],
                                            multi=False,
                                            value="Январь",
                                            placeholder="Выберите месяц:",
                                            style={
                                                "width": "130px",
                                                "display": "inline-block"
                                            }
                                        ),
                                        dcc.Dropdown(
                                            id="months_eb",
                                            options=[{"label" : i, "value" : i} for i in months],
                                            multi=False,
                                            value="Декабрь",
                                            placeholder="Выберите месяц:",
                                            style={
                                                "width": "130px",
                                                "display": "inline-block"
                                            }
                                        ),
                                        dcc.Dropdown(
                                            id="years_b",
                                            options=[{"label" : i, "value" : i} for i in years],
                                            multi=False,
                                            value=2015,
                                            placeholder="Выберите год:",
                                            style={
                                                "width": "130px",
                                                "display": "inline-block"
                                            }
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                
                dbc.Col(
                    [
                        dcc.Graph(id="timeseries-graph_3")
                    ],
                ),
            ]
        ),
        html.Div(
            """
            Ниже представлена карта с 12-ти створами со степенью загрязнения и
            диаграммой распространения химических вещевств между ними. 
            Видимость створов на карте регулируется нажатием на него (одно нажатие - отключить видимость, двойное нажатие - выделение), используя легенду.
            В правом верхнем углу карты можете сохранить изогражение (иконка "камеры"), 
            восстановить карту в исходное положение (иконка "домика") и т.д.
            """, 
            style={
                "display": "inline-block",
                "font-size": "16px",
                "padding": "5px",
                "margin-left": "2px"
            }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                           html.Div(
                                [
                                    html.P("Выберите химические вещество(а):", 
                                           style={
                                               "height": "auto",
                                               "margin-bottom": "auto",
                                               "font-weight": "bold",
                                               "margin-left": "5px"
                                            }
                                    ),
                                    
                                    dcc.Dropdown(
                                        id="chemicals_dropdown",
                                        options=[{"label" : i, "value" : i} for i in chemicals],
                                        multi=True,
                                        value=["Азот нитритный"],
                                    ),            
                                ]
                            )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.P("Выберите период наблюдения:",
                                       style={
                                           "height": "auto",
                                           "margin-bottom": "auto",
                                           "font-weight": "bold"
                                        }
                                ),
                                dbc.Row(
                                    [
                                        dcc.Dropdown(
                                            id="months_0",
                                            options=[{"label" : i, "value" : i} for i in months],
                                            multi=False,
                                            placeholder="Выберите месяц:",
                                            style={
                                                "width": "300px",
                                                "display": "inline-block"
                                            },
                                            value="Январь",
                                        ),
                                        dcc.Dropdown(
                                            id="years_0",
                                            options=[{"label" : i, "value" : i} for i in years],
                                            multi=False,
                                            placeholder="Выберите год:",
                                            style={
                                                "width": "260px",
                                                "display": "inline-block"
                                            },
                                            value=2015,
                                        ),
                                    ],
                                ),
                            ]
                        )
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="map"),
                    ]
                ),
            ]
        ),
        html.P("Визуализация потока загрязняющих веществ между створами со степенью загрязнения:",
                        style={
                           "height": "auto",
                           "margin-bottom": "auto",
                           "font-weight": "bold",
                           "margin-left": "5px"
                        }
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="sankey"),
                    ],
                )
            ]
        ),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                                "Расшифровка условных обозначений:",
                                style={
                                    "font-size": "16px",
                                    "margin-bottom": "30px",
                                    "margin-left": "5px"
                                }
                        ),
                        dash_table.DataTable(
                            id='table1',
                            columns=[{"name": i, "id": i} for i in out_df.columns],
                            data=out_df.to_dict('records'),
                            style_table={
                                'maxHeight': '50ex',
                                'overflowY': 'scroll',
                                'width': '100%',
                                'minWidth': '100%',
                            },
                            style_cell={
                                'fontFamily': 'Open Sans',
                                'textAlign': 'center',
                                'height': '10px',
                                'padding': '2px 22px',
                                'whiteSpace': 'inherit',
                                "size": 10,
                            },
                            style_header={
                                'fontWeight': 'bold',
                                'backgroundColor': 'white',
                            },
                            style_data_conditional=[
                                {
                                    # stripped rows
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                },
                                {
                                    # highlight one row
                                    'if': {'row_index': 4},
                                    "backgroundColor": "#3D9970",
                                    'color': 'white'
                                }
                            ],
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Div(
                                        "Цветовая схема загрязняющих веществ:",
                                        style={
                                            "font-size": "16px",
                                        }
                                ),
                                html.Img(
                                    src="data:image/png;base64,{}".format(legend_image.decode()),
                                    style={
                                        "height": "200px"
                                    }
                                )
                            ]
                        ),
                    ]
                ),
            ]
        ),
        dcc.Markdown("Ниже представлена диаграмма динамики изменения загрязнения водных объектов для сравнения в установленные временные промежутки:",
                     style={"margin-left": "6px"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="timeseries-graph_2")
                    ], width=8
                ),
                dbc.Col(
                    [
                        html.P("Выберите период наблюдения для верхнего графика:",
                               style={
                                   "height": "auto",
                                   "margin-bottom": "auto",
                                   "font-weight": "bold"
                                }
                        ),
                        dcc.Dropdown(
                            id="months_11",
                            options=[{"label" : i, "value" : i} for i in months],
                            multi=False,
                            value="Январь",
                            style={
                                "width": "150px",
                                "display": "inline-block"
                            }
                        ),
                        dcc.Dropdown(
                            id="months_12",
                            options=[{"label" : i, "value" : i} for i in months],
                            multi=False,
                            value="Декабрь",
                            style={
                                "width": "150px",
                                "display": "inline-block"
                            }
                        ),
                        dcc.Dropdown(
                            id="years_1",
                            options=[{"label" : i, "value" : i} for i in years],
                            multi=False,
                            value=2015,
                            style={
                                "width": "150px",
                                "display": "inline-block"
                            }
                        ),
                        html.P(
                            "Выберите период наблюдения для нижнего графика:",
                            style={
                                "height": "auto",
                                "margin-bottom": "auto",
                                "font-weight": "bold"
                            }
                        ),
                        dcc.Dropdown(
                            id="months_21",
                            options=[{"label" : i, "value" : i} for i in months],
                            multi=False,
                            value="Январь",
                            style={
                                "width": "150px",
                                "display": "inline-block"
                            }
                        ),
                        dcc.Dropdown(
                            id="months_22",
                            options=[{"label" : i, "value" : i} for i in months],
                            multi=False,
                            value="Декабрь",
                            style={
                                "width": "150px",
                                "display": "inline-block"
                            }
                        ),
                        dcc.Dropdown(
                            id="years_2",
                            options=[{"label" : i, "value" : i} for i in years],
                            multi=False,
                            value=2016,
                            style={
                                "width": "150px",
                                "display": "inline-block"
                            }
                        ), 
                        html.P(
                            "Выберите химические вещество(а):",
                            style={
                                "height": "auto",
                                "margin-bottom": "auto",
                                "font-weight": "bold"
                            }
                        ),
                        dcc.Dropdown(
                            id="chemicals_dropdown_2",
                            options=[{"label": i, "value": i} for i in chemicals],
                            multi=True,
                            value=["Нефтепродукты"],
                        ),
                        html.P(
                            "Выберите створ реки:",
                            style={"height": "auto",
                                   "margin-bottom": "auto",
                                   "font-weight": "bold"}
                        ),
                        dcc.Dropdown(
                            id="river_dropdown_2",
                            options=[{"label": i, "value": i} for i in rivers],
                            multi=False,
                            value="р. Тура, створ с. Салаирка",
                        ),

                    ]
                )
            ]
        ),
        html.Center(
            [
                html.A("Made with \u2764\ufe0f by Xrenya",
                        href="https://xrenya.github.io",
                        style=dict(color="#34495E")
                )
            ], style=dict(marginTop="30px")
        )
    ]
)

def map_plot(df, chemicals):
    fig = go.Figure()
    for river in rivers:
        hover = []
        for chem in chemicals:
            val = df[df["Наименование водного объекта"]==river][chem].to_list()
            hover.append(f"{chem}: {val}")
            hovertemplate="<br>".join(hover)
        fig.add_trace(go.Scattermapbox(
            lat=[location_dic[river][0]],
            lon=[location_dic[river][1]],
            mode='markers',
            marker=dict(size=df[df["Наименование водного объекта"]==river][chemicals].sum(axis=1)*10, color=location_dic[river][2]),
            textfont=dict(size=16, color='black'),
            name=river,
            hovertext=hovertemplate,
    ))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
        mapbox=dict(
            center=go.layout.mapbox.Center(lat=56.6, lon=68),
            zoom=6
        )
    )
    return fig
@app.callback(
    Output("map", "figure"),
    [Input("chemicals_dropdown", "value"),
     Input("months_0", "value"),
     Input("years_0", "value")],
)
def map_update(chemicals, month, year):
    df["Месяц"] = df["Месяц"].replace(months_dic)
    df_selected = df[(df["Год"] == year) & (df["Месяц"] == month)]
    fig = map_plot(df_selected, chemicals)
    return fig

@app.callback(
    Output("sankey", "figure"),
    [Input("months_0", "value"),
     Input("years_0", "value")],
)
def sankey_update(month, year):
    values = []
    df["Месяц"] = df["Месяц"].replace(months_dic)
    df_selected = df[(df["Год"] == year) & (df["Месяц"] == month)]
    for river in rivers_list:
        try:
            values.append(df_selected[df_selected["Наименование водного объекта"]==river].iloc[0, 2:13].to_list())
        except:
            values.append(np.full(11, 0))

    fig = go.Figure(
        data = [go.Sankey(
            node = dict(
                pad = 30,
                thickness = 2,
                line = dict(color = "black", width = 0.2),
                label = rivers_list,
                customdata = rivers_list,
                hovertemplate="%{customdata} имеет общее кол-во превышении %{value}<extra></extra>",
                color = "#049CE0"
            ),
            link = dict(
                source = source,
                target = target,
                value = np.array(values).flatten(),
                label = chemicals*14,
                color = colours*14,
            )
        )]
    )
    fig.update_layout(
        title_text="Диаграмма распространения химических вещевств", 
        font={
            "size": 10,
            "color": "white"
        }
    )
    return fig

def plots(df_1, df_2, chemicals, period_1, period_2):
    count = 0
    plot_1 = []
    plot_2 = []
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f"{period_1}", f"{period_2}"))
    if isinstance(chemicals, str):
        plot_1 = go.Bar(
            x=df_1["Месяц"],
            y=df_1[chemicals],
            name=chemicals,
            marker_color=color_dict[chemicals]
        )
        plot_2 = go.Bar(
            x=df_2["Месяц"],
            y=df_2[chemicals],
            name=chemicals,
            marker_color=color_dict[chemicals],
            showlegend=False,
        )
        fig.add_trace(plot_1, 1, 1)
        fig.add_trace(plot_2, 2, 1)
    if isinstance(chemicals, list):
        for chem in chemicals:
            plot_1.append(f"trace_{count}")
            plot_1[count] = go.Bar(
                x=df_1["Месяц"],
                y=df_1[chem],
                name=chem,
                marker_color=color_dict[chem]
            )
            plot_2.append(f"trace_{count}")
            plot_2[count] = go.Bar(
                x=df_2["Месяц"],
                y=df_2[chem],
                name=chem,
                marker_color=color_dict[chem],
                showlegend=False,
            )
            fig.add_trace(plot_1[count], 1, 1)
            fig.add_trace(plot_2[count], 2, 1)
            count+=1
    return fig
@app.callback(
    Output("timeseries-graph_2", "figure"),
    [Input("months_11", "value"),
     Input("months_12", "value"),
     Input("years_1", "value"),
     Input("months_21", "value"),
     Input("months_22", "value"),
     Input("years_2", "value"),
     Input("river_dropdown_2", "value"),
     Input("chemicals_dropdown_2", "value")]
)
def update_output(start_month1, end_month1, year1, start_month2, end_month2, year2, river_data, chemical):
    index_1 = months[months.index(start_month1):months.index(end_month1)+1]
    index_2 = months[months.index(start_month2):months.index(end_month2)+1]
    df_river = df[df["Наименование водного объекта"]==river_data]
    df_river["Месяц"] = df_river["Месяц"].replace(months_dic)
    selected_1 = df_river[df_river["Месяц"].isin(index_1)]
    df_time1 = selected_1[selected_1["Год"]==year1]
    selected_2 = df_river[df_river["Месяц"].isin(index_2)]
    df_time2 = selected_2[selected_2["Год"]==year2]
    period_1 = f"{start_month1}-{end_month1} {year1}"
    period_2 = f"{start_month2}-{end_month2} {year2}"
    fig = plots(df_time1.reset_index(drop=True), df_time2.reset_index(drop=True), chemical, period_1, period_2)
    fig.update_layout(
        yaxis1 = dict(
            tickmode = "array",
            tickvals = [0, 1, 2, 3],
            ticktext = ["ВПН", "НЗ", "ВЗ", "ЭВЗ"]),
        margin={"r": 0,"t": 20,"l": 50,"b": 0},
        #width=900
    )
    fig.update_layout(
        yaxis2 = dict(
            tickmode = "array",
            tickvals = [0, 1, 2, 3],
            ticktext = ["ВПН", "НЗ", "ВЗ", "ЭВЗ"]),
        margin={"r": 0,"t": 20,"l": 50,"b": 0},
        #width=900
    )
    fig.update_yaxes(range=[0, 3], row=1, col=1)
    fig.update_yaxes(range=[0, 3], row=2, col=1)
    return fig
def main_plot(df_1, chemicals):
    count = 0
    plot_1 = []
    fig = go.Figure()
    if isinstance(chemicals, str):
        plot_1 = go.Bar(
            x=df_1["Месяц"],
            y=df_1[chemicals],
            name=chemicals,
            marker_color=color_dict[chemicals]
        )
        fig.add_trace(plot_1)
    if isinstance(chemicals, list):
        for chem in chemicals:
            plot_1.append(f"trace_{count}")
            plot_1[count] = go.Bar(
                x=df_1["Месяц"],
                y=df_1[chem],
                name=chem,
                marker_color=color_dict[chem]
            )
            fig.add_trace(plot_1[count])
            count+=1
    return fig
@app.callback(
    Output("timeseries-graph_3", "figure"),
    [Input("months_sb", "value"),
     Input("months_eb", "value"),
     Input("years_b", "value"),
     Input("river_dropdown_b", "value"),
     Input("chemicals_dropdown_b", "value")]
)
def update_output(start_month1, end_month1, year1, river_data, chemical):
    print(months[months.index(start_month1):months.index(end_month1)+1])
    index_1 = months[months.index(start_month1):months.index(end_month1)+1]
    df_river = df[df["Наименование водного объекта"]==river_data]
    df_river["Месяц"] = df_river["Месяц"].replace(months_dic)
    selected_1 = df_river[df_river["Месяц"].isin(index_1)]
    df_time1 = selected_1[selected_1["Год"]==year1]
    period_1 = f"{start_month1}-{end_month1} {year1}"
    fig = main_plot(df_time1, chemical)
    fig.update_layout(
        yaxis1 = dict(
            tickmode = "array",
            tickvals = [0, 1, 2, 3],
            ticktext = ["ВПН", "НЗ", "ВЗ", "ЭВЗ"]
        ),
        margin={"r": 30,"t": 30,"l": 30,"b": 0},
        height=300,
    )
    fig.update_yaxes(range=[0, 3])
    fig.update_layout(
        title={
            'text': period_1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(debug=True, port=PORT, host=HOST)
