from bs4 import BeautifulSoup
import json

nextPeople = []
f = open('index.html', 'rb')
bsObj_following = BeautifulSoup(f.read(), "html.parser")
f.close()
def getNextPeople(html):

    items = bsObj_following.find('div', {'id':'data'})['data-state'].encode()
    print(items.decode())
    a = items.decode()
    items = json.loads(a.replace("'", ' '))

    def get_ids():
        id = 'aton'
        # print(items)
        # 获取20个ID中5000热度以上的ID
        ids = items['people']['followingByUser'][id]['ids']
        ids = [i for i in ids if i != None]
        users = items['entities']['users']
        followers = []
        for i in ids:
            if int(users[i]['followerCount']) >= 5000:
                followers.append(i)
        # followers = sorted(followers.items(), key=lambda x:x[1], reverse = True)
        print(followers)
        return followers

    def get_information():
        id = 'aton'
        x = items['entities']['users'][id]
        personal = {}
        information = ['urlToken','name','gender','description','headline','voteupCount','favoritedCount','followerCount','thankedCount','answerCount','articlesCount','questionCount','followingQuestionCount','followingCount','sinaWeiboUrl','sinaWeiboName','logsCount']
        for i in information:
            try:
                personal[i] = x[i]
            except:
                personal[i] = ' '

        try:
            personal['employments'] = x['employments'][0]['company']['name']
        except:
            personal['employments'] = ' '

        try:
            personal['business'] = x['business']['name']
        except:
            personal['business'] = ' '

        try:
            personal['locations'] = x['locations'][0]['name']
        except:
            personal['locations'] = ' '

        print(personal)
        return personal


    get_ids()
    get_information()

getNextPeople('')