# -*- encoding: utf8 -*-
# 需要使用分词和停用词
import jieba
import numpy as np

class SensitiveWord():



    def cut_word(self,word):
        return  jieba.cut(word)

    def build_bad_words(self):
        x = []
        with open('risk.txt') as ad_file:
            for text in ad_file.readlines():
                x.append(text.strip().replace(",",''))
        # with open('政治类.txt') as zz_file:
        #     for text in zz_file.readlines():
        #         x.append(text.strip().replace(",",''))
        # with open('涉枪涉爆违法信息关键词.txt',encoding="utf8") as gun_file:
        #     for text in gun_file.readlines():
        #         x.append(text.strip())
        # with open('网址.txt') as site_file:
        #     for text in site_file.readlines():
        #         x.append(text.strip())
        # with open('色情类.txt') as sex_file:
        #     for text in sex_file.readlines():
        #         x.append(text.strip().replace(",",''))

        resp = []
        for word in x :
            cut_word_and_tag = []
            cut_word_and_tag.append(tuple(self.cut_word(word)))
            cut_word_and_tag.append(1)
            resp.append(cut_word_and_tag)
        return resp

    def build_good_words(self):
        x = []
        with open('nickname.txt') as nickname_file:
            for text in nickname_file.readlines():
                nickname = text.strip()
                x.append(nickname)
        resp = []
        for word in x :
            cut_word_and_tag = []
            cut_word_and_tag.append(tuple(self.cut_word(word)))
            cut_word_and_tag.append(0)
            resp.append(cut_word_and_tag)
        return resp


    def build_test_words(self):
        x = []
        with open('test.txt') as nickname_file:
            for text in nickname_file.readlines():
                nickname = text.strip()
                x.append(nickname)
        resp = []
        for word in x :
            cut_word_and_tag = []
            cut_word_and_tag.append(tuple(self.cut_word(word)))
            resp.append(cut_word_and_tag)
        return resp

    def build_stop_word(self):
        stop_words = []
        with open('stopword.dic') as file:
            for line in file.readlines():
                stop_words.append(line.strip())
        return stop_words


    # 0 means good word
    # 1 means bad word
    def build_x_y(self,good_words,bad_words,stop_words):
        train_data = np.array(good_words + bad_words)
        np.random.shuffle(train_data)

        from sklearn.preprocessing import MultiLabelBinarizer
        mlb = MultiLabelBinarizer()
        mlb.fit(train_data[:,0])
        print('特征:\n', mlb.classes_)
        x = mlb.transform(train_data[:,0])
        y = train_data[:,1].tolist()

        print("y轴:\n", y)
        return x, y, mlb


if __name__ == '__main__':
    ssw = SensitiveWord()
    bad_words = ssw.build_bad_words()
    good_words = ssw.build_good_words()
    stop_words = ssw.build_stop_word()
    test_words = ssw.build_test_words()

    stop_words = []
    # print(train_words)
    X, Y, mlb= ssw.build_x_y(good_words,bad_words,stop_words)

    from sklearn.naive_bayes import BernoulliNB
    clf = BernoulliNB()
    clf.fit(X, Y)
    # print(clf)
    pre = clf.predict(X)
    print(u"数据集预测结果:\n", pre)

    score = clf.score(X,Y)
    print("结果打分:\n", score)

    hit_num = 0
    for val in pre:
        hit_num = hit_num +1
    print("命中次数,\n", hit_num)



    print("####测试数据回放:\n")

    test_set = mlb.transform(test_words)
    test_result = clf.predict(test_set)
    print(test_result)









