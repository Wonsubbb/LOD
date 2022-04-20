from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
#from .forms import TrafficInfoForm
from .serializers import TrafficInfoSerializer
from .get_secrets import get_ServiceKey
from .indexList import GUGUN_CHOICES
from collections import defaultdict
import requests
import json
# Create your views here.

def home(request):
    return HttpResponse("프론트앤드 화면 만들기")

class homeListAPIView(APIView):
    def post(self, request):
        serializer = TrafficInfoSerializer(data=request.data)
        if serializer.is_valid():
            url = 'http://apis.data.go.kr/B552061/AccidentDeath/getRestTrafficAccidentDeath'
            servicekey = get_ServiceKey()
            sido = serializer.data.get('siDo')

            acc_ty_cd = defaultdict(int)
            aslt_vtr_cd = defaultdict(int)
            info=dict(totalAccient=0, acc_year=serializer.data.get('searchYear'), sido=sido, casualties=0, dth_dnv_cnt=0, se_injured_cnt=0, sl_injured_cnt=0, wnd_dnv_cnt=0,
                      acc_type=dict(carVScar=0,carVSperson=0,carOnly=0,others=0),acc_ty_cd=acc_ty_cd, aslt_vtr_cd=aslt_vtr_cd, dght_cd=dict(daytime=0, night=0))


            for gugun in GUGUN_CHOICES[int(sido)]: #구/군에 따른 반목 ex) 서울시 : 강남구, 성북구 ....
                params ={'ServiceKey' : servicekey, 'searchYear' : serializer.data.get('searchYear'), 'siDo' : sido, 'guGun' : gugun, 'type' : 'json', 'numOfRows' : '9999', 'pageNo' : '1' }
                r = requests.get(url, params=params) #openAPI에 요청하기
                if r.status_code == requests.codes.ok: #코드 상태 확인
                    #요약보기 : 사고건수, 사고년도,발생위치시도코드(시군구 모두보기),  사상자수, 사망자수, 사고유형대분류
                    #상세보기 : 사고건수, 사고년도,발생위치시도코드(시군구 모두보기), 사상자수, 사망자수, 중상자수, 경상자수, 부상신고자수, 사고유형 대분류, 사고유형, 가해자 법규위반코드, 주야구분코드
                    body = r.json()['items']['item']
                    gutotalcnt = r.json()['totalCount']
                    info['totalAccient'] += gutotalcnt

                    if serializer.data.get('select') == 1:  #요약페이지 일때 info 칼럼 삭제
                        [info.pop(key, None) for key in ['se_injured_cnt', 'sl_injured_cnt', 'wnd_dnv_cnt', 'acc_ty_cd', 'aslt_vtr_cd', 'dght_cd']]

                    for cnt in range(gutotalcnt):
                        info['dth_dnv_cnt'] += body[cnt]['dth_dnv_cnt']
                        info['casualties'] += body[cnt]['injpsn_cnt']

                        #사고유형 대분류 처리
                        if body[cnt]['acc_ty_lclas_cd'] == '01' : info['acc_type']['carVScar'] += 1         #차대차 사고
                        elif body[cnt]['acc_ty_lclas_cd'] == '02' : info['acc_type']['carVSperson'] += 1    #차대사람 사고
                        elif body[cnt]['acc_ty_lclas_cd'] == '03' : info['acc_type']['carOnly'] += 1        #차량단독 사고
                        else: info['acc_type']['others'] += 1

                        if serializer.data.get('select') == 2:   #상세 페이지
                            info['se_injured_cnt'] += body[cnt]['se_dnv_cnt']   #중상자수
                            info['sl_injured_cnt'] += body[cnt]['sl_dnv_cnt']   #경상자수
                            info['wnd_dnv_cnt'] += body[cnt]['wnd_dnv_cnt']     #부상자수
                            acc_ty_cd[body[cnt]['acc_ty_cd']] += 1              #사고유형
                            aslt_vtr_cd[body[cnt]['aslt_vtr_cd']] += 1          #가해자 법규위반코드

                            #주야간 구분코드
                            if body[cnt]['dght_cd'] == '1':
                                info['dght_cd']['daytime'] += 1
                            else:
                                info['dght_cd']['night'] += 1

                else : return Response(r.raise_for_status())
            #response = Response(json.dumps(info))
            return Response(info)
        else:
            messages.error(request, '입력값을 다시 확인해 주세요')
            return redirect('traffic:home')