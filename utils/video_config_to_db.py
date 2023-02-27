from pymongo import MongoClient
import json
import xlrd
from config.server_info import mongo_uri,mongo_db_name


db_info = {
    "mongo_uri": mongo_uri,
    "db_name": mongo_db_name
}


def data_into_db(path):
    client = MongoClient(db_info.get("mongo_uri"))
    db = client[db_info.get("db")]
    videos_config = {}
    for sheet_index in range(0, 1):
        with xlrd.open_workbook(path) as data:
            table = data.sheet_by_index(sheet_index)
        rows = table.nrows
        cols = table.ncols
        titles = table.row_values(0)
        title_map = {}
        for index, title in enumerate(titles):
            title_map.update({index: title})
        for r in range(1, rows):
            video_name = None
            row_value = table.row_values(r)
            for c in range(0, cols):
                try:
                    videos_config.update({title_map[c]: json.loads(row_value[c])})
                except Exception as e:
                    print(e)
                    if c == 0:
                        video_name = row_value[c]
                    videos_config.update({title_map[c]: row_value[c]})
            try:
                col_list = db.list_collection_names()
                if "sx_videos_config" in col_list:
                    if db.sx_videos_config.find({"video_name": video_name}):
                        db.sx_videos_config.update_one({"video_name": video_name}, {"$set": videos_config},
                                                       upsert=True)
                    else:
                        db.sx_videos_config.insert_one(videos_config)
            except Exception as e:
                print(e)
                client.close()
                raise Exception("fail to insert truth into db")
            finally:
                videos_config = {}
    client.close()
    pass


if __name__ == '__main__':
    data_into_db()
