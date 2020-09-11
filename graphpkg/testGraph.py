import plotly.express as px
import pandas as pd

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


def makeTestFigure():
    df = pd.DataFrame({
        "Fruit": ["Apples1", "Oranges", "Bananas", "Apples1", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    return fig
