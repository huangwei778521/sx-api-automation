import pytest
from utils.mysql import Mysql


@pytest.fixture(scope='session')
def root_group_id():
    sql = "SELECT group_id  from info_device_group idg where remark ='root'"
    with Mysql() as mysql:
        query_result = mysql.select_one(sql)
    return query_result[0]


@pytest.fixture(scope='session')
def group_id():
    sql = "SELECT group_id  from info_device_group where name ='autotest';"
    with Mysql() as mysql:
        query_result = mysql.select_one(sql)
    return query_result[0]


def delete_device():
    pass
