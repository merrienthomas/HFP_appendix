from dash import Dash, dcc, html, Input, Output

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.spatial import ConvexHull
import plotly.express as px
import os


path="/Users/merrien/Documents/HFP&Demography/Script and R material/my_app"
os.chdir(path)

df = pd.read_csv("resilience.csv")
hull_choice = ["No", "Uniform distribution", "Normal distribution", "Gamma distribution"]

app = Dash("OnlineAppendix")

app.layout = html.Div([
    html.H4('Online Appendix 2: Highly disturbed human habitats house species with fewer resilient strategies than pristine habitats'),
    html.Div([
            dcc.Dropdown(
                df.columns,
                'Human_presence',
                id='xaxis',
            )]),
    html.Div([
            dcc.Dropdown(
                df.columns,
                'Resistance',
                id='yaxis',
            )]),
    html.Div([
            dcc.Dropdown(
                df.columns,
                'Speed_of_recovery',
                id='zaxis',
            )]),
    html.Div([
            dcc.Dropdown(
                hull_choice,
                'No',
                id='overlay',
            )]),
    dcc.Graph(id='graph')
    #html.Div(id='my-output')
])


@app.callback(
    Output('graph', 'figure'),
    Input('xaxis', 'value'),
    Input('yaxis', 'value'),
    Input('zaxis', 'value'),
    Input('overlay', 'value'))

def update_graph(xaxis, yaxis, zaxis, overlay):
    
    #Plotting the data points

    fig = px.scatter_3d(df, x=df[xaxis].values,
                      y=df[yaxis].values,
                      z=df[zaxis].values,
                      width=1200, height=800)
    
    fig.update_traces(marker=dict(size=4, color = "blue"))
    
    #Computing the hull
    
    resilience_framework = np.array([df[xaxis].values, df[yaxis].values, df[zaxis].values])
    
    hull = ConvexHull(np.transpose(resilience_framework[:,1:914]))
    
    polyhedra_points = [ ]

    polyhedra_points = hull.vertices.tolist()
    coordinates_all = np.transpose(resilience_framework)
    polyhedra_coordinates = coordinates_all[polyhedra_points]
    
    #Plotting the hull
    
    fig.add_trace(go.Mesh3d(x=polyhedra_coordinates[:, 0],
    y=polyhedra_coordinates[:, 1],
    z=polyhedra_coordinates[:, 2],
    color= 'blue',
    name= 'Real data',
    contour = dict(color = 'blue', show = True, width = 10),
    #facecolor = polyhedra_coordinates,
    flatshading=True, #helped a bit to see edges
    lighting=dict(ambient=0.6, diffuse=0.8), #helped a bit to see edges
    opacity=.4,
    alphahull=0
    ))
    
    #Adding the overlay
    
    if overlay=="Uniform distribution":
        
        unif_df = pd.read_csv(r'resilience_unif.csv')
        
        unif_framework = np.array([unif_df[xaxis].values, unif_df[yaxis].values, unif_df[zaxis].values])
        
        hull_unif = ConvexHull(np.transpose(unif_framework[:,1:914]))
        
        polyhedra_points2 = [ ]

        polyhedra_points2 = hull_unif.vertices.tolist()
        coordinates_all2 = np.transpose(unif_framework)
        polyhedra_coordinates2 = coordinates_all2[polyhedra_points2]

        fig.add_trace(go.Mesh3d(x=polyhedra_coordinates2[:, 0],
        y=polyhedra_coordinates2[:, 1],
        z=polyhedra_coordinates2[:, 2],
        color= 'red',
        name= 'Data simulated under Uniform distribution',
        contour = dict(color = 'red', show = True, width = 10),
        #facecolor = polyhedra_coordinates,
        flatshading=True, #helped a bit to see edges
        lighting=dict(ambient=0.6, diffuse=0.8), #helped a bit to see edges
        opacity=.4,
        alphahull=0
        ))
        
    elif overlay=="Normal distribution":
            
        norm_df = pd.read_csv(r'resilience_norm.csv')
        
        norm_framework = np.array([norm_df[xaxis].values, norm_df[yaxis].values, norm_df[zaxis].values])
        
        hull_norm = ConvexHull(np.transpose(norm_framework[:,1:914]))
        
        polyhedra_points2 = [ ]

        polyhedra_points2 = hull_norm.vertices.tolist()
        coordinates_all2 = np.transpose(norm_framework)
        polyhedra_coordinates2 = coordinates_all2[polyhedra_points2]

        fig.add_trace(go.Mesh3d(x=polyhedra_coordinates2[:, 0],
        y=polyhedra_coordinates2[:, 1],
        z=polyhedra_coordinates2[:, 2],
        color= 'red',
        name= 'Data simulated under Normal distribution',
        contour = dict(color = 'red', show = True, width = 10),
        #facecolor = polyhedra_coordinates,
        flatshading=True, #helped a bit to see edges
        lighting=dict(ambient=0.6, diffuse=0.8), #helped a bit to see edges
        opacity=.4,
        alphahull=0
        ))
            
    elif overlay=="Gamma distribution":
        
        gamma_df = pd.read_csv(r'resilience_gamma.csv')

        gamma_framework = np.array([gamma_df[xaxis].values, gamma_df[yaxis].values, gamma_df[zaxis].values])
        
        hull_gamma = ConvexHull(np.transpose(gamma_framework[:,1:914]))
        
        polyhedra_points2 = [ ]

        polyhedra_points2 = hull_gamma.vertices.tolist()
        coordinates_all2 = np.transpose(gamma_framework)
        polyhedra_coordinates2 = coordinates_all2[polyhedra_points2]

        fig.add_trace(go.Mesh3d(x=polyhedra_coordinates2[:, 0],
        y=polyhedra_coordinates2[:, 1],
        z=polyhedra_coordinates2[:, 2],
        color= 'red',
        name= 'Data simulated under Gamma distribution',
        contour = dict(color = 'red', show = True, width = 10),
        #facecolor = polyhedra_coordinates,
        flatshading=True, #helped a bit to see edges
        lighting=dict(ambient=0.6, diffuse=0.8), #helped a bit to see edges
        opacity=.4,
        alphahull=0
        ))
        
    fig.update_traces(showlegend=True)
    fig.update_layout(
    scene=dict(
    xaxis = dict(title= xaxis, nticks=10, range=[-2,20]),
    yaxis = dict(title= yaxis, nticks=10, range=[-3,13]),
    zaxis = dict(title= zaxis, nticks=10, range=[-3,13]))
    )


    return fig

#def update_output_div(xaxis, yaxis, zaxis):
#    return f'{xaxis}'

app.run_server(debug=True)

