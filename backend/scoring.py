import pandas as pd

def score_all(df):
    
    score = []
    
    # mean and std
    steps_mean = df.Steps.mean()
    steps_std = df.Steps.std()
    
    heart_rate_mean = df.HR.mean()
    heart_rate_std = df.HR.std()
    
    sleep_mean = df.Sleep.mean()
    sleep_std = df.Sleep.std()
    
    for index, row in df.iterrows():
        
        count = 0
        
        # steps
        if row.Steps < (steps_mean - steps_std):
            count += 1
        elif row.Steps > (steps_mean + steps_std):
            count += 3
        else:
            count += 2
        
        # heart rate
        if row.HR < 40:
            count += 1
        elif row.HR < heart_rate_mean:
            count += 3
        elif row.HR >= heart_rate_mean and row.HR <= (heart_rate_mean + 3*heart_rate_std): # three std to be safe
            count += 2
        else:
            count += 1
        
        # sleep
        if row.Sleep < (sleep_mean - sleep_std):
            count += 1
        elif row.Sleep > (sleep_mean + sleep_std):
            count += 3
        else:
            count += 2
        
        # bp upper
        if row.Bp_upper < 100:
            count += 1
        elif row.Bp_upper < 135:
            count += 3
        elif row.Bp_upper >= 135 and row.Bp_upper <= 160:
            count += 2
        elif row.Bp_upper > 160:
            count += 1
        
        # bp lower
        if row.Bp_lower < 60:
            count += 1
        elif row.Bp_lower < 85:
            count += 3
        elif row.Bp_lower >= 85 and row.Bp_lower <= 100:
            count += 2
        else:
            count += 1
            
        if count < 10:
            score.append(1)
        elif count > 12: 
            score.append(3)
        else: 
            score.append(2)
            
    return score


def score_steps(steps):
    return

def score_heartrate():
    return

def score_sleep():
    return

def score_bp_upper():
    return

def score_bp_lower():
    return