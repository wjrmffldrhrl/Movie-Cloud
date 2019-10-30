from django.shortcuts import render, redirect
from .models import MovieData
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

def home(request): # 홈페이지
    if request.method == 'GET': # get방식으로 접근 시
        return render(request, 'moviecloud/home.html') # 홈페이지 출력
    elif request.method == 'POST': # 영화 제목을 입력 받은 경우
        title = request.POST.get('title', None)  # 템플릿에서 입력한 name필드에 있는 값을 키값으로 받아옴
        res_data = {}  # 응답 메세지를 담을 변수(딕셔너리)
        #movieDetail = MovieData.objects.get(title=title)
        movieDetail = MovieData.objects.all() # 전체 목록을 가져옴
        cnt = 1
        for row in movieDetail:
            if row == title:
                cnt += 1
                break
        pk = cnt # 제목과 일치하는 pk(primary key) 가져옴
        return redirect('/moviecloud/detail/'+str(pk)) # url로 redirection


def detail(request, pk): # 영화 상세보기 페이지
    if request.method == 'GET': # get 방식으로 접근 시 해당 pk의 영화 상세보기 출력
        movieDetail = MovieData.objects.get(pk=pk)
        return render(request, 'moviecloud/detail.html', {'movieDetail' : movieDetail})

    elif request.method == 'POST': # 돌아가기 버튼 선택 시
        return render(request, 'moviecloud/home.html') # 홈페이지로 돌아감

def inputdata(request): # 크롤링해서 가공된 데이터를 자동화하여 데이터베이스에 입력하기 위한 함수
    if request.method == 'GET':

        for i in range(1, 9):
            lineNum = 1
            f = open('moviedata/'+str(i) + '.txt', 'r',  encoding="utf8")
            while True:
                line = f.readline() # 각 파일을 줄 단위로 읽어옴
                if not line:
                    break
                if lineNum == 1: # 제목
                    title = line
                if lineNum == 2: # 줄거리
                    story = line
                if lineNum == 3: # 주연배우
                    actors = line
                if lineNum == 4: # 감독
                    director = line
                if lineNum == 5: # 포스터 url
                    poster_url = line
                if lineNum == 6: # 영화 개봉일
                    premier = line
                if lineNum == 7: # 관객 별점
                    score = line
                    wordcloud = 'https://raw.githubusercontent.com/kyu9341/Python-Movie-Recommendation/master/Django/MovieRecommendation/uploads/wordclouds/'+title+'_wordcloud.png'
                lineNum += 1 # 라인 넘버 ++

            moviedata = MovieData( # 각 데이터들을 데이터베이스의 하나의 튜플로 저장
                title = title,
                story = story,
                actors=actors,
                director=director,
                poster_url=poster_url,
                premier=premier,
                score=score,
                wordcloud = wordcloud,
            )
            moviedata.save()

            f.close() # 현재 파일 닫고 반복

    return HttpResponse('success') # 성공 메세지 리턴
