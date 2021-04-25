import base64
from datetime import datetime
from io import BytesIO

import pandas as pd
from flask import Flask
from matplotlib.figure import Figure

from settings import LOG_DIR_PATH, LOG_FILE_NAME_TEMPLATE

app = Flask(__name__)


@app.route('/')
def pv_simulator():

    # Create data here for plotting
    file_name = LOG_DIR_PATH.joinpath(LOG_FILE_NAME_TEMPLATE.format(datetime.now().strftime('%Y-%m-%d')))
    data = pd.read_csv(file_name)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data = data[['timestamp', 'sum']].rename(
        columns={
            "timestamp": "timestamp",
            "sum": "Power (KW)"
        }
    )

    # Plot data here
    fig = Figure()
    ax = fig.subplots()
    fig.suptitle('PV Simulation (refresh to see current data)', fontsize=20)
    ax.set_xlabel('timestamp', fontsize=18)
    ax.set_ylabel('Power (KW)', fontsize=16)
    data.groupby(data["timestamp"].dt.hour).plot(x='timestamp', y='Power (KW)', ax=ax, legend=False)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")

    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
