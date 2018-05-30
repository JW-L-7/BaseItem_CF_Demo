# coding: utf-8
"""
Create on 2018/11/13

@author:hexiaosong
"""
"""
用户的相似性通过电影度量
电影相似性通过用户度量

计算相似性的方式: 欧几里得距离、夹角余弦等

基于用户BaseUser_CF:
找出与指定用户最相似的前K名用户 以相似度为权重 加权(相似度)平均(其他用户的评分)方式估算出未观看电影的评分 排序 把前K个排名作为结果推荐

基于物品BaseItem_CF:
计算电影的相似度 找出指定用户最喜爱的前K个电影  计算未观看电影的推荐指数: 加权(相似度)平均(电影评分)  排序 把前K个排名作为结果推荐
"""

import math


class recommender(object):

    def __init__(self, path, usr):
        self.path = path       # 数据路径
        self.usr = usr         # 待推荐用户
        self.usr_rating = {}   # 用户评分字典
        self.load_data(path)


    def load_data(self, path):
        """
        将二维矩阵数据转化为字典形式
        {'Bryan': {'Alien': 2, 'Avatar': 5}, 'Thomas': {'Alien': 5, 'Avatar': 2}}
        """
        with open(path) as f:
            lines = f.readlines()
        usr_name = [i.strip('"') for i in lines[0].strip().split(',')[1:]]
        for line in lines[1:]:
            items = line.strip().split(',')
            movie = items[0].strip('"')
            for index in range(1, len(items)):
                if not items[index] == '':
                    if usr_name[index - 1] not in self.usr_rating:
                        self.usr_rating[usr_name[index - 1]] = {movie: int(items[index])}
                    else:
                        self.usr_rating[usr_name[index - 1]][movie] = int(items[index])

    def o_distance(self, usr1, usr2):
        distance = 0
        for movie in usr1.keys():
            if movie in usr2.keys():
                distance += abs(usr1[movie] - usr2[movie]) ** 2
        return math.sqrt(distance)

    def pearson_distance(self, usr1, usr2):
        """
        欧式距离计算两个用户的相似度
        :param usr1: usr1评分数据: {'Avatar': 4, 'Braveheart': 3, 'Dodgeball': 4, 'Forest Gump': 4, 'Gladiator': 4}
        :param usr2: usr2评分数据: {'Alien': 2, 'Avatar': 5, 'Braveheart': 5, 'Dodgeball': 3, 'Forest Gump': 4}
        :return:
        """
        sum_x_y = 0
        sum_x = 0
        sum_y = 0
        sum_x_2 = 0
        sum_y_2 = 0
        n = 0
        for movie in usr1.keys():
            if movie in usr2.keys():
                n += 1
                x = usr1[movie]
                y = usr2[movie]
                sum_x_y += x * y
                sum_x += x
                sum_y += y
                sum_x_2 += x ** 2
                sum_y_2 += y ** 2
        if n == 0: return 0
        denominator = math.sqrt(sum_x_2 - float(sum_x ** 2) / n) * math.sqrt(sum_y_2 - float(sum_y ** 2) / n)
        if denominator == 0: return 0
        return (sum_x_y - float(sum_x * sum_y) / n) / denominator

    def k_nearst(self, k):
        """取前K个最相似的用户"""
        distances = []
        for usr, rate in self.usr_rating.items():
            if not usr == self.usr:
                distance = self.pearson_distance(self.usr_rating[self.usr], self.usr_rating[usr])
                if distance != 0: distances.append((usr, distance))
        distances.sort(key=lambda item: item[1], reverse=True)
        if k > len(distances):
            return distances
        else:
            return distances[:k]

    def recomend_k(self, nearst, k):
        """
        用前K个相似用户对指定用户未观看的电影
        以相似度为权重 按评分计算加权平均分数作为指定用户对该电影的评分
        """
        recommend = {}
        total_distance = 0
        for item in nearst:
            total_distance += item[1]
        for item in nearst:
            u_name = item[0]
            weight = float(item[1]) / total_distance
            for movie, rate in self.usr_rating[u_name].items():
                if movie not in self.usr_rating[self.usr].keys():   # 其他用户给指定用户没有看的电影计算推荐指数
                    if movie not in recommend.keys():
                        recommend[movie] = rate * weight
                    else:
                        recommend[movie] += rate * weight
        print(recommend)
        top_k = list(recommend.items())
        top_k.sort(key=lambda x: x[1], reverse=True)  # 估计出指定用户未观看电影的评分后排序
        if k > len(top_k):
            return top_k
        else:
            return top_k[:k]

    def run(self):
        nearst = self.k_nearst(5)
        print(nearst)
        top_k = self.recomend_k(nearst, 5)
        for item in top_k:
            print("为您推荐影片:" + item[0] + "\t推荐指数:" + str(item[1]))


if __name__ == '__main__':
    path = '/Users/apple/Downloads/Movie_Ratings.csv'
    r = recommender(path, 'vanessa')
    r.run()
