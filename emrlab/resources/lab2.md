<center><h1> EMR Hands-On Lab 2 - Adhoc on EMR </h1></center>

<hr>

이번 실습은 Adhoc 분석을 실습합니다.

분석에 적합한 데이터를 이용하여 Adhoc 분석을 실습합니다. ***1) SQL 형태의 Hive를 이용한 분석***과 ***2) PySpark를 이용하여 클러스터 프로그래밍***을 경험할 수 있습니다. 

또한 애플리케이션을 모니터링하고 용량을 자동으로 조정하여 최저 가격으로 안정적이고 예측 가능한 성능을 유지할 수 있도록 Auto Scaling을 이용하는 방법을 소개합니다.

## Table of Contents

1. [사전 준비](#사전 준비)
2. [클러스터 생성](#클러스터 생성)
3. [Analysis](#Analysis)
4. [Auto-Scaling](#EMR Core node Auto Scaling)

<br>

# 사전 준비<a name="사전 준비"></a>

<hr>

## S3 버킷 생성

1. Lab 1에서 만들었던 EC2 instance에 연결합니다. 인스턴스는 `EMRLAB-KIN` Name 태그를 가지고 있습니다.

    ```ssh -i key_file.pem ec2-user@PUBLIC_DNS```

2. Lab 1에서 우리는 S3 버킷 권한을 부여했습니다. 이 권한이 있으므로 아래 명령어를 통해 버킷을 생성합니다. 버킷은 분석용 데이터를 저장할 버킷입니다. 
*id-* 부분은 알맞게 수정합니다.

    ```aws s3 mb s3://id-emr-lab-data-20200306```

<br>

## 데이터 다운로드

1. 실습에서 사용할 데이터를 다운로드합니다. 실습은 Kaggle의 [Brazilian E-Commerce Public Dataset by Olist]((https://www.kaggle.com/olistbr/brazilian-ecommerce))를 사용할 것입니다. 
아래 링크를 클릭하여 파일을 다운로드하세요.

    [Download](https://www.kaggle.com/olistbr/brazilian-ecommerce/download)

    데이터는 order와 customer, product등의 데이터가 잘 연결되어 있어서 이번 실습에서 사용하기 적합합니다.

2. 파일 다운로드가 완료되면 압축을 풀고 이전에 생성한 S3의 버킷에 업로드합니다.

    ```aws s3 cp brazilian-ecommerce/ s3://id-emr-lab-data-20200306/brazilian-ecommerce --recursive```

    실습에서 사용한 데이터가 준비되었습니다.

<br>

# 클러스터 생성<a name="클러스터 생성"></a>

<hr>

이번 단계에서는 Adhoc 분석용 클러스터를 생성합니다.

1. EMR 메인 페이지로 이동합니다. [link](https://ap-northeast-2.console.aws.amazon.com/elasticmapreduce/home?region=ap-northeast-2)
2. Clusters를 선택합니다.
3. Create cluster를 선택합니다.
4. 페이지 상단에 Go to advanced options를 클릭합니다.

	<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic1.png?raw=true" border="1px solid black" width="90%">

5. Release에 emr 최신 버전을 선택하고, Hive와 Spark를 사용할 것이므로, Hadoop, Hive와 Spark를 선택합니다. Next를 눌러 다음 단계로 넘어갑니다.

	<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic2.png?raw=true" border="1px solid black" width="90%">

6. 이번 실습에서는 Core 노드만 사용합니다. 나머진 그대로 두고, Core 노드에 인스턴스 수를 2로 두고, Task 노드를 X 표시를 눌러 삭제합니다. Core와 Task 노드의 차이는 이 링크를 눌러 확인하시기 바랍니다. [Understanding Master, Core, and Task Nodes](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-master-core-task-nodes.html). Next를 눌러 다음 단계로 넘어갑니다.

	<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic3.png?raw=true" border="1px solid black" width="90%">

7. 클러스터 이름을 `EMR-lab-adhoc-20200306` 으로 넣고 Logging과 Debugging 옵션을 켭니다. Termination protection은 선택 해제 후 Next 를 눌러 다음 단계로 넘어갑니다.

	<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic4.png?raw=true" border="1px solid black" width="90%">

8. EC2 key pair에 인스턴스에 접속할 key pair를 선택한 후 Create cluster를 선택하여 클러스터를 생성합니다.

	<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic5.png?raw=true" border="1px solid black" width="90%">

9. 7~8분 정도 후에 클러스터의 마스터와 Core 노드의 상태가 Running으로 변경될 때까지 기다립니다.

	<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic6.png?raw=true" border="1px solid black" width="90%">
	
실습에서 사용할 클러스터의 생성이 완료되었습니다.
	
<br>

# Analysis<a name="Analysis"></a>

<hr>

이번 단계에서는 실습을 통해 분석 과정을 경험해 봅니다. 가장 많이 사용되는 어플리케이션인 Hive와 Spark를 사용하여 분석 예시를 살펴보겠습니다.
Hive와 Spark는 아래 설명을 참고하십시오.

* [Apache Hive](https://hive.apache.org/)는 하둡에서 동작하는 데이터 웨어하우스(Data Warehouse) 인프라 구조로서 데이터 요약, 질의 및 분석 기능을 제공합니다. 아파치 하이브는 아파치 HDFS이나 아파치 HBase와 같은 데이터 저장 시스템에 저장되어 있는 대용량 데이터 집합들을 분석할 수 있습니다. HiveQL 이라고 불리는 SQL같은 언어를 제공하며 맵리듀스의 모든 기능을 지원합니다.

* [Apache Spark](https://spark.apache.org/)는 오픈 소스 클러스터 컴퓨팅 프레임워크로, 암시적 데이터 병렬성과 장애 허용과 더불어 완전한 클러스터를 프로그래밍하기 위한 인터페이스를 제공합니다.

Hive와 Spark를 실행하기 위해 Master Node에 연결합니다. 
EC2 인스턴스에 연결하는 것과 동일합니다. EMR_PUBLIC_DNS는 EMR 클러스터의 **Master public DNS**입니다. user name에 **hadoop**을 작성하는 것에 유의하십시오.

```ssh -i key_file.pem hadoop@EMR_PUBLIC_DNS```

정상적으로 연결되면 아래와 같은 화면이 보입니다.

<img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic7.png?raw=true" border="1px solid black" width="60%">

<br>

## Hive

<hr>

Hive를 이용하여 SQL과 같은 분석 쿼리를 실습할 수 있습니다.

1. EMR 마스터 노드에 연결된 상태에서 `hive`를 입력하여 Hive를 실행합니다.

    <img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic8.png?raw=true" border="1px solid black" width="90%">

2. S3에 저장되어 있는 데이터를 Hive로 가지고 옵니다. 테이블을 생성합니다.

```

```

3. 각 User별 구매 금액 Sum을 구하고 저장하는 쿼리를 작성합니다.

```

```

4. 각 Product category별 판매 횟수의 Avg를 구하고 저장하는 쿼리를 작성합니다.

```

```


<br>

## PySpark

<hr>

이번에는 PySpark를 이용하여 파이썬 랭귀지로 클러스터 프로그래밍을 연습해 보겠습니다.

1. EMR 마스터 노드에 연결된 상태에서 `pyspark`를 입력하여 PySpark를 실행합니다.

    <img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic9.png?raw=true" border="1px solid black" width="90%">

2. Kinesis에서 저장한 log의 의미있는 부분만 추출하여 저장합니다.

```

```

3. Hive에서 추출한 두 테이블을 가져와서 평균 User가 누군지 확인합니다.

```

```

<br>

# EMR Core node Auto Scaling<a name="EMR Core node Auto Scaling"></a>

<hr>

이번 단계에서는 분석 작업이 많아졌을 때 클러스터를 자동으로 확장하는 방법에 대해 배워봅니다.

1. EMR 메인 페이지로 이동합니다. [link](https://ap-northeast-2.console.aws.amazon.com/elasticmapreduce/home?region=ap-northeast-2)
2. Clusters를 선택합니다. 
3. 실습에서 생성했던 `EMR-lab-adhoc-20200306` 클러스터를 선택합니다.
4. Hardware 탭을 선택합니다.
5. Auto Scaling 탭의 Not enabled 옆의 수정 아이콘을 클릭합니다.

    <img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic18.png?raw=true" border="1px solid black" width="90%">


6. 아래 스크린샷을 참고하여 값을 채워 넣습니다. 모든 값이 정확하게 입력되었는지 확인한 후 Modify를 클릭하여 적용합니다. 

    <img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic19.png?raw=true" border="1px solid black" width="90%">

    * Scale out
        * YARNMemoryAvailablePercentage가 20보다 작은 현상이 5분 간격으로 3번 관찰되었을 때 2개의 인스턴스를 추가합니다.
        * ContainerPendingRatio가 0.75보다 큰 현상이 5분 간격으로 3번 관찰되었을 때 2개의 인스턴스를 추가합니다.

    * Scale in
        * YARNMemoryAvailablePercentage가 85보다 큰 현상이 5분 간격으로 3번 관찰되었을 때 1개의 인스턴스를 종료합니다.

    * YARNMemoryAvailablePercentage와 ContainerPendingRatio는 아래 설명을 참조하십시오.
        * YarnMemoryAvailablePercentage: YARN에서 사용할 수 있는 잔여 메모리 비율입니다.
        * ContainerPendingRatio: 대기 중인 컨테이너/할당된 컨테이너 입니다. 이 측정치를 사용하여 다양한 로드에 대한 할당 컨테이너 동작을 기반으로 클러스터를 조정할 수 있으며, 이는 성능 튜닝에 유용합니다.

    Auto Scaling 상태가 Pending에서 Attached가 될 때까지 기다립니다.

    <img src="https://github.com/elbanic/emrlabs-web/blob/master/emrlab/resources/images/lab2_pic20.png?raw=true" border="1px solid black" width="30%">


7. 앞서 실험한 분석 예시를 여러 개의 쉘을 띄우고 동시에 실행해 봅니다. 여러 개의 분석 작업이 동시에 실행되면 YARN에서 사용할 수 있는 잔여 메모리의 비율이 감소하고, 대기 중인 컨테이너가 증가하여, 오토 스케일링 기능이 동작하는 것을 확인할 수 있습니다.

<center><a href="/emrlab/lab3"><font size="5">Next Lab</font></a></center>