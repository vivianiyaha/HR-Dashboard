import random

def predict_attrition():
    return round(random.uniform(0,1),2)

def predict_performance():
    return round(random.uniform(0,1),2)

def predict_kpi():
    return round(random.uniform(0,1),2)

def decision():
    return random.choice(["Hire", "Reject"])
