import argparse
from datetime import datetime

import pandas as pd
import panel as pn
import plotly.graph_objects as go
from google.cloud import bigquery
from ipywidgets import widgets

# Initialize Panel and set up widgets
pn.extension("plotly")

# Initialize BigQuery client
client = bigquery.Client()

# Argument parser
parser = argparse.ArgumentParser(
    description="Plot time series data with prediction intervals."
)
parser.add_argument(
    "--forecast_gbq_table",
    type=str,
    required=True,
    help="Forecast table name in BigQuery",
)
args = parser.parse_args()

# Date picker and dropdown widgets
start_date_widget = widgets.DatePicker(
    description="Start Date",
    value=datetime(2017, 1, 1),  # Default start date 2017-01-01
)
utility_widget = widgets.Dropdown(
    options=[
        "AEP",
        "COMED",
        "DAYTON",
        "DEOK",
        "DOM",
        "DUQ",
        "EKPC",
        "FE",
        "NI",
        "PJME",
        "PJMW",
    ],  # Replace with actual utility options
    value="PJMW",
    description="Utility",
)


# Define function to fetch and filter data
def fetch_data(client, forecast_gbq_table, start_date, utility):
    # Query to fetch the time series data
    query = f"""
        SELECT
            time_series_timestamp AS timestamp,
            time_series_data/1000 AS data,
            time_series_adjusted_data/1000 AS adjusted,
            prediction_interval_lower_bound/1000 AS lower_bound,
            prediction_interval_upper_bound/1000 AS upper_bound
        FROM
            `kv-ds-lder-der.hackathon_q1_2024.{forecast_gbq_table}`
        WHERE utility = "{utility}"
        ORDER BY timestamp
    """

    # Run the query and get the data as a pandas DataFrame
    df = client.query(query).to_dataframe()
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(None)

    # Filter data based on start_date
    return df[df["timestamp"] >= pd.to_datetime(start_date)]


# Define function to create the plot
def plot_time_series(df_filtered, start_date):
    # Create a plotly figure
    fig = go.Figure()

    # Add original and adjusted data lines
    fig.add_trace(
        go.Scatter(
            x=df_filtered["timestamp"],
            y=df_filtered["data"],
            mode="lines",
            name="Original Data",
            line=dict(color="blue"),
            opacity=0.5,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_filtered["timestamp"],
            y=df_filtered["adjusted"],
            mode="lines",
            name="Modeled Data",
            line=dict(color="orange"),
            opacity=0.5,
        )
    )

    # Add prediction interval as a filled area
    fig.add_trace(
        go.Scatter(
            x=pd.concat(
                [df_filtered["timestamp"], df_filtered["timestamp"][::-1]]
            ),
            y=pd.concat(
                [df_filtered["lower_bound"], df_filtered["upper_bound"][::-1]]
            ),
            fill="toself",
            fillcolor="lightgray",
            line=dict(color="lightgray"),
            showlegend=True,
            name="Prediction Interval",
            opacity=0.5,
        )
    )

    # Set plot layout
    fig.update_layout(
        title=f"Time Series Data with Prediction Interval (from {start_date})",
        xaxis_title="Timestamp",
        yaxis_title="GW",
        xaxis=dict(tickangle=45),
        template="plotly_white",
    )

    return fig


# Interactive callback
def update_plot(start_date, utility):
    df_filtered = fetch_data(
        client,
        args.forecast_gbq_table,
        start_date_widget.value,
        utility_widget.value,
    )
    fig = plot_time_series(df_filtered, start_date_widget.value)
    return pn.pane.Plotly(fig, sizing_mode="stretch_width")


# Set up the layout
layout = pn.Column(
    pn.Row("### Select Filters:"),
    pn.Row(
        pn.pane.IPyWidget(start_date_widget), pn.pane.IPyWidget(utility_widget)
    ),
    pn.bind(update_plot, start_date_widget, utility_widget),
)

# Launch the Panel app
if __name__ == "__main__":
    layout.show()
