import logging
import time
from pymongo import MongoClient
# from config.others import test


class CallbackMsg:
    def __init__(self, db):
        self.db = db

    def get_callback_by_region_id(self, region_id, msg_count=None):
        if msg_count:
            n_t = time.time()
            while True:
                time.sleep(5)
                callback_msg_list = []
                object_info_list = self.db.sx_callback_data.find(
                    {"batch_objects.camera_info.internal_id.region_id": region_id}).limit(msg_count)
                for object_info in object_info_list:
                    callback_data_list = object_info.get("batch_objects")
                    for callback_data in callback_data_list:
                        if callback_data["camera_info"]["internal_id"]["region_id"] == region_id:
                            callback_msg_list.append(callback_data)

                if len(callback_msg_list) >= msg_count:
                    return callback_msg_list

                if time.time() - n_t > 5 * 60:
                    logging.error("未获取到需求数量的回调消息")
                    return callback_msg_list

        else:
            n_t = time.time()
            while True:
                callback_msg_list = []
                count = self.db.sx_callback_data.find(
                    {"batch_objects.camera_info.internal_id.region_id": region_id}).count()
                time.sleep(5)
                count_next = self.db.sx_callback_data.find(
                    {"batch_objects.camera_info.internal_id.region_id": region_id}).count()
                if count == count_next:
                    object_info_list = self.db.sx_callback_data.find(
                        {"batch_objects.camera_info.internal_gid.region_id": region_id})
                    break

                if time.time() - n_t > 5 * 60:
                    logging.error("解析一直未停止，回调消息未完全取出")

            for object_info in object_info_list:
                callback_data_list = object_info.get("batch_objects")
                for callback_data in callback_data_list:
                    if callback_data["camera_info"]["internal_id"]["region_id"] == region_id:
                        callback_msg_list.append(callback_data)

            return callback_msg_list

    def get_callback_by_camera_id(self, camera_id, msg_count=None):
        if msg_count:
            n_t = time.time()
            while True:
                time.sleep(3)
                callback_msg_list = []
                object_info_list = self.db.sx_callback_data.find(
                    {"batch_objects.camera_info.camera_id": camera_id}).limit(msg_count)
                for object_info in object_info_list:
                    callback_data_list = object_info.get("batch_objects")
                    for callback_data in callback_data_list:
                        if callback_data["camera_info"]["camera_id"] == camera_id:
                            callback_msg_list.append(callback_data)

                if len(callback_msg_list) >= msg_count:
                    return callback_msg_list

                if time.time() - n_t > 5 * 60:
                    logging.error("未获取到需求数量的回调消息")
                    return callback_msg_list

        else:
            n_t = time.time()
            while True:
                callback_msg_list = []
                count = self.db.sx_callback_data.find(
                    {"batch_objects.camera_info.camera_id": camera_id}).count()
                time.sleep(5)
                count_next = self.db.sx_callback_data.find(
                    {"batch_objects.camera_info.camera_id": camera_id}).count()
                if count == count_next:
                    object_info_list = self.db.sx_callback_data.find(
                        {"batch_objects.camera_info.camera_id": camera_id})
                    break

                if time.time() - n_t > 5 * 60:
                    logging.error(f"camera_id:{camera_id}解析一直未停止，回调消息未完全取出")

            for object_info in object_info_list:
                callback_data_list = object_info.get("batch_objects")
                for callback_data in callback_data_list:
                    if callback_data["camera_info"]["camera_id"] == camera_id:
                        callback_msg_list.append(callback_data)

            return callback_msg_list

    def delete_callback_msg(self):

        self.db.sx_callback_data.delete_many({})


# if __name__ == "__main__":
#     client = MongoClient(test.get("mongo_uri"))
#     db = client[test.get("db")]
#     CallbackMsg(db).get_callback_by_region_id(45)
