import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math

# Set global font size
plt.rcParams.update({'font.size': 18})

def plot_multiple_csv_files(csv_files):
    num_files = len(csv_files)
    cols = math.ceil(math.sqrt(num_files))
    rows = math.ceil(num_files / cols)

    fig = plt.figure(figsize=(cols * 6.5, rows * 6.5), constrained_layout=True)
    gs = gridspec.GridSpec(rows * 2, cols, figure=fig)

    colors = {
        'Rudder angle': 'blue',
        'GN angle': 'green',
        'SOG': 'red',
        'VMG': 'orange',
        'Course': 'purple',
        'EOWD': '#40E0D0'
    }

    x_times_all = []
    pot_values = []
    speed_vmg_values = []
    course_wind_values = []
    all_data = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)

        col_rename_map = {
            'Pot1': 'Rudder angle',
            'Pot3': 'GN angle',
            'Speed': 'SOG'
        }
        df = df.rename(columns={k: v for k, v in col_rename_map.items() if k in df.columns})

        if 'GPS_Time' in df.columns:
            sample_value = str(df['GPS_Time'].dropna().iloc[0])
            if len(sample_value.split(':')) == 3 and '-' not in sample_value:
                df[['h', 'm', 's']] = df['GPS_Time'].str.split(':', expand=True)
                x_time = df['h'].astype(float) * 3600 + df['m'].astype(float) * 60 + df['s'].astype(float)
            else:
                df['GPS_Time'] = pd.to_datetime(df['GPS_Time'])
                x_time = (df['GPS_Time'] - df['GPS_Time'].dt.normalize()).dt.total_seconds()
        elif 'GPS_Time_dt' in df.columns:
            df['GPS_Time_dt'] = pd.to_datetime(df['GPS_Time_dt'])
            x_time = (df['GPS_Time_dt'] - df['GPS_Time_dt'].dt.normalize()).dt.total_seconds()
        elif 'Relative_Time' in df.columns:
            x_time = df['Relative_Time']
        else:
            x_time = pd.Series(range(len(df)))

        x_time = x_time - x_time.iloc[0]
        x_time = x_time.round(1)
        x_times_all.append(x_time)

        for col in ['Rudder angle', 'GN angle']:
            if col in df.columns:
                pot_values.extend(df[col].values)

        for col in ['SOG', 'VMG']:
            if col in df.columns:
                speed_vmg_values.extend(df[col].values)

        if 'Course' in df.columns:
            df['Course_Centered'] = ((df['Course'] + 180) % 360) - 180
            course_col = 'Course_Centered'
            course_wind_values.extend(df[course_col].values)
        else:
            course_col = 'Course'

        if 'EOWD' in df.columns:
            df['EOWD_Centered'] = ((df['EOWD'] + 180) % 360) - 180
            wind_dir_col = 'EOWD_Centered'
            course_wind_values.extend(df[wind_dir_col].values)
        else:
            wind_dir_col = None

        all_data.append({
            'x_time': x_time,
            'df': df,
            'course_col': course_col,
            'wind_dir_col': wind_dir_col
        })

    if len(pot_values) == 0: pot_values = [0]
    if len(speed_vmg_values) == 0: speed_vmg_values = [0]
    if len(course_wind_values) == 0: course_wind_values = [0]

    global_x_min = min([x.min() for x in x_times_all])
    global_x_max = max([x.max() for x in x_times_all])
    global_pot_min, global_pot_max = np.min(pot_values), np.max(pot_values)
    global_speed_min, global_speed_max = np.min(speed_vmg_values), np.max(speed_vmg_values)
    global_course_min, global_course_max = np.min(course_wind_values), np.max(course_wind_values)

    subplot_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

    for idx, data in enumerate(all_data):
        x_time = data['x_time']
        df = data['df']
        course_col = data['course_col']
        wind_dir_col = data['wind_dir_col']

        row = idx // cols
        col = idx % cols

        is_left = col == 0
        is_right = col == (cols - 1)
        is_bottom = row == (rows - 1)

        ax_pot = fig.add_subplot(gs[row * 2, col])
        ax_gps = fig.add_subplot(gs[row * 2 + 1, col])
        ax_gps_2 = ax_gps.twinx()

        pot_handles = []
        gps_handles = []

        for pot_col in ['Rudder angle', 'GN angle']:
            if pot_col in df.columns:
                line, = ax_pot.plot(x_time, df[pot_col], label=pot_col, color=colors[pot_col])
                pot_handles.append(line)
                ax_pot.text(
                    0.9, 0.25,
                    #0.9, 0.9,
                    #f"Tack {idx*2 + 3}",
                    #f"Tack {idx*2 + 2}",
                    f"Tack {idx + 2}",
                    #f"Tack {idx + 8}",
                    #f"Tack {idx + 4}",
                    #f"Tack {idx + 11}",
                    transform=ax_pot.transAxes,
                    fontsize=18,
                    verticalalignment='top',
                    horizontalalignment='right',
                    bbox=dict(facecolor='white')
                )

        ax_pot.set_ylim(global_pot_min, global_pot_max)
        ax_pot.grid(True)
        if is_left:
            ax_pot.set_ylabel("Angle [deg]")
        else:
            ax_pot.set_yticklabels([])

        ax_pot.tick_params(labelbottom=False)

        for colname in ['SOG', 'VMG']:
            if colname in df.columns:
                line, = ax_gps.plot(x_time, df[colname], label=colname, color=colors[colname], linestyle='-')
                gps_handles.append(line)

        ax_gps.set_ylim(global_speed_min, global_speed_max)
        ax_gps.grid(True)
        if is_left:
            ax_gps.set_ylabel("Velocity [m/s]")
        else:
            ax_gps.set_yticklabels([])

        if is_bottom:
            ax_gps.set_xlabel("Time [s]")
        else:
            ax_gps.set_xticklabels([])

        if course_col in df.columns:
            line, = ax_gps_2.plot(x_time, df[course_col], label="Course", color=colors['Course'], linestyle='--')
            gps_handles.append(line)

        if wind_dir_col is not None:
            line, = ax_gps_2.plot(x_time, df[wind_dir_col], label="EOWD", color=colors['EOWD'], linestyle='--')
            gps_handles.append(line)

        ax_gps_2.set_ylim(global_course_min, global_course_max)
        if is_right:
            ax_gps_2.set_ylabel("Course / EOWD [deg]")
        else:
            ax_gps_2.set_yticklabels([])

        label_text = subplot_labels[idx] if idx < len(subplot_labels) else f'({chr(97 + idx)})'
        y_pos = -0.15 if row < (rows - 1) else -0.35
        ax_gps.text(0.5, y_pos, label_text, transform=ax_gps.transAxes,
                    fontsize=18, fontweight='bold', ha='center', va='top')

    plt.show()


