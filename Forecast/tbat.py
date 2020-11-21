if __name__ == '__main__':
    from multiprocessing import Process, freeze_support
    from tbats import TBATS, BATS
    import pandas as pd
    import matplotlib.pyplot as plt
    from pmdarima import auto_arima


    path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_processed/part-{}-of-00500.csv'
    df=pd.read_csv(path.format(str(2).zfill(5)))
    df.index=pd.to_datetime(df['time'])
    df['arrival_rq'].plot()
    plt.show()

    y = df['arrival_rq']
    estimator = TBATS(seasonal_periods=(14, 30.5))
    model = estimator.fit(y)
    y_forecast = model.forecast(steps=14)


    # arima_model = auto_arima(y, seasonal=True, m=1)
    # y_forecast = arima_model.predict(n_periods=1)

    # y_forecast.plot()
    plt.plot(y_forecast)
    plt.show()
