import numpy as np
import plotly.graph_objs as go


def create_pitch(resize_factor=1.0):
    # Create a trace for the pitch
    pitch_trace = go.Scatter(
        x=[value * resize_factor for value in [0, 120, 120, 0, 0]],
        y=[value * resize_factor for value in [0, 0, 80, 80, 0]],
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    # Add midfield line
    midfield_trace = go.Scatter(
        x=[value * resize_factor for value in [60, 60]],
        y=[value * resize_factor for value in [0, 80]],
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    # Add center circle
    r = 9.15 * resize_factor
    h, k = 60 * resize_factor, 40 * resize_factor
    t = np.linspace(0, 2 * np.pi, 100)

    center_circle_trace = go.Scatter(
        x=h + r * np.cos(t),  # x0 + r*cos(t)
        y=k + r * np.sin(t),  # y0 + r*sin(t)
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    # Add penalty areas
    penalty_area1_trace = go.Scatter(
        x=[
            value * resize_factor
            for value in [120 - 16.5, 120 - 16.5, 120, 120, 120 - 16.5]
        ],
        y=[
            value * resize_factor
            for value in [
                (80 - 40.32) / 2,
                (80 + 40.32) / 2,
                (80 + 40.32) / 2,
                (80 - 40.32) / 2,
                (80 - 40.32) / 2,
            ]
        ],
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    penalty_area2_trace = go.Scatter(
        x=[value * resize_factor for value in [0, 0, 16.5, 16.5, 0]],
        y=[
            value * resize_factor
            for value in [
                (80 - 40.32) / 2,
                (80 + 40.32) / 2,
                (80 + 40.32) / 2,
                (80 - 40.32) / 2,
                (80 - 40.32) / 2,
            ]
        ],
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    six_yard_box1_trace = go.Scatter(
        x=[
            value * resize_factor
            for value in [120 - 5.5, 120 - 5.5, 120, 120, 120 - 5.5]
        ],
        y=[
            value * resize_factor
            for value in [
                (80 - 18.32) / 2,
                (80 + 18.32) / 2,
                (80 + 18.32) / 2,
                (80 - 18.32) / 2,
                (80 - 18.32) / 2,
            ]
        ],
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    six_yard_box2_trace = go.Scatter(
        x=[value * resize_factor for value in [0, 0, 5.5, 5.5, 0]],
        y=[
            value * resize_factor
            for value in [
                (80 - 18.32) / 2,
                (80 + 18.32) / 2,
                (80 + 18.32) / 2,
                (80 - 18.32) / 2,
                (80 - 18.32) / 2,
            ]
        ],
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    # Add penalty spots and center spot
    penalty_spot1_trace = go.Scatter(
        x=[value * resize_factor for value in [120 - 11]],
        y=[value * resize_factor for value in [40]],
        mode="markers",
        marker=dict(size=6 * resize_factor, color="#808080"),
        hoverinfo="none",
    )

    penalty_spot2_trace = go.Scatter(
        x=[value * resize_factor for value in [11]],
        y=[value * resize_factor for value in [40]],
        mode="markers",
        marker=dict(size=6 * resize_factor, color="#808080"),
        hoverinfo="none",
    )

    center_spot_trace = go.Scatter(
        x=[value * resize_factor for value in [60]],
        y=[value * resize_factor for value in [40]],
        mode="markers",
        marker=dict(size=6 * resize_factor, color="#808080"),
        hoverinfo="none",
    )

    # Define the radius and the center
    r = 9.15 * resize_factor
    h, k = 11 * resize_factor, 40 * resize_factor

    # Generate x values
    x = np.linspace(16.5 * resize_factor, h + r, 400)

    # Calculate corresponding y values
    y_positive = np.sqrt(r**2 - (x - h) ** 2) + k
    y_negative = -np.sqrt(r**2 - (x - h) ** 2) + k

    penalty_arc1_trace_positive = go.Scatter(
        x=x,
        y=y_positive,
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )
    penalty_arc1_trace_negative = go.Scatter(
        x=x,
        y=y_negative,
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    # Define the radius and the center for the second circle
    r = 9.15 * resize_factor
    h, k = (120 - 11) * resize_factor, 40 * resize_factor

    # Generate x values
    x = np.linspace(h - r, (120 - 16.5) * resize_factor, 400)

    # Calculate corresponding y values
    y_positive = np.sqrt(r**2 - (x - h) ** 2) + k
    y_negative = -np.sqrt(r**2 - (x - h) ** 2) + k

    # Create scatter plot for the second circle
    penalty_arc2_trace_positive = go.Scatter(
        x=x,
        y=y_positive,
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )
    penalty_arc2_trace_negative = go.Scatter(
        x=x,
        y=y_negative,
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

    # Add a small linear section to meet at y=40
    x_linear = np.linspace((99.8591) * resize_factor, (99.8591) * resize_factor)
    y_linear = np.linspace((39.59095) * resize_factor, (40.40905) * resize_factor)

    penalty_arc2_trace_linear = go.Scatter(
        x=x_linear,
        y=y_linear,
        mode="lines",
        line=dict(color="#808080", width=2 * resize_factor),
        hoverinfo="none",
    )

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
        penalty_arc2_trace_linear,
    ]


def create_half_pitch_rotated():
    # Create a trace for the pitch
    pitch_trace = go.Scatter(
        x=[0, 80, 80, 0, 0],
        y=[0, 0, 60, 60, 0],
        mode="lines",
        line=dict(color="#808080", width=2),
        hoverinfo="none",
    )

    # Add center circle
    t = np.linspace(0, 2 * np.pi, 100)
    center_circle_trace = go.Scatter(
        x=40 + 9.15 * np.cos(t),  # x0 + r*cos(t)
        y=0 + 9.15 * np.sin(t),  # y0 + r*sin(t)
        mode="lines",
        line=dict(color="#808080", width=2),
        hoverinfo="none",
    )

    # Add penalty areas
    penalty_area1_trace = go.Scatter(
        x=[
            (80 - 40.32) / 2,
            (80 + 40.32) / 2,
            (80 + 40.32) / 2,
            (80 - 40.32) / 2,
            (80 - 40.32) / 2,
        ],
        y=[(60 - 16.5), (60 - 16.5), 60, 60, (60 - 16.5)],
        mode="lines",
        line=dict(color="#808080", width=2),
        hoverinfo="none",
    )

    six_yard_box1_trace = go.Scatter(
        x=[
            (80 - 18.32) / 2,
            (80 + 18.32) / 2,
            (80 + 18.32) / 2,
            (80 - 18.32) / 2,
            (80 - 18.32) / 2,
        ],
        y=[60, 60, 60 - 5.5, 60 - 5.5, 60],
        mode="lines",
        line=dict(color="#808080", width=2),
        hoverinfo="none",
    )

    # Add penalty spots and center spot
    penalty_spot1_trace = go.Scatter(
        x=[40],
        y=[80 - 11],
        mode="markers",
        marker=dict(size=6, color="#808080"),
        hoverinfo="none",
    )

    center_spot_trace = go.Scatter(
        x=[40],
        y=[0],
        mode="markers",
        marker=dict(size=6, color="#808080"),
        hoverinfo="none",
    )

    # Define the radius and the center
    r = 9.15
    h, k = 11, 40

    # Generate x values
    x = np.linspace(16.5, h + r, 400)

    # Calculate corresponding y values
    y_positive = np.sqrt(r**2 - (x - h) ** 2) + k
    y_negative = -np.sqrt(r**2 - (x - h) ** 2) + k

    penalty_arc1_trace_positive = go.Scatter(
        x=x, y=y_positive, mode="lines", marker=dict(color="#808080")
    )
    penalty_arc1_trace_negative = go.Scatter(
        x=x, y=y_negative, mode="lines", marker=dict(color="#808080")
    )

    # Define the radius and the center for the second circle
    r = 9.15
    h, k = 120 - 11, 40

    # Generate x values
    x = np.linspace(h - r, 120 - 16.5, 400)

    # Calculate corresponding y values
    y_positive = np.sqrt(r**2 - (x - h) ** 2) + k
    y_negative = -np.sqrt(r**2 - (x - h) ** 2) + k

    # Create scatter plot for the second circle
    penalty_arc2_trace_positive = go.Scatter(
        x=x, y=y_positive, mode="lines", marker=dict(color="#808080")
    )
    penalty_arc2_trace_negative = go.Scatter(
        x=x, y=y_negative, mode="lines", marker=dict(color="#808080")
    )

    # Add a small linear section to meet at y=40
    x_linear = np.linspace(99.8591, 99.8591)
    y_linear = np.linspace(39.59095, 40.40905)

    penalty_arc2_trace_linear = go.Scatter(
        x=x_linear, y=y_linear, mode="lines", marker=dict(color="#808080")
    )

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
