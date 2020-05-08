# -*- encoding: utf8 -*-
# 需要使用分词和停用词
import jieba

class SensitiveWord():



    def cut_word(self,word):
        return ' ' .join(jieba.cut(word))

    def build_bad_words(self):
        x = []
        with open('广告.txt') as ad_file:
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
        cut_x = []
        for word in x :
            cut_x.append(self.cut_word(word))
        return cut_x

    def build_good_words(self):
        x = []
        with open('nickname.csv') as nickname_file:
            for text in nickname_file.readlines():
                nickname = text.strip()
                # if len(nickname) == 0:
                if len(nickname) == 0 or nickname.startswith("财主"):
                    continue
                else:
                    x.append(nickname)
        cut_x = []
        for word in x:
            cut_x.append(self.cut_word(word))
        print(len(cut_x))
        return cut_x


    def build_stop_word(self):
        stop_words = []
        with open('stopword.dic') as file:
            for line in file.readlines():
                stop_words.append(line.strip())
        return stop_words


    # 0 means good word
    # 1 means bad word
    def build_x_y(self,good_words,bad_words,stop_words):
        train_words = good_words + bad_words
        y = []
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(min_df = 1, stop_words = stop_words)
        x = vectorizer.fit_transform(train_words)
        for word in train_words:
            if word in good_words:
                y.append(0)
            if word in bad_words:
                y.append(1)
        return x.toarray(), y, vectorizer


if __name__ == '__main__':
    ssw = SensitiveWord()
    bad_words = ssw.build_bad_words()
    good_words = ssw.build_good_words()
    stop_words = ssw.build_stop_word()
    stop_words = []

    # print(train_words)
    X,Y,vectorizer = ssw.build_x_y(good_words,bad_words,stop_words)
    # print(X)
    print("特征名字：n", vectorizer.get_feature_names())
    import numpy as np

    from sklearn.naive_bayes import BernoulliNB
    clf = BernoulliNB()
    clf.fit(X, Y)
    # print(clf)
    pre = clf.predict(X)
    print(u"数据集预测结果:", pre)

    score = clf.score(X,Y)
    print(score)



    print("#####开始测试:", good_words[1:10])
    # test_nickname = '测试昵称'
    # test_doc = []
    # test_doc.append(ssw.cut_word(test_nickname))
    # test_vec = vectorizer.transform(test_doc).toarray()
    test_result = clf.predict(X[1:10])
    print(test_result)
    # for i in range(10):
    #     test_set = []
    #     print(train_words[i])
    #     test_set.append(X[i])
    #     test_result = clf.predict(test_set)
    #     print(test_result)



