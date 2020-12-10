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

PORT = 8051

df = pd.read_csv("7202136720.76.2.csv", encoding="cp1251", delimiter=";")

df["Lon"] = 0
df["Lat"] = 0
name = df.columns.to_list()
chemicals = name[2:13]
df_clean = df.copy()
# Make value to 0 if there is not clear whether there is a "ПДК" or "Выше ПДК"
for col in range(2, 13):
    for row in range(len(df_clean)):
        if len(df_clean.iloc[row, col])<=4:
            df_clean.iloc[row, col] = str(df_clean.iloc[row, col]).replace(",", ".")

for col in range(2, 13):
    for row in range(len(df_clean)):
        try:
            if float(df_clean.iloc[row, col])>0:
                df_clean.iloc[row, col] = 1
        except:
            continue

df_clean = df_clean.replace({"в пределах нормы": 0, "В пределах нормы ": 0, "В пределах нормы": 0})
df_clean = df_clean.replace({"Выше нормы": 1, "выше ПДК": 2, "Выше ПДК": 2})
df_clean = df_clean.replace({" ": 0})
df_clean = df_clean.replace({"-": 0})

index = df_clean.loc[df_clean["Наименование водного объекта"] == 0].index.tolist()
df_clean = df_clean.drop(index=index)

for i in range(len(df_clean)):
    df_clean.iloc[i, 1] = df_clean.iloc[i, 1].replace(", ПДК", "")
    df_clean.iloc[i, 1] = df_clean.iloc[i, 1].replace(", превышение ПДК", "")
    if df_clean.iloc[i, 1] == "р. Тобол, с. Иевлево":
        df_clean.iloc[i, 1] = "р. Тобол, в створе с. Иевлево"
    
rivers = df_clean.groupby("Наименование водного объекта")["Номер"].nunique().index.to_list()

location_dict = {
    "р. Ишим, в створе с. Абатское": [56.285047300385344, 70.47371860119425],
    "р. Ишим, в створе с. Ильинское": [55.44978293874859, 69.3301582915707],
    "р. Ишим, выше г. Ишима": [56.07169432110331, 69.43708215838365],
    "р. Ишим, ниже г. Ишима": [56.10577817944233, 69.58405204322325],
    "р. Тобол, в створе с. Иевлево": [57.57166046262647, 67.13838760936815],
    "р. Тобол, в створе с. Коркино": [56.08280026916204, 65.92686257850409],
    "р. Тобол, выше г. Ялуторовска": [56.616536196425926, 66.29641445127238],
    "р. Тобол, ниже г. Ялуторовска": [56.678684490568656, 66.36754361502852],
    "р. Тура, в створе с. Покровское": [57.2357237662492, 66.78950001970463],
    "р. Тура, в створе с. Салаирка": [57.37425356760983, 65.02041300889604],
    "р. Тура, выше г. Тюмени": [57.241179921985605, 65.42449197272792],
    "р. Тура, ниже г. Тюмени": [57.10438605873693, 65.78494851932228],
}
def full(num):
    return np.full(11, num)

source = [full(0), full(1), full(2), full(3), 
          full(4), full(5), full(6), full(7), 
          full(9), full(10), full(11), full(12)]
target = [full(1), full(2), full(3), full(7), 
          full(5), full(6), full(7), full(8), 
          full(10), full(11), full(12), full(13)]
rivers_list = ["р. Тура, в створе с. Салаирка", 
               "р. Тура, выше г. Тюмени", 
               "р. Тура, ниже г. Тюмени", 
               "р. Тура, в створе с. Покровское", 
               "р. Тобол, в створе с. Коркино", 
               "р. Тобол, выше г. Ялуторовска", 
               "р. Тобол, ниже г. Ялуторовска", 
               "р. Тобол, в створе с. Иевлево", 
               "р. Тобол", 
               "р. Ишим, в створе с. Ильинское", 
               "р. Ишим, выше г. Ишима", 
               "р. Ишим, ниже г. Ишима", 
               "р. Ишим, в створе с. Абатское", 
               "р. Ишим"]
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
    "#6a5acd",
    "#ff4500"
]

for i in range(len(df_clean)):
    river_name = df_clean.iloc[i, 1]
    df_clean.iloc[i, 15] = location_dict[river_name][1]
    df_clean.iloc[i, 16] = location_dict[river_name][0]
    
