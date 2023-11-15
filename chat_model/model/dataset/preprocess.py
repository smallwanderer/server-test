import pandas as pd

data = [
    [70, 85, 11, 73],
    [71, 89, 18, 82],
    [50, 80, 20, 72],
    [99, 20, 10, 57],
    [50, 10, 10, 34],
    [20, 99, 10, 58],
    [40, 50, 20, 56]
]

# 배열을 DataFrame으로 변환
df = pd.DataFrame(data, columns=['x1', 'x2', 'x3', 'y'])

# DataFrame을 CSV 파일로 저장
df.to_csv('dataset.csv', index=False)