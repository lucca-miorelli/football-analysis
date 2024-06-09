import numpy as np
import plotly.graph_objs as go

def create_pitch():
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

    return [
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


# def create_half_pitch_rotated():
#     # Define the function to rotate points
#     def rotate_point(origin, point, angle):
#         ox, oy = origin
#         px, py = point

#         qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
#         qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)

#         return qx, qy

#     # Function to create traces
#     def create_trace(points, mode='lines', size=6, color="#808080"):
#         x, y = zip(*points)
#         if mode == 'markers':
#             return go.Scatter(x=x, y=y, mode=mode, marker=dict(size=size, color=color), hoverinfo='none')
#         else:
#             return go.Scatter(x=x, y=y, mode=mode, line=dict(color=color, width=2), hoverinfo='none')

#     # Half-pitch points
#     half_pitch_points = [(0, 0), (60, 0), (60, 40), (0, 40), (0, 0)]
#     half_pitch_points = [rotate_point((30, 20), p, np.pi/2) for p in half_pitch_points]

#     # Midfield line points
#     midfield_line_points = [(30, 0), (30, 40)]
#     midfield_line_points = [rotate_point((30, 20), p, np.pi/2) for p in midfield_line_points]

#     # Center circle points
#     t = np.linspace(0, 2*np.pi, 100)
#     center_circle_points = [(30 + 9.15 * np.cos(ti), 20 + 9.15 * np.sin(ti)) for ti in t]
#     center_circle_points = [rotate_point((30, 20), p, np.pi/2) for p in center_circle_points]

#     # Penalty area points
#     penalty_area_points = [(60-16.5, 10), (60-16.5, 30), (60, 30), (60, 10), (60-16.5, 10)]
#     penalty_area_points = [rotate_point((30, 20), p, np.pi/2) for p in penalty_area_points]

#     # Six yard box points
#     six_yard_box_points = [(60-5.5, 13), (60-5.5, 27), (60, 27), (60, 13), (60-5.5, 13)]
#     six_yard_box_points = [rotate_point((30, 20), p, np.pi/2) for p in six_yard_box_points]

#     # Penalty spot points
#     penalty_spot_points = [(60-11, 20)]
#     penalty_spot_points = [rotate_point((30, 20), p, np.pi/2) for p in penalty_spot_points]

#     # Center spot points
#     center_spot_points = [(30, 20)]
#     center_spot_points = [rotate_point((30, 20), p, np.pi/2) for p in center_spot_points]

#     # Penalty arc points
#     penalty_arc_points = [(60-9.15, 20 + np.sin(ti) * 9.15) for ti in np.linspace(np.pi/6, 5*np.pi/6, 100)]
#     penalty_arc_points = [rotate_point((30, 20), p, np.pi/2) for p in penalty_arc_points]

#     return [
#         create_trace(half_pitch_points),
#         create_trace(midfield_line_points),
#         create_trace(center_circle_points),
#         create_trace(penalty_area_points),
#         create_trace(six_yard_box_points),
#         create_trace(penalty_spot_points, mode='markers'),
#         create_trace(center_spot_points, mode='markers'),
#         create_trace(penalty_arc_points)
#     ]

def create_half_pitch_rotated():
    # Create a trace for the pitch
    pitch_trace = go.Scatter(
        x=[0, 80, 80, 0, 0],
        y=[0, 0, 60, 60, 0],
        mode='lines',
        line=dict(color="#808080", width=2),
        hoverinfo='none'
    )

    # # Add midfield line
    # midfield_trace = go.Scatter(
    #     x=[60, 60],
    #     y=[0, 80],
    #     mode='lines',
    #     line=dict(color="#808080", width=2),
    #     hoverinfo='none'
    # )

    # Add center circle
    t = np.linspace(0, 2*np.pi, 100)
    center_circle_trace = go.Scatter(
        x=40 + 9.15 * np.cos(t),  # x0 + r*cos(t)
        y=0 + 9.15 * np.sin(t),  # y0 + r*sin(t)
        mode='lines',
        line=dict(color="#808080", width=2),
        hoverinfo='none'
    )

    # Add penalty areas
    penalty_area1_trace = go.Scatter(
        x=[(80-40.32)/2, (80+40.32)/2, (80+40.32)/2, (80-40.32)/2, (80-40.32)/2],
        y=[(60-16.5), (60-16.5), 60, 60, (60-16.5)],
        mode='lines',
        line=dict(color="#808080", width=2),
        hoverinfo='none'
    )


    six_yard_box1_trace = go.Scatter(
        x=[(80-18.32)/2, (80+18.32)/2, (80+18.32)/2, (80-18.32)/2, (80-18.32)/2],
        y=[60, 60, 60-5.5, 60-5.5, 60],
        mode='lines',
        line=dict(color="#808080", width=2),
        hoverinfo='none'
    )

    # Add penalty spots and center spot
    penalty_spot1_trace = go.Scatter(
        x=[40],
        y=[80-11],
        mode='markers',
        marker=dict(size=6, color="#808080"),
        hoverinfo='none'
    )

    center_spot_trace = go.Scatter(
        x=[40],
        y=[0],
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

    return [
        pitch_trace,
        center_circle_trace,
        penalty_area1_trace,
        six_yard_box1_trace,
        penalty_spot1_trace,
        center_spot_trace,
        # penalty_arc1_trace_positive,
        # penalty_arc1_trace_negative,
        # penalty_arc2_trace_positive,
        # penalty_arc2_trace_negative,
        # penalty_arc2_trace_linear
    ]