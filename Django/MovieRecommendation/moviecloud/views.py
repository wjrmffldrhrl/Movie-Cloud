from django.shortcuts import render
from .models import MovieData
from django.http import HttpResponse

# Create your views here.

def home(request):
    if request.method == 'GET':
        return render(request, 'moviecloud/home.html')
    elif request.method == 'POST':
        title = request.POST.get('title', None)  # 템플릿에서 입력한 name필드에 있는 값을 키값으로 받아옴

        res_data = {}  # 응답 메세지를 담을 변수(딕셔너리)

        if not (title):
            res_data['error'] = '값을 입력해 주세요.'
        else:
            moviedata = MovieData.objects.all()
            movieTitle = MovieData.objects.filter(title = title)

    return render(request, 'moviecloud/home.html')


def detail(request, pk): # 영화 상세보기 페이지
    if request.method == 'GET':
        movieDetail = MovieData.objects.get(pk=pk)
        return render(request, 'moviecloud/detail.html', {'movieDetail' : movieDetail})




