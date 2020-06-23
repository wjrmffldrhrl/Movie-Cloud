# Movie Crawling 
## 리뷰 크롤링


```python
import os # 폴더와 파일 생성을 위한 모듈
import re # 정규 표현식 사용을 위한 모듈

# 웹 통신을 위해 필요한 모듈
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote
from urllib.error import HTTPError

# 크롤링을 위해 필요한 모듈 BeautifulSoup
from bs4 import BeautifulSoup

# 문자열 비교를 위한 모듈
from operator import eq
```


```python
# Web Page에서 html data를 추출하여 BeautifulSoup 객채를 반환
def getBs(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html, 'html.parser')
    except AttributeError as e:
        return None
    return bs
```


```python
# 네이버 영화 순위 페이지에서 원하는 만큼 영화 리스트를 추출
# 1페이지부터 시작되며 
# 매개변수로 전달한 페이지 위치만큼 크롤링을 진행한다.
def get_moviechart(limit): # 영화 순위 리스트 추출
    page=1
    base_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=99999999&page='
    moviehome = 'https://movie.naver.com'
    count = 0
    movie_list = list()
    while True:
        url = base_url+str(page)
        bs = getBs(url)
        movies = bs.find('table').findAll('a',{'href':re.compile('/movie/bi/mi/basic.nhn*')})
        
        for movie in movies:
            print(movie.get_text())
            movie_list.append(moviehome+movie.attrs['href'])
        count += 1
        page += 1
        if count>limit:
            break
            
    return movie_list

```


```python
# 제목, 포스터이미지, 관람객 평점, 줄거리 등등
# 영화의 기본적인 정보를 추출한다. 
def get_movieinfo(url):
    
    movie_info = list()
    
    base_url = url
    code =base_url[base_url.find('code=')+5:]
    
    
    detail_url = 'https://movie.naver.com/movie/bi/mi/detail.nhn?code='
    bs = getBs(base_url)
    
    # 제목
    title = get_title(code)
    
    #poster
    poster = get_posturl(code)
    
    # 관람객 평점
    score = bs.find('span',{'class':'st_off'}).get_text()

    
    ## 줄거리
    con_tx = bs.find('p',{'class':'con_tx'})
    story = con_tx.get_text().replace('\xa0','').replace('\r','')

    ## 개봉일
    data = bs.findAll('a',{'href':re.compile('/movie/sdb/browsing/bmovie.nhn*')})
    day = list()
    for info in data:
        if '/movie/sdb/browsing/bmovie.nhn?open' in info.attrs['href']:
            now = info.get_text().replace(' ','')
            if now in day:
                pass
            else:
                day.append(now)
    day = ''.join(day)
    
    
    # 배우
    bs = getBs(detail_url+code)

    name = bs.findAll('div',{'class','p_info'})
    actors = list()

    for actor in name:
        part = actor.find('em',{'class':'p_part'}).get_text()
        if part == '주연':
            actors.append(actor.a.get_text())
    
    
    # 감독
    d_name = bs.findAll('div',{'class':'dir_obj'})
    director = list()
    for d in d_name:
        director.append(d.div.a.get_text())
    
    
    
    movie_info.append(title)
    movie_info.append(story)
    movie_info.append(actors)
    movie_info.append(director)
    movie_info.append(poster)
    movie_info.append(day)
    movie_info.append(score)
    

    text = ''

    for data in movie_info:
        if type(data) == str:
            text+=''.join(data)
        else:
            text+=','.join(data)
        text+='\n'
    
    print(text)

    f = open(title+'/'+title+'.txt','w',-1, "utf-8")
    f.write(text)
    f.close()
    
    return movie_info

```


```python
# 영화 리뷰 데이터가 저장될 디렉터리와 택스트파일 생성
def get_txtfile(rev,filename):
    text = ' '.join(rev)
    path = filename+'/'
    f = open(path+filename+'_rev'+'.txt','w',-1, "utf-8")
    
    f.write(text)
    f.close()
```


```python
# 영화 리뷰 추출
def get_rev(url,limit):
    code = url[url.find('code='):]
    sub_url_front= 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?'
    sub_url_back = '&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=
    false&isMileageSubscriptionReject=false&page='
    page = 1
    target = sub_url_front+code+sub_url_back+str(page)
    bs = getBs(target)
    count = 0
    
    rev = list()
    while True:
        print('craw'+str(page)+'page')
        review_data = bs.findAll('span',{'id':re.compile('_filtered_ment_*')})
    
    
        for i in review_data:
            #print(i.get_text().strip())
            rev.append(i.get_text().strip())
        
        count+=1
        page +=1
        target = sub_url_front+code+sub_url_back+str(page)
        bs = getBs(target)
        
        if bs.find('a',{'title':'다음'}) is None:
            print('no data')
            break
        elif count >= limit:
            print('limit')
            break
    
    
    
    return rev
    
```


