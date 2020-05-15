# -*- encoding: utf8 -*-
# 需要使用分词和停用词
import jieba
import numpy as np

class SensitiveWord():



    def cut_word(self,word):
        resp = []
        for sub_word in jieba.cut(word):
            if sub_word.isdigit():
                continue
            else:
                resp.append(sub_word)
        if len(resp) == 0:
            return None
        return ' ' .join(resp)

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
        return x

    def build_good_words(self):
        x = []
        with open('nickname.txt') as nickname_file:
            for text in nickname_file.readlines():
                nickname = text.strip()
                # if len(nickname) == 0:
                if len(nickname) == 0 or nickname.startswith("财主"):
                    continue
                else:
                    x.append(nickname)
        return x


    def build_stop_word(self):
        stop_words = []
        with open('stopword.dic') as file:
            for line in file.readlines():
                stop_words.append(line.strip())
        return stop_words


    def build_data_set(self, words,flag):
        data_set = []
        for word in words:
            item = []
            cut_words = self.cut_word(word)
            if cut_words != None:
                item.append(cut_words)
                item.append(flag)
                data_set.append(item)
        print(data_set)
        return data_set

    # 0 means good word
    # 1 means bad word
    def build_x_y(self,good_words,bad_words,stop_words):
        train_data = np.array(self.build_data_set(good_words,0)
                              + self.build_data_set(bad_words,1))

        # print(train_data.toarray())
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(min_df = 1, stop_words = stop_words)
        x = vectorizer.fit_transform(train_data[:,0].tolist())
        print("特征名字：\n", vectorizer.get_feature_names())
        y = train_data[:,1].tolist()
        print("y轴,\n",y)
        return x.toarray(), y, vectorizer


    def build_test_words(self):
        x = []
        with open('test.txt') as nickname_file:
            for text in nickname_file.readlines():
                nickname = text.strip()
                x.append(nickname)
        return x

    def test_one_by_one(self,vectorizer,word):
        test_nickname = word
        test_doc = []
        test_doc.append(ssw.cut_word(test_nickname))
        test_vec = vectorizer.transform(test_doc).toarray()
        test_result = clf.predict(test_vec)
        print("测试词汇, 对应结果, \n",word , test_result)

if __name__ == '__main__':
    ssw = SensitiveWord()
    bad_words = ssw.build_bad_words()
    good_words = ssw.build_good_words()
    stop_words = ssw.build_stop_word()
    test_word = ssw.build_test_words()

    stop_words = []

    # print(train_words)
    X,Y,vectorizer = ssw.build_x_y(good_words,bad_words,stop_words)
    import numpy as np

    from sklearn.naive_bayes import BernoulliNB
    clf = BernoulliNB()
    clf.fit(X, Y)
    # print(clf)
    pre = clf.predict(X)
    print(u"数据集预测结果,\n", pre)
    score = clf.score(X,Y)
    print("数据集预测打分,\n", score)


    for word in test_word:
        ssw.test_one_by_one(vectorizer,word)



