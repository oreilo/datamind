from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

def plot(df:pd.DataFrame,kind:str,x:str,y:str|None=None):
    if x not in df or (y and y not in df):raise ValueError("Unknown column")
    if kind not in {"bar","line","scatter","hist"}:raise ValueError("Unsupported chart")
    fig,ax=plt.subplots(figsize=(9,5))
    try:
        if kind=="hist":
            if not pd.api.types.is_numeric_dtype(df[x]):raise ValueError("Histogram requires numeric column")
            ax.hist(df[x].dropna(),bins=25)
        elif kind=="scatter":
            if not y:raise ValueError("Scatter requires y")
            ax.scatter(df[x],df[y],alpha=.65)
        elif kind=="line":
            if not y:raise ValueError("Line requires y")
            ax.plot(df[x].head(500),df[y].head(500))
        else:
            if y: df.groupby(x,dropna=False)[y].sum().head(30).plot.bar(ax=ax)
            else: df[x].value_counts().head(30).plot.bar(ax=ax)
        ax.set_title(f"{kind.title()} - {x}");ax.set_xlabel(x)
        if y:ax.set_ylabel(y)
        fig.tight_layout();buf=BytesIO();fig.savefig(buf,format="png",dpi=140);return buf.getvalue()
    finally:plt.close(fig)