df_time = df_clean.copy()
df_time["Период наблюдений"] = pd.to_datetime(df_time["Период наблюдений"], errors="coerce")
df_time["Период наблюдений"] = df_time["Период наблюдений"].apply(lambda x: str(x).replace(" 00:00:00", ""))
df_time = df_time.sort_values(by=["Период наблюдений"])
df_time.reset_index(drop=True)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets)

# Associating server
server = app.server
app.title = 'Pollution tracker'
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [
        html.H1("Pollution tracker"),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                           html.Div(
                                [
                                    html.P("Select chemicals", style={"height": "auto",
                                                            "margin-bottom": "auto",
                                                            "font-weight": "bold"}
                                    ),
                                    
                                    dcc.Dropdown(
                                        id="chemicals_dropdown",
                                        options=[{"label" : i, "value" : i} for i in chemicals],
                                        multi=True,
                                        value=["Нефтепродукты"],
                                        style=dict(height = "49px")
                                    ),            
                                ]
                            )
                    ]
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.P("Select the date", 
                                        style={"height": "auto",
                                                "margin-bottom": "auto",
                                                "font-weight": "bold"}
                                ),
                                dbc.Row(
                                    [
                                        dcc.DatePickerSingle(
                                            id='my-date-picker-single',
                                            initial_visible_month=date(2015, 1, 20),
                                            display_format='MM Y, DD',
                                            date=date(2015, 1, 20)
                                        ),
                                    ]
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
                    dcc.Graph(id="map"),
                ),
                dbc.Col(
                    [
                        dcc.Graph(id='sankey'),
                    ]
                )
            ]
        ),
        dcc.Markdown("The comparison of pollution level"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='timeseries-graph_2')
                    ], width=8
                ),
                dbc.Col(
                    [
                        html.P("Select the time range for first graphic", 
                                        style={"height": "auto",
                                                "margin-bottom": "auto",
                                                "font-weight": "bold"}
                        ),
                        dcc.DatePickerSingle(
                            id='date_start',
                            initial_visible_month=date(2015, 1, 20),
                            display_format='MM Y, DD',
                            date=date(2015, 1, 20)
                        ),
                        dcc.DatePickerSingle(
                            id='date_end',
                            initial_visible_month=date(2016, 1, 20),
                            display_format='MM Y, DD',
                            date=date(2016, 1, 20)
                        ),
                        html.P("Select the time range for second graphic", 
                                        style={"height": "auto",
                                                "margin-bottom": "auto",
                                                "font-weight": "bold"}
                        ),
                        dcc.DatePickerSingle(
                            id='date_start_1',
                            initial_visible_month=date(2016, 1, 20),
                            display_format='MM Y, DD',
                            date=date(2016, 1, 20)
                        ),
                        dcc.DatePickerSingle(
                            id='date_end_1',
                            initial_visible_month=date(2017, 1, 20),
                            display_format='MM Y, DD',
                            date=date(2017, 1, 20)
                        ),
                        html.P("Select the chemical", 
                                        style={"height": "auto",
                                                "margin-bottom": "auto",
                                                "font-weight": "bold"}
                        ),
                        dcc.Dropdown(
                            id='chemicals_dropdown_2',
                            options=[{'label': i, 'value': i} for i in chemicals],
                            multi=False,
                            value="Нефтепродукты",
                        ),
                        html.P("Select the river", 
                                        style={"height": "auto",
                                                "margin-bottom": "auto",
                                                "font-weight": "bold"}
                        ),
                        dcc.Dropdown(
                            id='river_dropdown_2',
                            options=[{'label': i, 'value': i} for i in rivers],
                            multi=False,
                            value="р. Тура, ниже г. Тюмени",
                        ),

                    ]
                )
            ]
        )
    ]
)


@app.callback(
    Output("map", "figure"),
    [Input("chemicals_dropdown", "value")],
)
def map_update(chemicals):
    fig = px.scatter_mapbox(
        data_frame=df_time,
        lat="Lat",
        lon="Lon",
        hover_name="Наименование водного объекта",
        hover_data=df_time[chemicals],
        size=np.sum(df_time[chemicals], axis=1)*10,
        animation_group="Нефтепродукты",
        animation_frame="Период наблюдений",
        zoom=5,
        height=500,
        center={"lat":56.75, "lon":67.7}
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0,"t": 0,"l": 0,"b": 0})
    return fig

