import streamlit as  st 
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]

    recommend_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommended_movies_posters

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similariry.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    (movies['title'].values),
)

# if st.button("Recommend"):
#     names, posters = recommend(selected_movie_name)

#     cols = st.columns(5)

#     for i in range(5):
#         with cols[i]:
#             st.text(names[i])
#             st.image(posters[i])
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-weight:bold;
                    padding-top:10px;
                    min-height:70px;
                ">
                    {names[i]}
                </div>
                """,
                unsafe_allow_html=True
            )
