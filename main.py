import sys
import logging
import time

import pandas as pd


def get_result(in_data_a='in_data_a.csv', in_data_b='in_data_p.csv', out='out.csv'):
    """
    Для решения задачи
    Получение информации о стоимости одной установки для каждой рекламной кампании, разбитую по названиям рекламируемых
    приложений, по операционной системе и по дням
    :param in_data_a: путь к файлу с информацией об установках
    :param in_data_b: путь к файлу с информацией о тратах
    :param out: путь к выходному файлу
    """
    df_result = pd.DataFrame(dict(app=[], date=[], campaign=[], os=[], installs=[], spend=[], cpi=[]))
    df_in_data_a = pd.read_csv(in_data_a)
    df_in_data_b = pd.read_csv(in_data_b)
    length = int(df_in_data_a['id'].count())      # Для отображения прогресса

    start = time.time()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
    logging.info('Старт программы')

    for i in df_in_data_a.index:
        if i % 1000 == 0:
            logging.info(f'обрабатано {round(i / length * 100)}% информации')
        try:
            app = df_in_data_a.loc[i, 'app']
            date = df_in_data_a.loc[i, 'Date']
            campaign = df_in_data_a.loc[i, 'Campaign']
            os = df_in_data_a.loc[i, 'os']
            installs = int(df_in_data_a.loc[i, 'Installs'])
            spend = df_in_data_b[(df_in_data_b['ad_id'] == df_in_data_a.loc[i, 'ad_id']) &
                                 (df_in_data_b['date'] == date)]['spend']
            if spend.empty:
                spend = 0
            else:
                spend = round(float(spend), 2)
            try:
                cpi = round(float(spend) / installs, 2)
            except ZeroDivisionError:
                cpi = 0
            df_result = df_result.append(dict(app=app, date=date, campaign=campaign, os=os, installs=installs,
                                              spend=spend, cpi=cpi), ignore_index=True)
        except Exception as e:
            logging.error(f'Непредвиденная ошибка {e}')
            raise

    df_result = df_result.groupby(['app', 'date', 'campaign', 'os']).sum()
    convert_dict = {'installs': int,
                    'spend': float,
                    'cpi': float,
                    }
    df_result = df_result.astype(convert_dict)
    df_result.to_csv(out, float_format='%.1f')
    logging.info(f'Программа окончена за {round(time.time() - start)} секунд(ы), обработано строк - {length}')

########################################################################################################################
class Work:
    """
    Реализация класса Не только сохраняет выполнене задачи, но и обеспечивает взаимод с Tkinter
    """
    def __init__(self, in_data_a='in_data_a.csv', in_data_b='in_data_p.csv', out='out.csv'):
        self.out = out
        self.df_in_data_a = pd.read_csv(in_data_a)
        self.df_in_data_b = pd.read_csv(in_data_b)
        self.length = int(self.df_in_data_a['id'].count())


    def first(self, progress=None):
        start = time.time()
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
        logging.info('Старт программы')
        df_result = pd.DataFrame(dict(app=[], date=[], campaign=[], os=[], installs=[], spend=[], cpi=[]))

        for i in self.df_in_data_a.index:
            if i % 1000 == 0:
                logging.info(f'обрабатано {round(i /  self.length * 100)}% информации')
                status = round(i / self.length * 100)
                if progress is not None and status != 0:
                    progress.set(status)
            try:
                app = self.df_in_data_a.loc[i, 'app']
                date = self.df_in_data_a.loc[i, 'Date']
                campaign = self.df_in_data_a.loc[i, 'Campaign']
                os = self.df_in_data_a.loc[i, 'os']
                installs = int(self.df_in_data_a.loc[i, 'Installs'])
                spend = self.df_in_data_b[(self.df_in_data_b['ad_id'] == self.df_in_data_a.loc[i, 'ad_id']) &
                                     (self.df_in_data_b['date'] == date)]['spend']
                if spend.empty:
                    spend = 0
                else:
                    spend = round(float(spend), 2)
                try:
                    cpi = round(float(spend) / installs, 2)
                except ZeroDivisionError:
                    cpi = 0
                df_result = df_result.append(dict(app=app, date=date, campaign=campaign, os=os, installs=installs,
                                                  spend=spend, cpi=cpi), ignore_index=True)
            except Exception as e:
                logging.error(f'Непредвиденная ошибка {e}')
                raise

        df_result = df_result.groupby(['app', 'date', 'campaign', 'os']).sum()
        convert_dict = {'installs': int,
                        'spend': float,
                        'cpi': float,
                        }
        df_result = df_result.astype(convert_dict)
        df_result.to_csv(self.out, float_format='%.1f')
        logging.info(f'Программа окончена за {round(time.time() - start)} секунд(ы), обработано строк - {self.length}')
        progress.set(0)

if __name__ == '__main__':
    get_result()
    # a = Work()
    # a.first()

