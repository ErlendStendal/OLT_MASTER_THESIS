import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def plot_csv_data(csv_file):
    # Read CSV
    df = pd.read_csv(csv_file)

    # Decide x_time
    if 'GPS_Time' in df.columns:
        sample_value = str(df['GPS_Time'].dropna().iloc[0])
        if len(sample_value.split(':')) == 3 and '-' not in sample_value:
            x_time = df['GPS_Time']
        else:
            df['GPS_Time'] = pd.to_datetime(df['GPS_Time'])
            x_time = df['GPS_Time']
    elif 'Relative_Time' in df.columns:
        x_time = df['Relative_Time']
    else:
        x_time = range(len(df))

    # Center Course and Wind Direction
    if 'Course' in df.columns:
        df['Course_Centered'] = ((df['Course'] + 180) % 360) - 180
        course_col = 'Course_Centered'
    else:
        course_col = None

    if 'Wind_Direction' in df.columns:
        df['Wind_Direction_Centered'] = ((df['Wind_Direction'] + 180) % 360) - 180
        wind_dir_col = 'Wind_Direction_Centered'
    else:
        wind_dir_col = None

    # Subplots: Row 1 - Potentiometers, Row 2 - Speed/VMG, Row 3 - Course/Wind
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        subplot_titles=["Potentiometers", "Speed / VMG", "Course / Wind Direction"],
        specs=[[{}], [{}], [{}]]  # Removed secondary_y
    )

    # Plot Potentiometers
    for col in ['Pot1', 'Pot2']:
        if col in df.columns:
            fig.add_trace(go.Scatter(x=x_time, y=df[col], mode='lines', name=col), row=1, col=1)

    # Plot Speed and VMG
    for col in ['Speed', 'VMG']:
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=x_time, y=df[col], mode='lines', name=col,
                line=dict(dash='dot' if col == 'VMG' else 'solid')
            ), row=2, col=1)

    # Plot Course
    if course_col and course_col in df.columns:
        fig.add_trace(go.Scatter(
            x=x_time, y=df[course_col], mode='lines', name='Course (Centered)'
        ), row=3, col=1)

    # Plot Wind Direction
    if wind_dir_col and wind_dir_col in df.columns:
        fig.add_trace(go.Scatter(
            x=x_time, y=df[wind_dir_col], mode='lines',
            name='Wind Direction (Centered)', line=dict(dash='dash')
        ), row=3, col=1)

    # Axis Labels
    fig.update_yaxes(title_text="Pot Value", row=1, col=1)
    fig.update_yaxes(title_text="Speed / VMG", row=2, col=1)
    fig.update_yaxes(title_text="Course / Wind Dir (deg)", row=3, col=1)

    # X-axis
    if 'GPS_Time' in df.columns:
        fig.update_xaxes(title_text="GPS Time", row=3, col=1)
    elif 'Relative_Time' in df.columns:
        fig.update_xaxes(title_text="Relative Time (s)", row=3, col=1)
    else:
        fig.update_xaxes(title_text="Index", row=3, col=1)

    # Layout
    fig.update_layout(
        height=1500, width=3000,
        title_text="Sensor Data Overview (Single File)",
        showlegend=True
    )

    fig.show()

# Example usage
plot_csv_data("tacks_meter_wind_VMG.csv")
