import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ---------------------------
# Load and prepare data
# ---------------------------
df = pd.read_csv("data/processed_sales_data.csv")
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
df = df.dropna(subset=["date"])

# Create a month grouping column
df["year_month"] = df["date"].dt.to_period("M").dt.to_timestamp()

# ---------------------------
# Dash app setup
# ---------------------------
app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

# ---------------------------
# App layout
# ---------------------------
app.layout = html.Div(
    className="page",
    children=[
        html.H1("Pink Morsel Sales Visualiser", className="title"),

        html.Div(
            className="controls",
            children=[
                html.Label("Chart Type:", className="label"),
                dcc.RadioItems(
                    id="chart-type",
                    options=[
                        {"label": "Bar Chart", "value": "bar"},
                        {"label": "Line Chart", "value": "line"},
                    ],
                    value="bar",
                    className="radio-items",
                    labelStyle={"margin-right": "15px"},
                ),
                html.Br(),
                html.Label("Select Region:", className="label"),
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    className="radio-items",
                    labelStyle={"display": "inline-block", "margin-right": "15px"},
                ),
            ],
        ),

        html.Div(
            className="graph-container",
            children=[
                dcc.Graph(id="sales-chart"),
                html.P(
                    "Sales increase noticeably after the price rise on 15 January 2021, "
                    "indicating that the higher price did not reduce demand.",
                    className="insight-text",
                ),
            ],
        ),
    ],
)

# ---------------------------
# Callback for dynamic chart
# ---------------------------
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-radio", "value"),
    Input("chart-type", "value"),
)
def update_chart(selected_region, chart_type):
    # Filter data
    if selected_region == "all":
        df_filtered = df.copy()
    else:
        df_filtered = df[df["region"] == selected_region]

    # Aggregate monthly sales
    df_monthly = df_filtered.groupby("year_month", as_index=False)["sales"].sum()

    # Build chart based on chart type
    if chart_type == "bar":
        fig = px.bar(
            df_monthly,
            x="year_month",
            y="sales",
            hover_data={"sales": True},
            labels={"year_month": "Month", "sales": "Total Sales ($)"},
            title="Monthly Pink Morsel Sales",
            text="sales"
        )
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    else:
        fig = px.line(
            df_monthly,
            x="year_month",
            y="sales",
            hover_data={"sales": True},
            labels={"year_month": "Month", "sales": "Total Sales ($)"},
            title="Monthly Pink Morsel Sales",
        )
        fig.update_traces(mode="lines+markers+text", textposition="top center")

    # Layout improvements
    fig.update_layout(
        xaxis_tickformat="%b %Y",
        template="plotly_white",
        margin=dict(l=40, r=40, t=80, b=40),
    )

    return fig

# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