@app.callback(
    Output("sankey", "figure"),
    [Input("my-date-picker-single", "date")],
)
def map_update(date_value):
    values = []
    df_selected = df_time[df_time["Период наблюдений"] == date_value]
    for river in rivers_list:
        try:
            values.append(df_selected[df_selected["Наименование водного объекта"]==river].iloc[0, 2:13].to_list())
        except:
            values.append(np.full(11, 0))

    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 30,
             thickness = 5,
             line = dict(color = "black", width = 0.2),
             label = rivers_list,
             customdata = rivers_list,
             hovertemplate='Node %{customdata} has total value %{value}<extra></extra>',
             color = "#049CE0"
        ),
        link = dict(
            source = np.array(source).flatten(),
            target = np.array(target).flatten(),
            value = np.array(values).flatten(),
            label = chemicals*14,
            color = colours*14,))])
    fig.update_layout(
        title_text="Chemicals Sankey Diagram", 
        font=dict(size = 10, color = 'white')
    )
    return fig

@app.callback(
    dash.dependencies.Output("timeseries-graph_2", "figure"),
    [dash.dependencies.Input("date_start", "date"),
     dash.dependencies.Input("date_end", "date"),
     dash.dependencies.Input("date_start_1", "date"),
     dash.dependencies.Input("date_end_1", "date"),
     dash.dependencies.Input("chemicals_dropdown_2", "value"),
     dash.dependencies.Input("river_dropdown_2", "value")]
)
def update_output(start_date, end_date, start_date_1, end_date_1, chemicals, river):
    print(start_date, end_date)
    fig = make_subplots(rows=2, cols=1)
    df_time1 = df_time[df_time["Период наблюдений"] > start_date]
    df_time1 = df_time1[df_time1["Период наблюдений"] < end_date]
    df_time1 = df_time1[df_time1["Наименование водного объекта"] == river]
    df_time1 = df_time1.reset_index(drop=True)
    
    df_time2 = df_time[df_time["Период наблюдений"] > start_date_1]
    df_time2 = df_time2[df_time2["Период наблюдений"] < end_date_1]
    df_time2 = df_time2[df_time2["Наименование водного объекта"] == river]
    df_time2 = df_time2.reset_index(drop=True)

    trace1 = go.Bar(
    	name=f"{start_date} - {end_date}",
    	x=df_time1["Период наблюдений"],
    	y=df_time1[chemicals])
    trace2 = go.Bar(
    	name=f"{start_date_1} - {end_date_1}",
    	x=df_time2["Период наблюдений"],
    	y=df_time2[chemicals])
    fig.add_trace(trace1, 1, 1)
    fig.add_trace(trace2, 2, 1)
    fig.update_layout(
        yaxis1 = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2],
            ticktext = ["Normal", "Middle", "High"]),
        yaxis2 = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2],
            ticktext = ["Normal", "Middle", "High"]),
        margin={"r": 0,"t": 10,"l": 100,"b": 0},
        #width=900
    )
    return fig

@app.callback(
    dash.dependencies.Output("timeseries-graph_3", "figure"),
    [dash.dependencies.Input("date_start", "date"),
     dash.dependencies.Input("date_end", "date"),
     dash.dependencies.Input("date_start_1", "date"),
     dash.dependencies.Input("date_end_1", "date"),
     dash.dependencies.Input("chemicals_dropdown_2", "value"),
     dash.dependencies.Input("river_dropdown_2", "value")]
)
def update_output(start_date, end_date, start_date_1, end_date_1, chemicals, river):
    print(start_date, end_date)
    fig = make_subplots(rows=2, cols=1)
    df_time1 = df_time[df_time["Период наблюдений"] > start_date]
    df_time1 = df_time1[df_time1["Период наблюдений"] < end_date]
    df_time1 = df_time1[df_time1["Наименование водного объекта"] == river]
    df_time1 = df_time1.reset_index(drop=True)
    
    df_time2 = df_time[df_time["Период наблюдений"] > start_date_1]
    df_time2 = df_time2[df_time2["Период наблюдений"] < end_date_1]
    df_time2 = df_time2[df_time2["Наименование водного объекта"] == river]
    df_time2 = df_time2.reset_index(drop=True)

    trace1 = go.Bar(
        name="График 1",
        x=df_time1["Период наблюдений"],
        y=df_time1[chemicals])
    trace2 = go.Bar(
        name="График 2",
        x=df_time2["Период наблюдений"],
        y=df_time2[chemicals])
    fig.add_trace(trace1, 1, 1)
    fig.add_trace(trace2, 2, 1)
    fig.update_layout(
        yaxis1 = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2],
            ticktext = ["Normal", "Middle", "High"]),
        yaxis2 = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2],
            ticktext = ["Normal", "Middle", "High"]),
        margin={"r": 0,"t": 10,"l": 100,"b": 0},
    )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
