import base64
import os
from datetime import datetime
from io import BytesIO

import pandas as pd
from flask import Flask
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route('/')
def pv_simulator():

    # Create data here for plotting
    file_name = os.path.join("services\power_reading_file",
                             "Meter_reading_on_{}_.csv".format(datetime.now().strftime('%Y-%m-%d')))
    data = pd.read_csv(file_name)
    data['time_of_reading'] = pd.to_datetime(data['time_of_reading'])
    data = data[['time_of_reading', 'meter_power_value']].rename(columns={"time_of_reading": "Time of Reading",
                                                                          "meter_power_value": "Power (KW)"})

    # Plot data here
    fig = Figure()
    ax = fig.subplots()
    fig.suptitle('PV Meter Reading', fontsize=20)
    ax.set_xlabel('Time of Reading', fontsize=18)
    ax.set_ylabel('Power (KW)', fontsize=16)
    data.groupby(data["Time of Reading"].dt.hour).plot(x='Time of Reading', y='Power (KW)', ax=ax, legend=False)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
