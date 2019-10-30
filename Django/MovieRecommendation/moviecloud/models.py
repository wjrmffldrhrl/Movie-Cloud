from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class MovieData(models.Model):
    title = models.CharField(max_length=100, verbose_name='영화 제목')
    story = models.TextField(verbose_name='줄거리')
    actors = models.CharField(max_length=100, verbose_name='주연 배우')
    director = models.CharField(max_length=100, verbose_name='감독')
#    genre = models.CharField(max_length=100, verbose_name='장르')
#    poster = models.ImageField(upload_to='posters', blank=True, verbose_name='포스터 이미지')
    poster_url = models.URLField(max_length=400, blank=True, verbose_name='포스터 URL')
    wordcloud = models.CharField(max_length=400, verbose_name='wordcloud 이미지 경로')
#    wordcloud = models.ImageField(upload_to='wordclouds', blank=True, verbose_name='wordcloud 이미지')
#    wordcloud_url = models.URLField(max_length=400, blank=True, verbose_name='워드클라우드 URL')
    premier = models.CharField(max_length=100, verbose_name='영화 개봉일')
    score = models.CharField(max_length=100, verbose_name='평점')

    def __str__(self): # 클래스가 문자열로 변환될 때 사용되는 내장함수
        return self.title


    class Meta:
        db_table = 'MovieData'
        verbose_name = '영화 데이터'
        verbose_name_plural = '영화 데이터' # 복수형 표현도 설정
