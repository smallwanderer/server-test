import numpy as np
import pandas as pd
import os
from tensorflow.keras.models import Sequential, load_model


print("Current Working Directory:", os.getcwd())
print("File Exists:", os.path.isfile('my_model.h5'))

# 테스트 입력
test_data = np.array([[20, 99, 10]])
model_path = "my_model.h5"

# 저장된 모델
loaded_model = load_model(model_path)

# 모델 적용
result = loaded_model.predict(test_data)

print('prediction: ',result)