import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Main Background */

.stApp{
    background-color:#302C2B;
    color:White;
    
}

/* Sidebar */

[data-testid="stSidebar"]{
    background-color:#141414;
}

[data-testid="stSidebar"] *{
    color:white !important;
}

/* Hide Streamlit elements */

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

/* Title */

.main-title{
font-size:45px;
font-weight:bold;
text-align:center;
padding:10px;
color:white;
}

/* KPI Cards */

.card{
background:#141414;
padding:20px;
border-radius:15px;
box-shadow:0px 0px 10px rgba(0,0,0,0.5);
text-align:center;
margin-bottom:10px;
}

.metric-title{
font-size:18px;
color:#b3b3b3;
}

.metric-value{
font-size:35px;
font-weight:bold;
color:white;
}

/* Chart Containers */

.chart-box{
background:#141414;
padding:15px;
border-radius:15px;
margin-top:15px;
}

/* Footer */

.footer{
position:fixed;
bottom:0;
left:0;
width:100%;
background:red;
color:black;
text-align:center;
padding:10px;
font-size:16px;
font-weight:bold;
z-index:999;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():

    df = pd.read_csv("cleaned_netflix.csv")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df = df.dropna(subset=["year_added"])

    df["year_added"] = (
        df["year_added"]
        .astype(int)
    )

    return df


df = load_data()

# ---------------- SIDEBAR ----------------

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/7/75/Netflix_icon.svg",
    width=100
)

st.sidebar.title("Filters")

type_filter = st.sidebar.selectbox(
    "Select Type",
    ["All"] + sorted(df["type"].dropna().unique())
)

year_filter = st.sidebar.slider(
    "Select Year",
    int(df["year_added"].min()),
    int(df["year_added"].max()),
    int(df["year_added"].max())
)

# ---------------- FILTER DATA ----------------

filtered_df = df.copy()

if type_filter != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == type_filter
    ]

filtered_df = filtered_df[
    filtered_df["year_added"] <= year_filter
]


# ---------------- TITLE ----------------

st.markdown(
    """
    <div class='main-title'>
    🎬 NETFLIX ANALYTICS DASHBOARD
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- KPI ----------------

total_titles = len(filtered_df)

movie_count = len(
    filtered_df[
        filtered_df["type"]=="Movie"
    ]
)

tv_count = len(
    filtered_df[
        filtered_df["type"]=="TV Show"
    ]
)

c1,c2,c3=st.columns(3)

with c1:

    st.markdown(
        f"""
        <div class='card'>
        <div class='metric-title'>
        Total Titles
        </div>

        <div class='metric-value'>
        {total_titles}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        f"""
        <div class='card'>
        <div class='metric-title'>
        Movies
        </div>

        <div class='metric-value'>
        {movie_count}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class='card'>
        <div class='metric-title'>
        TV Shows
        </div>

        <div class='metric-value'>
        {tv_count}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Chart background

chart_bg = "#141414"


# ---------------- ROW 1 ----------------

col1,col2 = st.columns(2)

with col1:

    st.subheader("Movies vs TV Shows")

    fig = px.pie(
        filtered_df,
        names="type",
        hole=.5,
        color_discrete_sequence=[
            "#E50914",
            "#ff8080"
        ]
    )

    fig.update_layout(
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    st.subheader("Ratings Distribution")

    rating_data = (
        filtered_df["rating"]
        .value_counts()
        .reset_index()
    )

    rating_data.columns = [
        "rating",
        "count"
    ]

    fig = px.bar(
        rating_data,
        x="rating",
        y="count",
        color="count",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------- ROW 2 ----------------

col3,col4 = st.columns(2)

with col3:

    st.subheader("Yearly Growth")

    year_data = (
        filtered_df.groupby(
            "year_added"
        )
        .size()
        .reset_index(
            name="count"
        )
    )

    fig = px.line(
        year_data,
        x="year_added",
        y="count",
        markers=True
    )

    fig.update_traces(
        line_color="#ffffff"
    )

    fig.update_layout(
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col4:

    st.subheader("Top Countries")

    countries = (
        filtered_df["country"]
        .dropna()
        .str.split(", ")
    )

    all_countries = Counter(
        c
        for sublist in countries
        for c in sublist
    )

    top_countries = pd.DataFrame(
        all_countries.most_common(10),
        columns=["Country","Count"]
    )

    fig = px.bar(
        top_countries,
        x="Count",
        y="Country",
        orientation="h",
        color="Count",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        paper_bgcolor=chart_bg,
        plot_bgcolor=chart_bg,
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ---------------- GENRES ----------------

st.subheader("Top Genres")

genres = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(",")
)

all_genres = Counter(
    g.strip()
    for sublist in genres
    for g in sublist
)

top_genres = pd.DataFrame(
    all_genres.most_common(10),
    columns=["Genre","Count"]
)

fig = px.bar(
    top_genres,
    x="Count",
    y="Genre",
    orientation="h",
    color="Count",
    color_continuous_scale="Reds"
)

fig.update_layout(
    paper_bgcolor=chart_bg,
    plot_bgcolor=chart_bg,
    font_color="White"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ---------------- FOOTER ----------------

st.markdown(
"""
<div class="footer">
Developed by Abishek
</div>
""",
unsafe_allow_html=True
)