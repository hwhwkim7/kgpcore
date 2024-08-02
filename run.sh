#!/bin/bash

# 사용 방법
# chmod +x run.sh
# ./run.sh aminer

# 외부에서 데이터셋 이름을 받습니다.
dataset_name=$1

# 최대 프로세스 수 설정
max_processes=35

# 실행할 알고리즘 배열 정의
algorithms=("ASAP" "naive")

# 파라미터 배열 정의
# ks=(20 25 30 35 40)
# gs=(20 25 30 35 40)
# ps=(0.0 0.2 0.4 0.6 0.8 1.0)
ks=(3 4 5 6 7)
gs=(3 4 5 6 7)
ps=(0.0 0.2 0.4 0.6 0.8 1.0)

# 모든 알고리즘에 대해 반복
for algorithm in "${algorithms[@]}"; do
    # 모든 k, g, p 조합에 대해 루프
    for k in "${ks[@]}"; do
        for g in "${gs[@]}"; do
            for p in "${ps[@]}"; do
                # 현재 실행 중인 프로세스 수가 최대치에 도달하면 대기
                while [ $(jobs -p | wc -l) -ge $max_processes ]; do
                    sleep 10 # 짧은 대기 시간 후 다시 체크
                done
                
                echo "Running: $algorithm on $dataset_name with k=$k, g=$g, p=$p"
                # 파이썬 스크립트 비동기 실행
                python main.py --k $k --g $g --p $p --algorithm $algorithm --network "./dataset/real/$dataset_name/network.hyp" --rec 0 &
            done
        done
    done
done

# 마지막 배치의 모든 작업이 완료될 때까지 대기
wait
