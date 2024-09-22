import pickle
import streamlit as st
st.set_page_config("Movie Recommender",page_icon="🎥")
import requests
import time
url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/"

querystring = {"exact":"false","titleType":"movie"}

headers = {
	"x-rapidapi-key": st.secrets['api_key'],
	"x-rapidapi-host": "moviesdatabase.p.rapidapi.com"
}




def fetch_poster(movie_id,title):
    response = requests.get(url+title, headers=headers, params=querystring)
    response=response.json()
    if 'results' in response and response['results']!=None:
            img=''
            for i in response['results']:
                if i['primaryImage']!='null':
                    img=i['primaryImage']['url']
                    break
            return img if img else 'https://img.freepik.com/free-photo/old-building-walls-grunge-stained-weathered-run-down-generative-ai_188544-12818.jpg'

    return 'https://img.freepik.com/free-photo/old-building-walls-grunge-stained-weathered-run-down-generative-ai_188544-12818.jpg'

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id,movies.iloc[i[0]].title))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        time.sleep(2)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0],use_column_width=True)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
