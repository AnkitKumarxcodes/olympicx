import streamlit as st
from data.data_loader import load_data
import pandas as pd
from src import (
    preprocessor,
    medal_analysis,
    overall_analysis,
    country_wise_analysis,
    athlete_analysis
)
from ui import charts
from ui.metrics import colored_metric, inject_metric_styles
import seaborn as sns
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px


# ---------------- Page config ----------------
st.set_page_config(
    page_title="OlympiX Analytics",
    layout="wide"
)


# ---------------- Cached data loading & preprocessing ----------------
@st.cache_data
def load_and_preprocess():
    df, region_df = load_data()
    df = preprocessor.preprocess(df, region_df)
    return df, region_df


df, region_df = load_and_preprocess()


# ---------------- Cached helper functions ----------------
@st.cache_data
def cached_country_year_list(df):
    return medal_analysis.country_year_list(df)


@st.cache_data
def cached_participating(df, col):
    return overall_analysis.participating_nation_overtime(df, col)


@st.cache_data
def cached_height_weight(df, sport):
    return athlete_analysis.height_weight_df(df, sport)


@st.cache_data
def cached_men_vs_women(df):
    return athlete_analysis.men_vs_women(df)


@st.cache_data
def cached_country_success(df, country):
    return country_wise_analysis.country_successful_sport(df, country)


@st.cache_data
def cached_year_wise_medals(df, country):
    return country_wise_analysis.year_wise_medals(df, country)


@st.cache_data
def cached_top_10_athletes(df, country):
    return country_wise_analysis.top_10_athlete(df, country)


# ---------------- Sidebar ----------------
st.sidebar.title("OlympiX Analytics")
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/"
    "Olympic_rings_with_transparent_rims.svg/1024px-Olympic_rings_with_transparent_rims.svg.png"
)

user_menu = st.sidebar.radio(
    "Select an Option",
    (
        "Overall Analysis",
        "Medal Tally",
        "Country-wise Analysis",
        "Athlete wise Analysis"
    )
)


# ============================= Overall Analysis =============================
if user_menu == "Overall Analysis":

    editions = df["Year"].nunique() - 1
    cities = df["City"].nunique()
    nations = df["region"].nunique()
    events = df["Event"].nunique()
    athletes = df["Name"].nunique()
    sports = df["Sport"].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        colored_metric("Editions", editions, "#e76f51")
    with col2:
        colored_metric("Cities", cities, "#457b9d")
    with col3:
        colored_metric("Nations", nations, "#2a9d8f")

    col4, col5, col6 = st.columns(3)
    with col4:
        colored_metric("Events", events, "#f4a261")
    with col5:
        colored_metric("Athletes", athletes, "#6a4c93")
    with col6:
        colored_metric("Sports", sports, "#264653")

    nations_over_time = cached_participating(df, "region")
    fig1 = charts.line_graph(
        nations_over_time,
        nations_over_time.columns[0],
        nations_over_time.columns[1],
        "Edition",
        "no. of countries"
    )
    st.title("Participating nations over time")
    st.plotly_chart(fig1, use_container_width=True)

    events_over_time = cached_participating(df, "Event")
    fig2 = charts.line_graph(
        events_over_time,
        events_over_time.columns[0],
        events_over_time.columns[1],
        "Edition",
        "Events"
    )
    st.title("Events Over the Years")
    st.plotly_chart(fig2, use_container_width=True)

    athletes_over_time = cached_participating(df, "Name")
    fig3 = charts.line_graph(
        athletes_over_time,
        athletes_over_time.columns[0],
        athletes_over_time.columns[1],
        "Edition",
        "no of athletes"
    )
    st.title("Participating Athletes Over the Years")
    st.plotly_chart(fig3, use_container_width=True)

    st.title("No. of Events in Every Sport Over the Years")
    fig = charts.heatmaps(df, "Sport", "Year", "Event", "nunique")
    st.plotly_chart(fig, use_container_width=True)

    years, country, sport = cached_country_year_list(df)

    st.title("🏆 Leaderboards")
    selected_filter = st.selectbox("Filter by", ["Athletes", "Country"])
    selected_year = st.selectbox("Year", years)
    selected_sport = st.selectbox("Sport", sport)

    if selected_filter == "Athletes":
        st.dataframe(
            overall_analysis.leaderboard(
                df,
                entity="athlete",
                year=selected_year,
                sport=selected_sport
            ),
            use_container_width=True
        )

    if selected_filter == "Country":
        st.dataframe(
            overall_analysis.leaderboard(
                df,
                entity="country",
                year=selected_year,
                sport=selected_sport
            ),
            use_container_width=True
        )


