import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
from src import overall_analysis

def line_graph(df ,x , y, x_label , y_label):
    fig =px.line(df,x = x , y = y )
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    return fig


def heatmaps(df , index , columns , values ,agg_func):
    pivot = df.pivot_table(
        index=index , 
        columns=columns , 
        values = values  , 
        aggfunc=agg_func).fillna(0).astype('int')
     
    fig = px.imshow(
        pivot,
        color_continuous_scale="Blues",
        labels=dict(
            x=columns,
            y=index,
            color=values   
        ),
        aspect="auto"
    )

    fig.update_traces(
        hovertemplate=(
            f"{index}: %{{y}}<br>"
            f"{columns}: %{{x}}<br>"
            f"{values}: %{{z}}"  
            "<extra></extra>"
        )
    )

    fig.update_layout(height=900)
    return fig 

def dist_plots(dist_list , dist_name):
    fig = ff.create_distplot(dist_list,dist_name , show_hist=False , show_rug=False)
    fig.update_layout(height = 500 ,
                      width = 1000,
                      xaxis_title="Age (years)",
                      yaxis_title="Density")
    return fig

def scatterplot(athlete_df):
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=athlete_df,
        x="Weight",
        y="Height",
        hue="Medal",
        hue_order=["No Medal", "Gold", "Bronze", "Silver"],  
        style="Sex",
        style_order=["M", "F"],                              
        s=40,
        alpha=0.75,
        ax=ax
    )
    ax.legend(
            loc="upper left",
            bbox_to_anchor=(1.01, 1),
            frameon=True,
            fontsize=6,          
            markerscale=0.6,     
            labelspacing=0.3,    
            borderpad=0.2,       
            handletextpad=0.5    
        )

    # ---- Axis settings ----
    sns.set_style("white")
    sns.despine(ax=ax , left=True, bottom=True)
    ax.yaxis.grid(True)
    ax.xaxis.grid(False)
    ax.set_xlabel("Weight (kg)")
    ax.set_ylabel("Height (cm)")

    fig.subplots_adjust(right=0.80)
    ax.tick_params(axis='both', labelsize=6, colors='gray')
    return fig



