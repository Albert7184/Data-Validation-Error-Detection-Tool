import numpy as np

def calculate_z_score_anomalies(numbers):
    if not numbers:
        return 0, [], "Dữ liệu trống"
    
    arr = np.array(numbers)
    mean = np.mean(arr)
    std = np.std(arr)
    count = len(numbers)
    
    anomalies = []
    ai_score = 100
    
    if count >= 3 and std > 0:
        z_scores = np.abs((arr - mean) / std)
        anomalies = arr[z_scores > 2.0].tolist()
        ai_score = int(((count - len(anomalies)) / count) * 100)
        
    return ai_score, anomalies, mean, std