# ============================= Medal Tally =============================
if user_menu == "Medal Tally":

    years, country, sport = cached_country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = medal_analysis.fetch_medal_tally(
        df, selected_year, selected_country
    )

    INITIAL_ROWS = 10
    filter_key = (selected_year, selected_country)

    if "show_all" not in st.session_state:
        st.session_state.show_all = False
        st.session_state.prev_filter = filter_key

    if st.session_state.prev_filter != filter_key:
        st.session_state.show_all = False
        st.session_state.prev_filter = filter_key

    display_df = medal_tally if st.session_state.show_all else medal_tally.iloc[:INITIAL_ROWS]
    st.dataframe(display_df, use_container_width=True)

    if not st.session_state.show_all and len(medal_tally) > INITIAL_ROWS:
        if st.button("⬇ Show more"):
            st.session_state.show_all = True
            st.rerun()


# ============================= Country-wise Analysis =============================
if user_menu == "Country-wise Analysis":

    years, country, sport = cached_country_year_list(df)
    selected_country = st.sidebar.selectbox(
        "Select Country",
        country[1:],
        index=191
    )

    st.title(f"Medal Trends of {selected_country}")
    country_wise_medals = cached_year_wise_medals(df, selected_country)
    fig1 = charts.line_graph(
        country_wise_medals,
        country_wise_medals.columns[0],
        country_wise_medals.columns[1],
        "Edition",
        "Medals counts"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.title(f"Medal count of {selected_country} in olympics")
    success_sports_countrywise = cached_country_success(df, selected_country)
    fig = charts.heatmaps(
        success_sports_countrywise,
        "Sport",
        "Year",
        "Medal",
        "count"
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------- Top 10 Athletes --------
    st.title(f"Top 10 Athletes of {selected_country}")
    top_10_athletes = cached_top_10_athletes(df, selected_country)
    st.dataframe(top_10_athletes, use_container_width=True)


# ============================= Athlete-wise Analysis =============================
if user_menu == "Athlete wise Analysis":

    st.title("Age distribution of Olympics Athletes")
    x1, x2, x3, x4 = athlete_analysis.age_distribution(df)
    fig = charts.dist_plots(
        [x1, x2, x3, x4],
        ["Age", "Gold Medalists", "Silver Medalists", "Bronze Medalists"]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.title("Age distribution of Olympics Medalists in sports")
    olympic_sports = df["Sport"].value_counts()
    core_sports = olympic_sports[olympic_sports >= 60].index.tolist()
    selected_sports = st.multiselect("Select sports", options=core_sports)

    medal = ["ALL", "Gold", "Silver", "Bronze"]
    medal_type = st.selectbox("Select medal type", medal)

    dist_list, dist_name = athlete_analysis.sports_distribution(
        df, selected_sports, medal_type
    )
    fig = charts.dist_plots(dist_list, dist_name)
    st.plotly_chart(fig, use_container_width=True)

    st.title("Anthropometric Distribution of Olympic Athletes")
    olympic_sport = df["Sport"].unique().tolist() + ["overall"]
    select_sport = st.selectbox(
        "select sport",
        options=olympic_sport,
        index=olympic_sport.index("overall")
    )

    athlete_df = cached_height_weight(df, select_sport)
    fig = charts.scatterplot(athlete_df)
    st.pyplot(fig)

    st.title("Man vs Women athlete Participation through Years")
    man_women_df = cached_men_vs_women(df)
    fig = charts.line_graph(
        man_women_df,
        "Year",
        ["Male", "Female"],
        "Year",
        "Athletes"
    )
    st.plotly_chart(fig, use_container_width=True)


