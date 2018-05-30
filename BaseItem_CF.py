import pandas as pd
import numpy as np

#read the data
data={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'The Night Listener': 3.0}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Just My Luck': 2.0, 'Lady in the Water': 3.0,'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0}, 
'Jack Matthews': {'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

#clean&transform the data
data = pd.DataFrame(data)
#0 represents not been rated
data = data.fillna(0)
#each column represents a movie
mdata = data.T

#calculate the simularity of different movies, normalize the data into [0,1]
np.set_printoptions(3)
mcors = np.corrcoef(mdata, rowvar=0)
mcors = 0.5+mcors*0.5
mcors = pd.DataFrame(mcors, columns=mdata.columns, index=mdata.columns)

#calculate the score of every item of every user
#matrix:the user-movie matrix
#mcors:the movie-movie correlation matrix
#item:the movie id
#user:the user id
#score:score of movie for the specific user 
def cal_score(matrix,mcors,item,user):
    totscore = 0
    totsims = 0
    score = 0
    if pd.isnull(matrix[item][user]) or matrix[item][user]==0:
        for mitem in matrix.columns:
            if matrix[mitem][user]==0:
                continue
            else:
                totscore += matrix[mitem][user]*mcors[item][mitem]
                totsims += mcors[item][mitem]
        score = totscore/totsims
    else:
        score = matrix[item][user]
    return score

#calculate the socre matrix
#matrix:the user-movie matrix
#mcors:the movie-movie correlation matrix
#score_matrix:score matrix of movie for different users 
def cal_matscore(matrix,mcors):
    score_matrix = np.zeros(matrix.shape)
    score_matrix = pd.DataFrame(score_matrix, columns=matrix.columns, index=matrix.index)
    for mitem in score_matrix.columns:
        for muser in score_matrix.index:
            score_matrix[mitem][muser]  = cal_score(matrix,mcors,mitem,muser)
    return score_matrix

#give recommendations: depending on the score matrix
#matrix:the user-movie matrix
#score_matrix:score matrix of movie for different users 
#user:the user id
#n:the number of recommendations
def recommend(matrix,score_matrix,user,n):
    user_ratings = matrix.ix[user]
    not_rated_item = user_ratings[user_ratings==0]
    recom_items = {}
    #recom_items={'a':1,'b':7,'c':3}
    for item in not_rated_item.index:
        recom_items[item] = score_matrix[item][user]
    recom_items = pd.Series(recom_items)
    recom_items = recom_items.sort_values(ascending=False)
    return recom_items[:n]  


if __name__ == '__main__':
    score_matrix = cal_matscore(mdata,mcors)
    user = 'Michael Phillips'
    print(recommend(mdata,score_matrix,user,2))