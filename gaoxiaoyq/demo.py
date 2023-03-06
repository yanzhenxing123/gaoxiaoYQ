import random

for i in range(1000):
    print("Predicting::第{}条新闻".format(i))
    print("分类结果为{}".format([random.randint(0,1) for _ in range(6)]))