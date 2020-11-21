import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_cpu/part-{}-of-00500.csv'
ROUND = 120
CUT = ROUND - 1


class Sarima:

    def __init__(self, file):
        # file là mảng index dữ liệu lấy để dự đoán
        # mỗi file chứa khoản thời gian dự đoán bẳng nhau liên tiếp
        # VD: part-00000-of-00500.csv chứa dữ liệu 8-10h, part-00001-of-00500.csv chứa dữ liệu 10h-12h
        df = pd.read_csv(path.format(str(file[0]).zfill(5)))
        for i in range(1, len(file)):
            df2 = pd.read_csv(path.format(str(i).zfill(5)))
            df = pd.concat([df, df2])
        # print(df)
        print("forecast arrival rate ...")
        df.index = pd.to_datetime(df['time'])
        # SARIMAX https://www.statsmodels.org/dev/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html
        # forecast arrival request với mô hình sarima (2, 0, 2) (0, 1, 11, 12)
        model = sm.tsa.statespace.SARIMAX(endog=df['arrival_rate'], order=(2, 0, 2), seasonal_order=(0, 1, 11, 12),
                                          trend='c',
                                          enforce_invertibility=False)
        # lưu kết quả dự đoán arrival request vào biến forecast
        self.forecast = model.fit()
        print("forecast done")
        print("estimate cpu")
        # forecast trung bình cpu sử dụng với mô hình sarima (1, 0, 2) (0, 1, 2, 12)
        model = sm.tsa.statespace.SARIMAX(endog=df['cpu'], order=(1, 0, 2), seasonal_order=(0, 1, 2, 12),
                                          trend='c',
                                          enforce_invertibility=False)
        # lưu kết quả dự đoán cpu vào biến estimate
        self.estimate = model.fit()
        print("estimate done")

    # lấy kết quả dự đoán arrival request vào thời điểm time
    def get_forecast(self, time):
        forecast = self.forecast.get_forecast(steps=time)
        f_ci = forecast.conf_int()
        return forecast.predicted_mean[time]

    def get_estimate(self, time):
        estimate = self.estimate.get_forecast(steps=time)
        e_ci = estimate.conf_int()
        return estimate.predicted_mean[time]
