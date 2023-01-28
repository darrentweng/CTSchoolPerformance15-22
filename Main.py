import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

st.set_page_config(layout="wide")
st.sidebar.title('CT School Performance')
@st.cache
def load_data():
    df = pd.read_csv("sb_final.csv")
    unique_towns = df['Town'].unique().tolist()
    return df,unique_towns
df, all_towns = load_data()

col1, col2, col3, col4 = st.columns(4)
with col1:
    grades = st.multiselect('Grade', ['3','4','5','6','7','8'] ,default=['8'])
with col2:
    subjects = st.multiselect('Subject', ['Math','ELA'], default=['Math'])
with col3:
    races = st.multiselect('Race/Ethnicity', ['Asian','Black or African American','Hispanic/Latino of any race','White'] ,default=['White'])
with col4:
    towns = st.multiselect('Town', all_towns)
cols = ['Per capita income','Population','StudentNo','2015','2016','2017','2018','2021']

option = st.sidebar.radio('Show', ('Table', 'Scatter','Barchart','Map'))

cond = df['Grade'].notna() # initial condition
if len(grades) > 0:
    cond = cond & (df['Grade'].isin(list(map(int, grades))))
if len(races) > 0:
    cond = cond & (df['Race/Ethnicity'].isin(races))
if len(towns) > 0:
    cond = cond & (df['Town'].isin(towns))
if len(subjects) > 0:
    cond = cond & (df['Subject'].isin(subjects))
tbl = df[cond]

if option == 'Table':
    st.dataframe(tbl) #, use_container_width=True)
elif option == 'Scatter':
    xcol = st.sidebar.selectbox('X-Axis', cols, index=cols.index("Per capita income"))
    ycol = st.sidebar.selectbox('Y-Axis', cols, index=cols.index("2021"))
    cat = 'Race/Ethnicity'
    bubble_col = st.sidebar.selectbox('Bubble Size', cols, index=cols.index("StudentNo"))
    plot = tbl[["District",xcol,ycol,bubble_col,cat]].dropna()
    fig = px.scatter(plot, x=xcol, y=ycol, hover_data=["District"],size=bubble_col,color=cat,height=600, trendline="ols") # "lowess" for nonlinear
    st.plotly_chart(fig, use_container_width=True)
elif option == 'Barchart':
    fig = px.bar(tbl, x="District", y="2021", color="Race/Ethnicity", barmode="group")
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig, use_container_width=True)
else:
    bubble_col = st.sidebar.selectbox('Bubble Size', cols, index=cols.index("2021"))

    mapdf = tbl[['District','lon','lat',bubble_col]].dropna(thresh=4)
    bubble_factor = 1.5

    # https://docs.streamlit.io/en/stable/api.html?highlight=pydeck_chart
    st.pydeck_chart( 
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            layers=[
                pdk.Layer("ScatterplotLayer", data=mapdf, get_position='[lon, lat]',
                get_fill_color="[200, 30, 0, 160]",  get_radius=bubble_col+"*"+str(bubble_factor), 
                pickable=True, opacity=0.8, stroked=False, filled=True, wireframe=True,
                )],
            initial_view_state=pdk.ViewState(longitude=-72.40, latitude=41.45, zoom=8, min_zoom=2, max_zoom=15, height=800),
            tooltip={"html": "<b>{District}</b>: {"+bubble_col+"}"}
        ), 
        use_container_width=True)
st.sidebar.write(f"Made with love from the [Weng team](https://devpost.com/software/collegeviz)")