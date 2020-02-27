# EMR Hands-On Lab 2 - Adhoc on EMR

이번 실습에서는


 * 여기서 각 코드를 조금 살펴보겠습니다.
 * SQL은 대부분 알고 계실 겁니다. HiveQL은 Hadoop에 있는 파일들을 쿼리하기 위한 SQL이라고 생각하시면 됩니다. 
 * Spark는 Python으로 코딩했습니다. Python을 잘 모르시는 분은 대략 이렇게 Spark를 사용하는구나 참고만 하시고 코드 복붙하시면 됩니다. 
 * SQL은 아무래도 데이터의 디테일한 처리가 어렵습니다. 로그 파싱 같은 경우가 이에 해당합니다. 데이터를 디테일하게 처리하기 위해 Spark를 쓴다고 생각하시면 됩니다.
 
<hr>

## Hive에서 할 것
1. 각 User별 구매 금액 Sum을 구하고 저장합니다.
2. 각 Product category별 판매 횟수의 Avg를 구하고 저장합니다.

<hr>

## Spark에서 할 것
1. Kinesis에서 저장한 log의 의미있는 부분만 추출하여 저장합니다.
2. Hive에서 추출한 두 테이블을 가져와서 평균 User가 누군지 확인합니다.


<center><a href="/emrlab/lab3"><font size="6">Next Lab</font></a></center>