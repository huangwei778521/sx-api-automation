import json
import os
import xlrd
from pymongo import MongoClient

from config.others import test
from utils.tool import judge_files_download_completely


def parse_scenario_data_into_db():
    truth_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "truth_json")
    client = MongoClient(test.get("mongo_uri"))
    db = client[test.get("db")]
    scenario_data = {}
    path = "/Users/wangsuhua/Downloads/sxp_platform_ha_scenario.xlsx"
    truth_path = "/Users/wangsuhua/Downloads/sx1.3_truth/{}/{}"
    for sheet_index in range(0, 1):
        with xlrd.open_workbook(path) as data:
            table = data.sheet_by_index(sheet_index)
            sheet_name = table.name
        rows = table.nrows  # 行
        cols = table.ncols  # 列
        titles = table.row_values(0)
        title_map = {}
        for index, title in enumerate(titles):
            title_map.update({index: title})
        for r in range(1, rows):
            scenario_id = None
            row_value = table.row_values(r)
            for c in range(0, cols):
                try:
                    if title_map[c] == "truth_dir":
                        json_truth_host = "10.8.10.253"
                        dir_path = row_value[c]
                        cmd = f"sshpass -p Goodsense scp root@{json_truth_host}:{dir_path} {truth_json_path}"
                        os.popen(cmd)
                        if judge_files_download_completely(truth_json_path, 1):
                            file = os.listdir(truth_json_path)[0]
                            file_path = os.path.join(truth_json_path, file)
                        else:
                            raise Exception("未下载完成")
                        with open(file_path, "r") as f:
                            truth = f.read()
                            scenario_data.update({title_map[c]: json.loads(truth)})
                        os.popen(f"rm -r {file_path}")
                    else:
                        if title_map[c] == "truth" and "txt" in row_value[c]:
                            truth_dir = truth_path.format(sheet_name, json.loads(row_value[c])["truth"])
                            with open(truth_dir, "r") as f:
                                truth_txt = json.loads(f.read())
                                truth = json.loads(row_value[c])
                                truth["truth"] = truth_txt
                                scenario_data.update(
                                    {title_map[c]: truth})
                        else:
                            scenario_data.update({title_map[c]: json.loads(row_value[c])})
                except Exception as e:
                    print(e)
                    if title_map[c] == "scenario_id":
                        scenario_id = row_value[c]

                    elif title_map[c] == "truth":
                        truth_dir = truth_path.format(sheet_name, row_value[c])
                        with open(truth_dir, "r") as f:
                            truth = json.loads(f.read())
                        scenario_data.update({title_map[c]: truth})

                    elif title_map[c] == "image_num":
                        scenario_data.update({title_map[c]: int(row_value[c])})
                    else:
                        scenario_data.update({title_map[c]: row_value[c]})
            try:
                col_list = db.list_collection_names()
                if "sx_scenario_data" in col_list:
                    if db.sx_scenario_data.find({"scenario_id": scenario_id}):
                        db.sx_scenario_data.update_one({"scenario_id": scenario_id}, {"$set": scenario_data},
                                                       upsert=True)
                    else:
                        db.sx_scenario_data.insert_one(scenario_data)
                else:
                    db.sx_scenario_data.insert_one(scenario_data)
            except Exception as e:
                print(e)
                client.close()
                raise Exception("fail to insert truth into db")
            finally:
                scenario_data = {}
    client.close()


if __name__ == '__main__':
    parse_scenario_data_into_db()
