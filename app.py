import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
import flask
import os

server = app.server

# Gapminder dataset GAPMINDER.ORG, CC-BY LICENSE
df = pd.read_csv("df.csv", index_col=0)
df_years = pd.read_csv("yearly.csv", index_col=0)
# Dash app
app = dash.Dash()
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Utility functions
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app.layout = html.Div([
    html.H1('Анализ содержания загрязняющих веществ в водных объектах',
    ),

    dcc.Markdown("""В ежемесячном режиме осуществляется мониторинг содержания загрязняющих 
        веществ в водных объектах Тюменской области в части выявления превышений предельных 
        допустимых концентраций по сведениям, предоставленным Тюменским центром по гидрометеорологии 
        и мониторингу окружающей среды – филиалом ФГБУ «Обь-Иртышское управление по 
        гидрометеорологии и мониторингу окружающей среды».
        Ниже приведен пример обработанного набора данных (0: нет ПДК, 1: ПДК):
        """
    ),
    generate_table(df.sample(5)),
    dcc.Dropdown(
        id='river-dropdown',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph'),

    dcc.Dropdown(
        id='river-dropdown1',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph1'),

    dcc.Dropdown(
        id='river-dropdown2',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph2'),

    dcc.Dropdown(
        id='river-dropdown3',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph3'),

    dcc.Dropdown(
        id='river-dropdown4',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph4'),

    dcc.Dropdown(
        id='river-dropdown5',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph5'),

    dcc.Dropdown(
        id='river-dropdown6',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph6'),

    dcc.Dropdown(
        id='river-dropdown7',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph7'),

    dcc.Dropdown(
        id='river-dropdown8',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph8'),

    dcc.Dropdown(
        id='river-dropdown9',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph9'),

    dcc.Dropdown(
        id='river-dropdown10',
        options=[{'label': i, 'value': i} for i in df["Наименование водного объекта"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph10'),

    html.H1("Анализ распределения химических веществ", style={"textAlign": "center"}), dcc.Markdown('''
Ниже представлено распределение по общему содержанию загрязняющих веществ в водных объектах Тюменской области.'''),
    html.Div([
        html.Div([
            html.H3('ПДК химических веществ по рекам 2015-20'),
            dcc.Graph(id='g1', figure={'data': [{"x":['р. Ишим, в створе с. Абатское',
                                                     'р. Тура, в створе с. Покровское',
                                                     'р. Тобол, ниже г. Ялуторовска',
                                                     'р. Ишим, в створе с. Ильинское',
                                                     'р. Ишим, выше г. Ишима',
                                                     'р. Тобол, в створе с. Коркино',
                                                     'р. Ишим, ниже г. Ишима',
                                                     'р. Тура, ниже г. Тюмени',
                                                     'р. Тура, выше г. Тюмени',
                                                     'р. Тобол, выше г. Ялуторовска',
                                                     'р. Тура, в створе с. Салаирка',
                                                     'р. Тобол, в створе с. Иевлево'], 
              'y': [45, 50, 114, 85, 89, 96, 93, 125, 126, 114, 133, 48], 'type': 'bar'}]})
        ], className="six columns"),

        html.Div([
            html.H3('Общее количество химических веществ 2015-20'),
            dcc.Graph(id='g2', figure={'data': [{'x': ['Азот нитритный',
                                                       'Азот аммонийный',
                                                       'Азот нитратный',
                                                       'Фенол',
                                                       'Нефтепродукты',
                                                       'Органические вещества (по ХПК)',
                                                       'Железо',
                                                       'Медь',
                                                       'Цинк',
                                                       'Марганец',
                                                       'БПК5'],
 "y": [171, 282, 0, 243, 256, 233, 21, 38, 0, 39, 6], "type": "bar"}]})
        ], className="six columns"),
    ], className="row"),

    html.H1("Тренд ПДК по годам", style={"textAlign": "center"}), dcc.Markdown('''
Распределение суммарного зафиксированных ПДК по годам.'''),

    dcc.Dropdown(
        id='river-dropdown11',
        options=[{'label': i, 'value': i} for i in df_years["River"].unique()],
        multi=True,
        value=['р. Тура, ниже г. Тюмени']
    ),
    dcc.Graph(id='timeseries-graph11'),

])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    [dash.dependencies.Input('river-dropdown', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Азот нитритный'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Азот нитритный",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph1', 'figure'),
    [dash.dependencies.Input('river-dropdown1', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Азот аммонийный'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Азот аммонийный",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph2', 'figure'),
    [dash.dependencies.Input('river-dropdown2', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Азот нитратный'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Азот нитратный",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph3', 'figure'),
    [dash.dependencies.Input('river-dropdown3', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Фенол'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Фенол",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph4', 'figure'),
    [dash.dependencies.Input('river-dropdown4', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]["Нефтепродукты"],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Нефтепродукты",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph5', 'figure'),
    [dash.dependencies.Input('river-dropdown5', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Органические вещества (по ХПК)'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Органические вещества (по ХПК)",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph6', 'figure'),
    [dash.dependencies.Input('river-dropdown6', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Железо'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Железо",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph7', 'figure'),
    [dash.dependencies.Input('river-dropdown7', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Медь'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Медь",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph8', 'figure'),
    [dash.dependencies.Input('river-dropdown8', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Цинк'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Цинк",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph9', 'figure'),
    [dash.dependencies.Input('river-dropdown9', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['Марганец'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="Марганец",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph10', 'figure'),
    [dash.dependencies.Input('river-dropdown10', 'value')])
def update_graph(river_values):
    dff = df.loc[df["Наименование водного объекта"].isin(river_values)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Наименование водного объекта'] == river]['Период наблюдений'],
            y=dff[dff['Наименование водного объекта'] == river]['БПК5'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            mode='lines+markers',
            name=river,
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for river in dff['Наименование водного объекта'].unique()],

        'layout': go.Layout(
            height=250,
            title="БПК5",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК', "tickvals": [0,1]},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('timeseries-graph11', 'figure'),
    [dash.dependencies.Input('river-dropdown11', 'value')])
def update_graph(river_values):
    dff = df_years.loc[df_years["River"].isin(river_values)]

    return {
        'data': [go.Bar(
            x=dff[dff['River'] == river]['Year'],
            y=dff[dff['River'] == river]['Value'],
            #text="Continent: " +
            #      f"{dff[dff['Наименование водного объекта'] == river]['continent'].unique()[0]}",
            #mode='lines+markers',
            name=river
            #marker={
            #    'size': 15,
            #    'opacity': 0.5,
            #    'line': {'width': 0.5, 'color': 'white'}
            #}
        ) for river in dff['River'].unique()],

        'layout': go.Layout(
            height=500,
            title="Общее количество ПДК",
            xaxis={'title': 'Период наблюдений'},
            yaxis={'title': 'ПДК'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.server.run(debug=True, threaded=True)
