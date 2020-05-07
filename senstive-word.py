# -*- encoding: utf8 -*-

class SensitiveWord():

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
        with open('色情类.txt') as sex_file:
            for text in sex_file.readlines():
                x.append(text.strip().replace(",",''))
        return x

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
        return x

    def bagOfWords2VecMN(self,vocabList, inputSet):
        returnVec = [0] * len(vocabList)
        for word in inputSet:
            if word in vocabList:
                returnVec[vocabList.index(word)] += 1
        return returnVec


    # 0 means good word
    # 1 means bad word
    def build_x_y(self,good_words,bad_words,train_words):
        y = []
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(min_df=1)
        x = vectorizer.fit_transform(train_words)
        for word in train_words:
            if word in good_words:
                y.append(0)
            if word in bad_words:
                y.append(1)

        return x.toarray(),y


if __name__ == '__main__':
    ssw = SensitiveWord()
    bad_words = ssw.build_bad_words()
    good_words = ssw.build_good_words()

    train_words = list(set(good_words) | set(bad_words))
    # print(train_words)
    X,Y = ssw.build_x_y(good_words,bad_words,train_words)
    # print(X)

    import numpy as np

    from sklearn.naive_bayes import BernoulliNB
    clf = BernoulliNB()
    clf.fit(X, Y)
    # print(clf)
    pre = clf.predict(X)
    # print(u"数据集预测结果:", pre)

    score = clf.score(X,Y)
    print(score)



    print("#####开始测试")
    test_doc = "胡八一"
    test_vec = np.array(ssw.bagOfWords2VecMN(train_words,test_doc))
    test_set = []
    print(test_doc)
    test_set.append(test_vec)
    test_result = clf.predict(test_set)
    print(test_result)
    # for i in range(10):
    #     test_set = []
    #     print(train_words[i])
    #     test_set.append(X[i])
    #     test_result = clf.predict(test_set)
    #     print(test_result)