```python
# 영화 제목 추출
def get_title(code):
    url = 'https://movie.naver.com/movie/bi/mi/point.nhn?code='+code
    
    bs = getBs(url)
    title = bs.find('h3',{'class':'h_movie'}).a.get_text()
    
    title = list(title)
    stopchar = ['/',':','*','?','<','>','|','"','.']
    
    for i in stopchar:
        if i in title:
            title.remove(i)
    
 
    title = ''.join(title)
    
    return title

# get_title('167613')
```


```python
# 영화 이미지 파일 생성
def get_postimg(code):
    #code = 179482
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+code
    title = get_title(code)
    bs = getBs(url)
    img_src = bs.find('img',{'id':'targetImage'})
    downlink = img_src.attrs['src']
    urlretrieve(downlink,title+'/'+title+'.jpg')
```


```python
# 영화 이미지 주소
def get_posturl(code): 
    url = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+code
    title = get_title(code)
    bs = getBs(url)
    img_src = bs.find('img',{'id':'targetImage'})
    downlink = img_src.attrs['src']
    return downlink
```


```python
# 영화 제목을 추출한 뒤 
# 디렉터리 생성에 문제가 생기는 문자를 제거
def get_data(url):# 영화 
    code = url[url.find('code=')+5:]
    print('code : '+code)
    
    title = get_title(code)
    print('title : '+title)
    


    os.makedirs(title) # 타이틀 이름 중 안되는 문자 제거할 것
                       # \ / : * ? " < > |
    
    
    get_postimg(code)
    rev = get_rev(url,1000)
    
    get_txtfile(rev,title)
    
    return title
    
```

# Word Cloud
## 워드 클라우드 이미지 생성


```python
# 차트 생성용 모듈
import matplotlib.pyplot as plt
%matplotlib inline

from matplotlib import font_manager, rc

# 자연어 처리 모듈 nltk
import nltk

# 한글 자연어 처리 모듈 kolaw
from konlpy.corpus import kolaw
from konlpy.tag import Okt; t = Okt()
from konlpy.tag import Kkma

# OS에 따른 폰트 설정
import platform

# WordCloud 생성 모듈
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS


# 데이터 분석용 모듈 numpy
import numpy as np
from PIL import Image

# 한국어 모듈 실행
kkma = Kkma()
```


```python
# 생성해둔 리뷰 데이터를 제목으로 접근하여 얻어낸다.
def get_word(title):
    text = open(title+'/'+title+'_rev'+'.txt','r',-1,"utf-8").read()
    tokens = t.nouns(text)

    # 1글자 , 영화 제거
    tokens = [word for word in tokens if len(word) > 1 and word != '영화']

    word = nltk.Text(tokens, name='영화 리뷰')
    
    return word
```


```python
# 추출한 리뷰 데이터와 포스터를 기반으로
# 워드클라우드 이미지를 생성한다.
def get_wrodcloud(word,title):

    # 폰트설정
    if platform.system()  == 'Darwin':
        rc('font',family='AppleGothic')
    elif platform.system() == 'Windows':
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    else:
        print('unknown system')
    
    %matplotlib inline

    data = word.vocab().most_common(1000)
    tmp_data = dict(data)
    
    movie_coloring = np.array(Image.open(title+'/'+title+'.jpg'))

    image_colors = ImageColorGenerator(movie_coloring)

    wordcloud = WordCloud(font_path='c:/Windows/Fonts/malgun.ttf',
                         relative_scaling = 0.08, mask=movie_coloring,
                         background_color='white',max_words = 2000#,min_font_size=1,max_font_size=20,random_state=50
                         ).generate_from_frequencies(tmp_data)

    plt.figure(figsize=(30,30))
    plt.imshow(wordcloud.recolor(color_func=image_colors),interpolation='bilinear')
    plt.axis('off')
    plt.savefig(title+'/'+title+'_wordcloud'+'.png', format="png")
    plt.show()

```

# Crawling & wordcloud start


```python
chart = get_moviechart(3)

for movie in chart:
    title = get_data(movie)
    get_movieinfo(movie)
    word = get_word(title)
    get_wrodcloud(word,title)
```
