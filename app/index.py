from app.server import app
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from football_analysis.statsbomb.analysis import PassAnalysis, plotly_test_network

pass_analysis = PassAnalysis(
    game_id='3895194',
    team_id=904,
    starting_players_only=True
)

temp_passes_between, temp_passers_avg_location, color = plotly_test_network(
    pass_analysis.passes_between,
    pass_analysis.passers_avg_location,
    pass_analysis.players_to_plot,
    pass_analysis.players_df
)
TITLE_TEXT = f"{pass_analysis.team_name} vs {pass_analysis.opp_team_name}"

# Create a trace for the pitch
pitch_trace = go.Scatter(
    x=[0, 120, 120, 0, 0],
    y=[0, 0, 80, 80, 0],
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

# Add midfield line
midfield_trace = go.Scatter(
    x=[60, 60],
    y=[0, 80],
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

# Add center circle
t = np.linspace(0, 2*np.pi, 100)
center_circle_trace = go.Scatter(
    x=60 + 9.15 * np.cos(t),  # x0 + r*cos(t)
    y=40 + 9.15 * np.sin(t),  # y0 + r*sin(t)
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

# Add penalty areas
penalty_area1_trace = go.Scatter(
    x=[120-16.5, 120-16.5, 120, 120, 120-16.5],
    y=[(80-40.32)/2, (80+40.32)/2, (80+40.32)/2, (80-40.32)/2, (80-40.32)/2],
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

penalty_area2_trace = go.Scatter(
    x=[0, 0, 16.5, 16.5, 0],
    y=[(80-40.32)/2, (80+40.32)/2, (80+40.32)/2, (80-40.32)/2, (80-40.32)/2],
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

six_yard_box1_trace = go.Scatter(
    x=[120-5.5, 120-5.5, 120, 120, 120-5.5],
    y=[(80-18.32)/2, (80+18.32)/2, (80+18.32)/2, (80-18.32)/2, (80-18.32)/2],
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

six_yard_box2_trace = go.Scatter(
    x=[0, 0, 5.5, 5.5, 0],
    y=[(80-18.32)/2, (80+18.32)/2, (80+18.32)/2, (80-18.32)/2, (80-18.32)/2],
    mode='lines',
    line=dict(color="#808080", width=2),
    hoverinfo='none'
)

# Add penalty spots and center spot
penalty_spot1_trace = go.Scatter(
    x=[120-11],
    y=[40],
    mode='markers',
    marker=dict(size=6, color="#808080"),
    hoverinfo='none'
)

penalty_spot2_trace = go.Scatter(
    x=[11],
    y=[40],
    mode='markers',
    marker=dict(size=6, color="#808080"),
    hoverinfo='none'
)

center_spot_trace = go.Scatter(
    x=[60],
    y=[40],
    mode='markers',
    marker=dict(size=6, color="#808080"),
    hoverinfo='none'
)

# Define the radius and the center
r = 9.15
h, k = 11, 40

# Generate x values
x = np.linspace(16.5, h+r, 400)

# Calculate corresponding y values
y_positive = np.sqrt(r**2 - (x-h)**2) + k
y_negative = -np.sqrt(r**2 - (x-h)**2) + k

penalty_arc1_trace_positive = go.Scatter(x=x, y=y_positive, mode='lines', marker=dict(color="#808080"))
penalty_arc1_trace_negative = go.Scatter(x=x, y=y_negative, mode='lines', marker=dict(color="#808080"))

# Define the radius and the center for the second circle
r = 9.15
h, k = 120-11, 40

# Generate x values
x = np.linspace(h-r, 120-16.5, 400)

# Calculate corresponding y values
y_positive = np.sqrt(r**2 - (x-h)**2) + k
y_negative = -np.sqrt(r**2 - (x-h)**2) + k

# Create scatter plot for the second circle
penalty_arc2_trace_positive = go.Scatter(x=x, y=y_positive, mode='lines', marker=dict(color="#808080"))
penalty_arc2_trace_negative = go.Scatter(x=x, y=y_negative, mode='lines', marker=dict(color="#808080"))

# Add a small linear section to meet at y=40
x_linear = np.linspace(99.8591, 99.8591)
y_linear = np.linspace(39.59095, 40.40905)

penalty_arc2_trace_linear = go.Scatter(x=x_linear, y=y_linear, mode='lines', marker=dict(color="#808080"))

traces = [
    pitch_trace,
    midfield_trace,
    center_circle_trace,
    penalty_area1_trace,
    penalty_area2_trace,
    six_yard_box1_trace,
    six_yard_box2_trace,
    penalty_spot1_trace,
    penalty_spot2_trace,
    center_spot_trace,
    penalty_arc1_trace_positive,
    penalty_arc1_trace_negative,
    penalty_arc2_trace_positive,
    penalty_arc2_trace_negative,
    penalty_arc2_trace_linear
    
]

# Create a separate trace for each line
for i in range(len(temp_passes_between)):
    traces.append(
        go.Scatter(
            x=temp_passes_between[['x', 'x_end']].iloc[i].values,
            y=temp_passes_between[['y', 'y_end']].iloc[i].values,
            mode='lines',
            line=dict(width=float(temp_passes_between['width'].iloc[i]), color='rgba(128, 128, 128, 0.75)'),
            hovertemplate='Number of passes: %{text}',
            text=f'{temp_passes_between["pass_count"].iloc[i]}'
        )
    )

# Add the marker trace
traces.append(
    go.Scatter(
        x=temp_passers_avg_location['x'],
        y=temp_passers_avg_location['y'],
        mode='markers',
        marker=dict(
            size=temp_passers_avg_location['normalized_marker_size'],  # Replace 'your_column' with the name of your column
            sizemode='diameter',  # Marker size is set by diameter
            sizemin=4,  # Minimum marker size
            sizeref=1/30,  # Adjust this value to change the scaling of your marker sizes
            color='#E32221',
            opacity=1,  # Ensure markers are completely opaque
            line=dict(color= "#E32221",width=10)
        ),
        text=temp_passers_avg_location['player_name'] + ' (' +
            temp_passers_avg_location['jersey_number'].astype(str) + ') - ' +
            temp_passers_avg_location['position_name'] + '<br>' + 
            temp_passers_avg_location['passes_given'].astype(str) + ' passes given<br>' + 
            temp_passers_avg_location['passes_received'].astype(str) + ' passes received',
        textposition='middle center',
        hovertemplate='%{text}<extra></extra>', # Only display the text when hovering
        hoverinfo='text' # Disable default hover info
    )
)

# Create a list of annotations
annotations = []
for i, row in temp_passers_avg_location.iterrows():
    annotations.append(dict(
        x=row['x'],
        y=row['y'],
        text=str(row['jersey_number']),
        showarrow=False,
        font=dict(size=15*row['normalized_marker_size']+8, color='white', family="Arial, bold"),
        xanchor='center',
        yanchor='middle'
    ))

layout = go.Layout(
    title={
        'text': TITLE_TEXT,
        'font': {
            'color': '#808080',
            'size': 24,  # adjust as needed
            'family': 'Arial, bold'
        },
        # 'y':0.9,
        # 'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    showlegend=False,
    autosize=False,
    width=1200,
    height=800,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 120]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 80]),
    annotations=annotations,  # Add annotations to your layout
    plot_bgcolor='rgba(20, 20, 20, 0.9)',  # Dark background color
    paper_bgcolor='rgba(20, 20, 20, 0.9)'  # Dark background color for the entire chart
)

app.layout = html.Div([
    dcc.Graph(
        id='pass-network-graph',
        figure={
            'data': traces,
            'layout': layout
        }
    )
], style={'backgroundColor': 'rgba(20, 20, 20, 0.9)'})

if __name__ == '__main__':
    app.run_server(debug=True)
