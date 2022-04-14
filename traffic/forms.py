from django import forms
from datetime import datetime
from .validate import validate_sido, validate_gugun




class TrafficInfoForm(forms.Form):
    searchYear = forms.IntegerField(max_value=datetime.now().year, min_value=2012)
    siDo = forms.IntegerField(validators=[validate_sido])
    guGun = forms.IntegerField(validators=[validate_gugun])
    numOfRows = forms.DecimalField(max_digits=4, min_value=1)
    pageNo = forms.DecimalField(max_digits=4, min_value=1)
    select = forms.DecimalField(min_value=1, max_value=2)
    labels = {
        'searchYear': '발생연도',
        'siDo': '시도코드',
        'guGun': '시군구코드',
        'numOfRows': '검색건수',
        'pageNo': '페이지 번호',
    }



