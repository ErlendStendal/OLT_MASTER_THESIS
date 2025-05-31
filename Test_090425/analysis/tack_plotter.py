import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load CSV file
def plot_csv_data(csv_file):
    # Read CSV
    df = pd.read_csv(csv_file)

    # Convert GPS_Time_dt to datetime if available
    if 'GPS_Time' in df.columns:
        df['GPS_Time'] = pd.to_datetime(df['GPS_Time'])
        x_time = df['GPS_Time']
    elif 'Relative_Time' in df.columns:
        x_time = df['Relative_Time']
    else:
        x_time = range(len(df))

    # Adjust Course to avoid jumps (center around -180 to 180)
    if 'Course' in df.columns:
        df['Course_Centered'] = ((df['Course'] + 180) % 360) - 180
        course_col = 'Course_Centered'
    else:
        course_col = 'Course'

    # Categorize columns
    categories = {
        'Potentiometers': ['Pot1', 'Pot2'],
        'GPS (Speed & Course)': ['Speed', course_col],
    }

    # Create subplots
    fig = make_subplots(rows=len(categories), cols=1, shared_xaxes=True, 
                        subplot_titles=list(categories.keys()), 
                        specs=[[{"secondary_y": False}], [{"secondary_y": True}]])

    # Plot Potentiometers
    for col in categories['Potentiometers']:
        if col in df.columns:
            fig.add_trace(go.Scatter(x=x_time, y=df[col], mode='lines', name=col), row=1, col=1)

    # Plot GPS (Speed & Course) with secondary y-axis
    if 'Speed' in df.columns:
        fig.add_trace(go.Scatter(x=x_time, y=df['Speed'], mode='lines', name='Speed'), 
                      row=2, col=1, secondary_y=False)

    if course_col in df.columns:
        fig.add_trace(go.Scatter(x=x_time, y=df[course_col], mode='lines', name='Course (Centered)'), 
                      row=2, col=1, secondary_y=True)

    fig.update_layout(height=600, width=1000, title_text="Sensor Data Overview (Interactive)")

    # X-axis formatting
    if 'GPS_Time' in df.columns:
        fig.update_xaxes(title_text="GPS Time", row=len(categories), col=1)
    elif 'Relative_Time' in df.columns:
        fig.update_xaxes(title_text="Relative Time (s)", row=len(categories), col=1)
    else:
        fig.update_xaxes(title_text="Index", row=len(categories), col=1)

    # Y-axis titles
    fig.update_yaxes(title_text="Potentiometers", row=1, col=1)
    fig.update_yaxes(title_text="Speed", row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_text="Course (deg)", row=2, col=1, secondary_y=True)

    fig.show()

# Example usage
plot_csv_data("tacks/Turn_12.csv")
