import math

from .models import Rate


def make_ratings_expand():
    rate_dict = {}
    rates = Rate.objects.all()

    for rate in rates:
        rate_dict.setdefault(rate.user.username, {}).update({rate.order_product.product.id:rate.rate})

    return rate_dict

def sim_pearson(data, name1, name2):
    avg_name1 = 0
    avg_name2 = 0
    count = 0
    for products in data[name1]:
        if products in data[name2]:  # 같은 영화를 봤다면
            avg_name1 = data[name1][products]
            avg_name2 = data[name2][products]
            count += 1
    try:
        avg_name1 = avg_name1 / count
    except:
        avg_name1 = 0

    try:
        avg_name2 = avg_name2 / count
    except:
        avg_name2 = 0

    sum_name1 = 0
    sum_name2 = 0
    sum_name1_name2 = 0
    count = 0
    for products in data[name1]:
        if products in data[name2]:  # 같은 영화를 봤다면
            sum_name1 += pow(data[name1][products] - avg_name1, 2)
            sum_name2 += pow(data[name2][products] - avg_name2, 2)
            sum_name1_name2 += (data[name1][products] - avg_name1) * (data[name2][products] - avg_name2)
    try:
        return sum_name1_name2 / (math.sqrt(sum_name1) * math.sqrt(sum_name2))
    except:
        return 0

def top_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]


def getRecommendation(data, person, k=3, sim_function=sim_pearson):
    result = top_match(data, person, k)

    score = 0  # 평점 합을 위한 변수
    li = list()  # 리턴을 위한 리스트
    score_dic = dict()  # 유사도 총합을 위한 dic
    sim_dic = dict()  # 평점 총합을 위한 dic

    for sim, name in result:  # 튜플이므로 한번에
        print(sim, name)
        if sim < 0: continue  # 유사도가 양수인 사람만
        for product in data[name]:
            if product not in data[person]:  # name이 평가를 내리지 않은 영화
                score += sim * data[name][product]  # 그사람의 영화평점 * 유사도
                score_dic.setdefault(product, 0)  # 기본값 설정
                score_dic[product] += score  # 합계 구함

                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(product, 0)
                sim_dic[product] += sim

            score = 0  # 영화가 바뀌었으니 초기화한다

    for key in score_dic:
        try:
            score_dic[key] = score_dic[key] / sim_dic[key]  # 평점 총합/ 유사도 총합
        except:
            score_dic[key] = 0
        li.append((score_dic[key], key))  # list((tuple))의 리턴을 위해서.
    li.sort()  # 오름차순
    li.reverse()  # 내림차순
    return li