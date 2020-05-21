# ANCHOVYMART

## 1. ANCHOVYMART란?
	anchovy란 '멸치'를 의미합니다. 제가 운동식품, 용품을 구매하는데 자주사용하는 E-commerce인
    'MONSTERMART'에서 영감을 얻었습니다.
    
    ANCHOVYMART는 Iamport사의 API을 이용한 E-commerce입니다.

## 2. 프로젝트 제작 목적
	 API에 대한 정확한 이해, 사용해보는 것과 아마존 EC2를 이용한 배포경험 쌓는것을
     제작목적으로 두었습니다.

## 3. 주요 기능
#### 3.1 Accounts
* 기본적인 Login, Logout, Register
* '네이버 아이디로 로그인'
#### 3.2 Shop
* 관리자는 판매상품 등록(Admin site), 구매자는 판매물품 확인.
* 카테고리별 상품 확인
* 상품 이름을 통한 검색
* Slug를 이용한 인간친화적인 URL
* Paginator 
* 재고 0개 일시 자동 판매 중단
#### 3.3 Cart
* 장바구니
* 재고보다 초과한 물품 등록 제한 및 삭제
#### 3.4 Order
* 주문서, 영수증을 비교하는 검증
* Iamport API를 이용한 결제
* AJAX통신으로 사이트 전환 없이 결제정보 생성 및 통신
* Iamport API를 이용한 iamport transaction 확인
* 주문 완료시 주문한 수량만큼 재고 data 변경
* modal을 이용한 영수증 출력
* 주문 내역 CSV파일화


## 4. Skill Stack

#### 4.1 front-end
	Bootstrap, Bootswatch-cyborg template, django-template
#### 4.2 back-end
	python Django framework
#### 4.3 Dev-Ops
	AWS S3, EC2, Putty, FileZilla, Iamport API, Naver API, etc..
    
## 5. More Information
#### 5.1 Website 
>[**ANCHOVYMART**](http://ec2-13-125-139-153.ap-northeast-2.compute.amazonaws.com/)
#### 5.2 More information  
>[**ANCHOVYMART.pdf**](https://github.com/Donkey-1028/ANCHOVYMART/blob/master/ANCHOVYMART.pdf)
#### 5.3 Bootstrap template  
>[**Cyborg**](https://bootswatch.com/cyborg/)
<br>



<br>
