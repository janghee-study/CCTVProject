# CCTVProject
### 집안에 웹캠으로 CCTV (CCTV as a webcam in the house)

<img src="/images/CCTV.gif" width="50%">

### :large_orange_diamond: 작품선정 배경
----------------------------------------------------------

:point_right: 입안에 문열고 다닐 수 있도록 집 내부의 보안강화

### :large_orange_diamond: 작품 목표
----------------------------------------------------------
:point_right: 외부인으로부터의 보안강화

:point_right: 외부인은 얼굴을 DB에 저장해서 열람가능

:point_right: 본인얼굴은 딥러닝을 이용하여 제외

### :large_orange_diamond: 기능
----------------------------------------------------------
#### :heavy_check_mark: python, MySql, Jupiter Notobook
&nbsp;&nbsp;&nbsp; 영상을 통한 얼굴분류, GUI 및 Database 연동
#### :heavy_check_mark: WebCam
&nbsp;&nbsp;&nbsp; WebCam에 영상 전송, OpenCV 라이브러리 활용
#### :heavy_check_mark: tensorflow, keras
&nbsp;&nbsp;&nbsp; 비전학습

### :large_orange_diamond: 추가 수행과정
----------------------------------------------------------
#### :heavy_check_mark: 추가 수행일정
&nbsp;&nbsp;&nbsp; @얼굴인식,Pymysql 추가!

### :large_orange_diamond: 시행착오
----------------------------------------------------------
#### :heavy_check_mark: 시행착오 부분

<img src="/images/시행착오.PNG" width="60%">

#### :heavy_check_mark: 해결방안
----------------------------------------------------------
&nbsp;&nbsp;&nbsp; 표본부족으로 인한 과적합오류 --> (해결방안) --> 카테고리를 줄이며 카테고리마다의 표본 갯수 추가

&nbsp;&nbsp;&nbsp; 큰 해상도로 인한 동작시간증가 --> (해결방안) --> OpenCV를 통한 이미지 전처리

#### :heavy_check_mark: 시연영상
----------------------------------------------------------
<img src="/images/시연영상.gif" width="110%">