if __name__ == "__main__":
    csv_files1 = [
        #"tacks_converted_deg1/Turn_01.csv",
        "tacks_converted_deg1/Turn_03.csv",
        "tacks_converted_deg1/Turn_05.csv",
        "tacks_converted_deg1/Turn_07.csv",
        "tacks_converted_deg1/Turn_09.csv",
        "tacks_converted_deg1/Turn_11.csv",
        "tacks_converted_deg1/Turn_13.csv"
    ]
    csv_files2 = [
        "tacks_converted_deg1/Turn_02.csv",
        "tacks_converted_deg1/Turn_04.csv",
        "tacks_converted_deg1/Turn_06.csv",
        "tacks_converted_deg1/Turn_08.csv",
        "tacks_converted_deg1/Turn_10.csv",
        "tacks_converted_deg1/Turn_12.csv"
        #"tacks_converted_deg1/Turn_14.csv"
    ]
    csv_files3 = [
        #"tacks_converted_deg1/Turn_01.csv",
        "tacks_converted_deg1/Turn_02.csv",
        "tacks_converted_deg1/Turn_03.csv",
        "tacks_converted_deg1/Turn_04.csv",
        "tacks_converted_deg1/Turn_05.csv",
        "tacks_converted_deg1/Turn_06.csv",
        "tacks_converted_deg1/Turn_07.csv"
    ]
    csv_files4 = [
        "tacks_converted_deg1/Turn_08.csv",
        "tacks_converted_deg1/Turn_09.csv",
        "tacks_converted_deg1/Turn_10.csv",
        "tacks_converted_deg1/Turn_11.csv",
        "tacks_converted_deg1/Turn_12.csv",
        "tacks_converted_deg1/Turn_13.csv"
        #"tacks_converted_deg1/Turn_14.csv"
    ]
    csv_files5 = [
        #"tacks_converted_deg2/Turn_01.csv",
        "tacks_converted_deg2/Turn_04.csv",
        "tacks_converted_deg2/Turn_05.csv",
        "tacks_converted_deg2/Turn_06.csv",
        "tacks_converted_deg2/Turn_07.csv",
        "tacks_converted_deg2/Turn_08.csv",
        "tacks_converted_deg2/Turn_09.csv"
    ]
    csv_files6 = [
        "tacks_converted_deg2/Turn_11.csv",
        "tacks_converted_deg2/Turn_12.csv",
        "tacks_converted_deg2/Turn_13.csv",
        "tacks_converted_deg2/Turn_14.csv",
        "tacks_converted_deg2/Turn_15.csv",
        "tacks_converted_deg2/Turn_16.csv"
        #"tacks_converted_deg1/Turn_14.csv"
    ]
    #plot_multiple_csv_files(csv_files1)
    #plot_multiple_csv_files(csv_files2)
    plot_multiple_csv_files(csv_files3)
    #plot_multiple_csv_files(csv_files4)
    #plot_multiple_csv_files(csv_files5)
    #plot_multiple_csv_files(csv_files6)
