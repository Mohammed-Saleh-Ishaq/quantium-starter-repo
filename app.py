import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load the processed data
df = pd.read_csv("data/processed_sales_data.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

# Drop rows with invalid dates
df = df.dropna(subset=["date"])

# Aggregate sales by day and sort
df_daily = (
    df.groupby("date", as_index=False)["sales"]
    .sum()
    .sort_values("date")
)

# Create line chart
fig = px.line(
    df_daily,
    x="date",
    y="sales",
    title="Total Daily Pink Morsel Sales",
    labels={
        "date": "Date",
        "sales": "Total Sales"
    }
)

# Initialize Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div(
    children=[
        html.H1("Pink Morsel Sales Visualiser"),
        dcc.Graph(figure=fig)
    ]
)

# Run the app
if __name__ == "__main__":
    print("App is starting...")
    app.run(debug=True)
