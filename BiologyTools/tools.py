import colorama
import pymysql
from .define import Record


class SQL:
    def __init__(self, host='192.168.1.4', user='cleverboss', password='clever3366', database='biology', port=3307):
        self.table = None
        self.connect = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        self.cursor = self.connect.cursor()
        self.info = None
        self.keys = 'value,light,number,part,wrong'

    def tables(self, table: str):
        self.table = table

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connect.close()

    def __add__(self, other: list):
        self.cursor.execute(
            "INSERT INTO "
            + self.table
            + " (" + self.keys + ") VALUES ('" +
            str(other[0]) + "','" + str(other[1]) + "','" + str(other[2]) + "','" + str(other[3]) + "','" + str(other[4])
            + "');"
        )

    def __mul__(self, other: dict):
        if type(other) is not dict:
            raise TypeError(f'输入一个字典,不是{type(other)}')
        for k, v in other.items():
            self.cursor.execute(
                f"INSERT INTO {self.table} (value,light) VALUES ('{v}','{self.info}');"
            )

    @classmethod
    def increase(cls, table):
        def decorator(func):
            def wrapper(*args, **kwargs):
                with cls() as db:
                    db.tables(table)
                    # 调用原始函数
                    for i in func(*args, **kwargs):
                        print(i)

            return wrapper

        return decorator


class Output:
    @staticmethod
    def records(records: Record):
        """
        将结果输出为一个好看的格式
        :param records:
        :return:
        """
        print(
            f'{colorama.Style.BRIGHT}{colorama.Fore.WHITE}{colorama.Back.BLACK}{records[0][1]}-'
            f'{records[0][2]}{colorama.Fore.RESET}{colorama.Back.RESET}'
        )
        print(f"{colorama.Fore.GREEN} 分段 {colorama.Fore.BLUE}  速率  {colorama.Fore.RED} 错误 {colorama.Fore.RESET}")
        for i in records:
            print(
                f'{colorama.Fore.GREEN}{i[3]:-3d}  {colorama.Fore.BLUE}{i[0]:.4f} '
                f' {colorama.Fore.RED}{i[4]}{colorama.Fore.RESET}'
            )

