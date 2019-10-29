from django.shortcuts import render, redirect
from .models import MovieData
from django.urls import reverse
from django.http import HttpResponse

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'moviecloud/home.html')
    elif request.method == 'POST':
        title = request.POST.get('title', None)  # 템플릿에서 입력한 name필드에 있는 값을 키값으로 받아옴
        res_data = {}  # 응답 메세지를 담을 변수(딕셔너리)
        movieDetail = MovieData.objects.get(title=title)
        pk = movieDetail.pk

        print(title, pk)

        return redirect('/moviecloud/detail/'+str(pk)) # url로 redirection


def detail(request, pk): # 영화 상세보기 페이지
    if request.method == 'GET':
        movieDetail = MovieData.objects.get(pk=pk)
        return render(request, 'moviecloud/detail.html', {'movieDetail' : movieDetail})

    elif request.method == 'POST':
        return render(request, 'moviecloud/home.html')
#       return redirect('/moviecloud/')

#def searched(request, title): # 검색시 목록을 출력해줄 페이지
#    if request.method == 'GET':
#        movieDetail = MovieData.objects.filter(title=title)
#        return render(request, 'moviecloud/searched.html', {'movieDetail' : movieDetail})


def inputdata(request):
    if request.method == 'GET':

        for i in range(1, 9):
            lineNum = 1
            f = open('moviedata/'+str(i) + '.txt', 'r',  encoding="utf8")
            while True:
                line = f.readline()
                if not line:
                    break
                if lineNum == 1:
                    title = line
                if lineNum == 2:
                    story = line
                if lineNum == 3:
                    actors = line
                if lineNum == 4:
                    director = line
                if lineNum == 5:
                    poster_url = line
                if lineNum == 6:
                    premier = line
                if lineNum == 7:
                    score = line
                    wordcloud = '/upload/wordclouds/'+title+'_wordcloud.jpg'
                lineNum += 1

            moviedata = MovieData(
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

            f.close()
    return HttpResponse('success')
