import pandas as pd
import time
import os
from pathlib import Path

def run_generator(arg1, arg2):
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        DATA_ROOT = os.path.join(BASE_DIR, 'data.pkl')
        data = pd.read_pickle(DATA_ROOT)
        steps = int(arg1)
        info_step = 10 #% шаг информирования - через 10% превышения
        mean_std_max = 0
        seconds = int(arg2)
        new_news = []
        messenge = ''
        strOut = [
            [],
            []
        ]
        while True:
            steps -= 1
            if steps < 0:
                break
            time.sleep(seconds)
            data_sample = data[data['rubric']=='Дом'].sample(n=1).reset_index(drop=True)
            new_news.append(data_sample['title'][0])
            mean_std = int(data_sample['month_mean'][0]+data_sample['month_std'][0])
            if len(new_news) > mean_std:
                procces = int((len(new_news)*100)/mean_std)-100
                if procces >= mean_std_max + info_step:
                    mean_std_max += info_step
                    messenge = 'Превышено стандартное отклонение на: ' + str(procces) + '%'
                    strOut[0].append(messenge)
            strOut[0].append(data_sample['title'][0])
            print(data_sample['title'][0])
        mean_std = int(data_sample['month_mean'][0]-data_sample['month_std'][0])
        if len(new_news) < mean_std:
            procces = 100 - int((len(new_news)*100)/mean_std)
            messenge = 'Количество сообщений ниже стандартного отклонения на: ' + str(procces) + '%'
            strOut[1].append(messenge)
            print(messenge)
        # print(strOut)
        return strOut
    except ValueError:
        return False