import ftplib
import os
import subprocess
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

ftp_host = "ita.ee.lbl.gov"
file_place = 'input/wc_day{}_{}.gz'


def download_data(start_day, end_day):
    end_day = end_day + 1
    with ftplib.FTP(host=ftp_host) as ftp_client:
        ftp_client.login()
        for day in range(start_day, end_day):
            print("Downloading day {} ...".format(day))
            for part in range(1, 10):
                ftp_file = "traces/WorldCup/wc_day{}_{}.gz".format(day, part)
                file_stream = open(file_place.format(day, part), "wb")
                try:
                    ftp_client.retrbinary('RETR {}'.format(ftp_file),
                                          file_stream.write, 1024)
                except ftplib.error_perm as err:
                    # print(err)
                    os.remove(file_place.format(day, part))
                    print("     Day {} has {} part!".format(day, (part - 1)))
                    break
                finally:
                    file_stream.close()
        print("Download done!")
        ftp_client.close


def to_csv(start_day, end_day):
    print("Start transfer to data/*.csv")
    subprocess.call(["./create_data.sh", str(start_day), str(end_day)])
    print("Done!!!")


def draw(start_day, end_day, field, style='line'):
    path = './data/wc_day{}_{}.csv'
    end_day = end_day + 1
    print(end_day)
    cols = ['time', 'datetime', 'request', 'bytes']
    df = pd.DataFrame()

    for day in range(start_day, end_day):
        for part in range(1, 2):
            try:
                df2 = pd.read_csv(path.format(day, part), names=cols, header=None)
                df = pd.concat([df, df2])
            except FileNotFoundError:
                break
    # plot line
    if style == 'line':
        df.plot(x='datetime', y=field)
        plt.show()
    else:
        df.plot(x='datetime', y=field, style='.-')
        plt.show()


if __name__ == "__main__":
    # WC98 - day46-day78

    # download_data(1, 92)

    # to_csv(46, 72)

    draw(46, 72, field='bytes')
    # draw(1, 92, field='request')
