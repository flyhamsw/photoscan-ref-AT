# PhotoScan 기준영상 AT

## Step 1. 기준영상 준비 (DJI_0001.JPG~DJI_0042.JPG)
기준영상의 조정된 EO를 다음과 같은 형식으로 저장 (reference_image_adjusted_EOs.txt)

```
[파일명1],[정밀도],[X],[Y],[Z]
[파일명2],[정밀도],[X],[Y],[Z]
[파일명3],[정밀도],[X],[Y],[Z]
[파일명4],[정밀도],[X],[Y],[Z]
```

## Step 2. 설정
run.py에서 쿼리영상(DJI_0411.JPG)의 초기 EO 입력 (x, y, z, 기준영상 검색 반경)
```
reference_image_AT('DJI_0411.JPG', 240773.156605, 543483.567496, 59.052039, 50)
```

## Step 3. 실행
포토스캔 파이썬 인터프리터로 run.py 실행
```
E:\python-workspace\photoscan-ref-AT>"C:\Program Files\Agisoft\PhotoScan Pro\photoscan.exe" -r run.py
```
