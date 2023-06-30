import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load the data from Excel using pandas
df = pd.read_excel("Galbulidae.xlsx")

# Get the list of classes in the "epiteto" column
classes_epiteto = df["epiteto"].unique()

# Create the Dash application
app = dash.Dash(__name__, external_stylesheets=["styles.css"])

# Calculate the width of the dropdown based on the maximum length of the epiteto names
max_epiteto_length = max([len(epiteto) for epiteto in classes_epiteto])
dropdown_width = (
    12 * max_epiteto_length
)  # Approximate width in pixels based on character length

# Application layout
app.layout = html.Div(
    style={
        "display": "flex",
        "height": "100vh",
        "background-color": "#444654",  # Set the background color here
        "font-family": "Gill Sans MT",
    },
    children=[
        html.Div(
            style={
                "flex": "0 0 auto",
                "width": f"{dropdown_width}px",
                "color": "#ffffff",
                "font-size": "12px",
                "padding": "10px",
            },
            children=[
                html.H3("Species List", style={"padding-top": "5px"}),
                dcc.Dropdown(
                    id="dropdown_classes",
                    options=[
                        {"label": classe, "value": classe} for classe in classes_epiteto
                    ],
                    value=classes_epiteto[0],  # Initial value for the dropdown
                    style={
                        "font-family": "Gill Sans MT",
                        "color": "#444654",
                    },  # Set font-family for the dropdown
                ),
                html.H3("Map Type", style={"padding-top": "15px"}),
                dcc.Dropdown(
                    id="dropdown_map_type",
                    options=[
                        {"label": "Current Map", "value": "open-street-map"},
                        {"label": "Relief Map", "value": "stamen-terrain"},
                    ],
                    value="open-street-map",  # Initial value for the dropdown
                    style={
                        "font-family": "Gill Sans MT",
                        "color": "#444654",
                    },  # Set font-family for the dropdown
                ),
            ],
        ),
        html.Div(
            style={
                "flex": "1",
                "overflow": "hidden",
                "color": "#ffffff",  # Set the text color for the map
                "padding": "10px",
            },
            children=[
                dcc.Graph(
                    id="mapa",
                    style={
                        "height": "100%",
                        "font-size": "12px",
                    },
                ),  # Set height to 100% of the element
            ],
        ),
    ],
)


# Create the callback to generate the interactive map
@app.callback(
    Output("mapa", "figure"),
    [Input("dropdown_classes", "value"), Input("dropdown_map_type", "value")],
)
def update_map(selected_class, map_type):
    # Filter the dataframe to show only the points of the selected class
    filtered_df = df[df["epiteto"] == selected_class]

    # Use Plotly library to create the interactive map
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Sigla coleção",
        hover_data=[
            "Número de Tombo",
            "Sexo",
            "Gênero",
            "epiteto",
            "País",
            "Estado/Departamento",
            "Localidade",
        ],
        zoom=3.8,
    )
    # Set the size of the points
    fig.update_traces(
        marker=dict(size=10, color="red")
    )  # You can adjust the size value as needed

    # Set the map style based on the selected option
    fig.update_layout(
        mapbox_style=map_type,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox=dict(
            center=dict(lat=-12, lon=-53.58),
            pitch=0,
            bearing=0,
        ),
    )

    return fig


# Run the application
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
