import copy
import json
import logging
import os
from itertools import groupby
from operator import itemgetter
import openpyxl
from utils.logger import basic_log


def format_data_from_sensebee():
    source_data_dir = "/Users/wangsuhua/Downloads/sx1.3_accuracy_truth"
    write_path = "/Users/wangsuhua/Downloads/sx1.3_accuracy_truth.xlsx"
    write_truth_dir = "/Users/wangsuhua/Downloads/sx1.3_truth"
    scenario_dirs = os.listdir(source_data_dir)
    write_workbook = openpyxl.Workbook()
    start_scenario_id_map = {"density": "AS_VPS0003011", "strand": "AS_VPS0005010", "intrusion": "AS_VPS0004011",
                             "social_distance": "AS_VPS0001008", "congregate_scatter": "AS_VPS0007000",
                             "retrograde": "AS_VPS0006012", "cross_line": "AS_VPS0002018"}
    for directory in scenario_dirs:
        if directory.startswith("."):
            continue
        scenario_dir = os.path.join(source_data_dir, directory)
        scenario_name = directory.split("image")[0][0:-7]
        scenario_id_number = int(start_scenario_id_map[scenario_name][6:])
        basic_log("platform", "sensebe_data.log")
        sub_dirs_of_scenario = os.listdir(scenario_dir)
        write_table = write_workbook.create_sheet(title=scenario_name)
        if scenario_name in ["density", "strand", "intrusion", "social_distance", "congregate_scatter"]:
            title = ["scenario_id", "scenario_desc", "video_name", "pixel", "labeled_person", "roi", "truth", ]
        elif scenario_name in ["retrograde"]:
            title = ["scenario_id", "scenario_desc", "video_name", "pixel", "labeled_person", "roi", "directions",
                     "truth"]
        elif scenario_name in ["cross_line"]:
            title = ["scenario_id", "scenario_desc", "video_name", "pixel", "labeled_person", "roi", "directions",
                     "truth"]
        else:
            title = []
        write_table.append(title)
        for sub_dir in sub_dirs_of_scenario:
            if sub_dir.startswith("."):
                continue
            sub_dir_of_scenario = os.path.join(scenario_dir, sub_dir)
            sub_files_of_scenario = os.listdir(sub_dir_of_scenario)
            sub_files_of_scenario = sorted(sub_files_of_scenario, key=lambda e: int(e.split(".")[0]))
            directions = {}
            scenario_id_number = scenario_id_number + 1
            scenario_id = "AS_VPS000" + str(scenario_id_number)
            scenario_desc = scenario_name + " accuracy test"
            roi = {}
            pixel = {}
            truth = {}
            labeled_person = []
            queue_line = {}
            range_of_head_coordinates = {}
            for sub_file_of_scenario in sub_files_of_scenario:
                if sub_file_of_scenario.startswith("."):
                    continue
                frame_index = str(int(sub_file_of_scenario.split(".")[0]) - 1)
                sub_file = os.path.join(sub_dir_of_scenario, sub_file_of_scenario)
                with open(sub_file, "r") as f:
                    file_data = json.loads(f.read())
                    if not pixel:
                        pixel.update(width=file_data["width"], height=file_data["height"])

                    if file_data.get("step_1"):
                        if file_data["step_1"]["result"]:
                            step_1_results = file_data["step_1"]["result"]
                            if step_1_results[0]["attribute"] in ["roi框", "cross_line直线"]:
                                step_1_results.sort(key=itemgetter('valid'))
                                step_1_results_copy = [list(i[1]) for i in
                                                       groupby(step_1_results, lambda e: e["valid"])]
                                for index, step_1_result in enumerate(step_1_results_copy):
                                    roi_element = []
                                    if step_1_results[0]["attribute"] == "roi框":
                                        result = sorted(step_1_result, key=lambda x: x["order"])
                                        roi_element = [[re["x"], re["y"]] for re in result]
                                        if roi_element[1][0] < roi_element[0][0] or roi_element[2][0] < roi_element[3][
                                            0] or roi_element[2][1] < roi_element[1][1] or roi_element[3][1] < \
                                                roi_element[0][1]:
                                            logging.error(f"roi没有顺时针标注,{sub_dir},{sub_file_of_scenario}")

                                    if step_1_results[0]["attribute"] in ["cross_line直线", "排队线"]:
                                        elements_length = len(step_1_results)
                                        if elements_length >= 4:
                                            result = sorted(step_1_result, key=lambda e: e["order"])
                                            roi_element = [[re["x"], re["y"]] for re in result]
                                            if roi_element[0][1] < roi_element[1][1] or roi_element[3][1] < \
                                                    roi_element[2][1] or roi_element[2][0] > roi_element[1][0] or \
                                                    roi_element[3][0] > roi_element[0][0]:
                                                logging.error(
                                                    f"跨线三段直线未按照逆时针顺序标注且不成非闭合凸多边形,{sub_dir},{sub_file_of_scenario}")
                                        else:
                                            result = sorted(step_1_result, key=lambda e: e["order"])
                                            roi_element = [[re["x"], re["y"]] for re in result]

                                    if index == 0:
                                        if scenario_name == "queue_management":
                                            queue_line.update(roi_1=roi_element)
                                        else:
                                            roi.update(roi_1=roi_element)
                                    else:
                                        if scenario_name == "queue_management":
                                            queue_line.update(roi_2=roi_element)
                                        else:
                                            roi.update(roi_2=roi_element)

                            if step_1_results[0]["attribute"] in ["人头点", "人脚点"]:
                                step_1_results_copy = sorted(step_1_results, key=lambda x: x["order"])
                                global labeled_person_temp
                                labeled_person_temp = []
                                global count
                                count = 0
                                for result in step_1_results_copy:
                                    if count > 0:
                                        labeled_person_temp.append(result["y"])
                                        if labeled_person_temp[0] > labeled_person_temp[1]:
                                            logging.error(f"labeled_person人头与人脚不对应,{sub_dir},{sub_file_of_scenario}")
                                        labeled_person.append(labeled_person_temp)
                                        count = 0
                                        labeled_person_temp = []
                                    else:
                                        labeled_person_temp.append(result["y"])
                                        count = count + 1

                    if scenario_name in ["density"]:
                        if file_data["step_3"]["result"]:
                            if not file_data["step_3"]["result"][0].get("value"):
                                person_num = 0
                            else:
                                person_num = file_data["step_3"]["result"][0]["value"]["text"]
                            person_num_attribution = None
                            get_person_num(person_num, scenario_name, person_num_attribution, frame_index, truth)

                    if scenario_name in ["strand", "intrusion", "social_distance", "queue_management"]:
                        if file_data["step_3"]["result"]:
                            if not file_data["step_3"]["result"][0].get("value"):
                                if not file_data["step_3"]["result"][0].get("text"):
                                    person_num = 0
                                else:
                                    person_num = file_data["step_3"]["result"][0]["text"]
                            else:
                                person_num = file_data["step_3"]["result"][0]['value']["text"]
                            person_num_attribution = None
                            person_num = get_person_num(person_num, scenario_name, person_num_attribution, frame_index,
                                                        truth, sub_dir)

                    if scenario_name in ["congregate_scatter"]:
                        print(frame_index, sub_file)
                        if file_data["step_3"]["result"]:
                            value = file_data["step_3"]["result"][0]["value"]
                            number = value["人数"]
                            tag = value["图片标注"]

                            person_num = {"person_num": value["人数"], "tag": value["图片标注"]}

                            if file_data["step_5"]["result"] and file_data["step_7"]["result"]:
                                head_point_results = file_data["step_7"].get("result")
                                head_frame_results = file_data["step_5"].get("result")
                                get_head_point_and_frame(head_point_results, head_frame_results,
                                                         range_of_head_coordinates,
                                                         person_num, scenario_name, sub_dir,
                                                         sub_file_of_scenario,
                                                         frame_index, truth)

                            if file_data["step_9"]["result"] and file_data["step_11"]["result"]:
                                head_point_results = file_data["step_11"].get("result")
                                head_frame_results = file_data["step_9"].get("result")
                                get_head_point_and_frame(head_point_results, head_frame_results,
                                                         range_of_head_coordinates,
                                                         person_num, scenario_name, sub_dir,
                                                         sub_file_of_scenario,
                                                         frame_index, truth)

                    if scenario_name in ["retrograde"]:
                        if file_data["step_5"]["result"]:
                            if not file_data["step_5"]["result"][0].get("value"):
                                if not file_data["step_5"]["result"][0].get("text"):
                                    person_num = 0
                                else:
                                    person_num = file_data["step_5"]["result"][0]["text"]
                            else:
                                person_num = file_data["step_5"]["result"][0]["value"]["text"]
                            person_num_attribution = None
                            if sub_dir == "retrograde_image_10" and frame_index == "902":
                                print(1)
                            person_num = get_person_num(person_num, scenario_name, person_num_attribution,
                                                        frame_index, truth, sub_dir)
                    if scenario_name in ["cross_line"]:
                        if file_data["step_5"]["result"]:
                            if not file_data["step_5"]["result"][0]["value"].get("text"):
                                pass
                            else:
                                person_num = file_data["step_5"]["result"][0]["value"]["text"]
                                person_num = person_num.replace(" ", "")
                                person_num_list = person_num.split("\n")
                                if len(person_num_list) == 2:
                                    person_num_out_roi_1 = int(person_num_list[0][4:])
                                    person_num_in_roi_1 = int(person_num_list[-1][3:])
                                    truth.update({"roi_1": {
                                        frame_index: {"in": person_num_in_roi_1, "out": person_num_out_roi_1}}})
                                if len(person_num_list) == 4:
                                    person_num_in_roi_1 = person_num_list[0].split(":")[-1]
                                    person_num_out_roi_1 = person_num_list[1].split(":")[-1]
                                    person_num_in_roi_2 = person_num_list[2].split(":")[-1]
                                    person_num_out_roi_2 = person_num_list[3].split(":")[-1]
                                    truth.update({"roi_1": {
                                        frame_index: {"in": person_num_in_roi_1, "out": person_num_out_roi_1}},
                                        "roi_2": {
                                            frame_index: {"in": person_num_in_roi_2, "out": person_num_out_roi_2}}})

                    if scenario_name in ["retrograde", "cross_line"]:
                        if file_data["step_3"]["result"]:
                            text_attribute = file_data["step_3"]["result"][0]["textAttribute"]
                            text_attribute = text_attribute.replace(" ", "").replace("(", "").replace(")", "").replace(
                                ",", "").replace("，", "").replace("（", "").replace("）", "").replace(".", "").replace(
                                "-", "")
                            origin_coordinate_x = int(text_attribute[0])
                            origin_coordinate_y = int(text_attribute[1])
                            vector_coordinate_x = int(text_attribute[2])
                            vector_coordinate_y = int(text_attribute[3])

                            valid = file_data["step_3"]["result"][0]["valid"]

                            if valid is True:
                                directions = {"roi_1": [{"x": origin_coordinate_x, "y": origin_coordinate_y},
                                                        {"x": vector_coordinate_x, "y": vector_coordinate_y}]}
                            if valid is False:
                                directions = {"roi_2": [{"x": origin_coordinate_x, "y": origin_coordinate_y},
                                                        {"x": vector_coordinate_x, "y": vector_coordinate_y}]}

                    if scenario_name in ["strand", "intrusion", "social_distance", "queue_management"]:
                        if file_data["step_5"].get("result") and file_data["step_7"].get("result"):
                            head_point_results = file_data["step_7"].get("result")
                            head_frame_results = file_data["step_5"].get("result")
                            get_head_point_and_frame(head_point_results, head_frame_results, range_of_head_coordinates,
                                                     person_num,
                                                     scenario_name, sub_dir, sub_file_of_scenario, frame_index, truth)
                        else:
                            try:
                                if person_num > 0:
                                    logging.error(
                                        f"人头框人头点无值但有人数,{scenario_name},{sub_dir},{sub_file_of_scenario},{person_num}")
                            except Exception:
                                print(f"{sub_dir},{frame_index},{person_num}")

                    if scenario_name in ["intrusion", "social_distance", "strand"]:
                        if file_data["step_9"].get("result") and file_data["step_11"].get("result"):
                            head_point_results = file_data["step_11"].get("result")
                            head_frame_results = file_data["step_9"].get("result")
                            get_head_point_and_frame(head_point_results, head_frame_results, range_of_head_coordinates,
                                                     person_num,
                                                     scenario_name, sub_dir, sub_file_of_scenario, frame_index, truth)
                        else:
                            try:
                                if person_num > 0:
                                    logging.error(
                                        f"人头框人头点无值但有人数,{scenario_name},{sub_dir},{sub_file_of_scenario},{person_num}")
                            except Exception:
                                print(f"{sub_dir},{frame_index},{person_num}")

                    if scenario_name in ["retrograde"]:
                        if file_data["step_7"].get("result") and file_data["step_9"].get("result"):
                            head_point_results = file_data["step_9"].get("result")
                            head_frame_results = file_data["step_7"].get("result")
                            get_head_point_and_frame(head_point_results, head_frame_results, range_of_head_coordinates,
                                                     person_num,
                                                     scenario_name, sub_dir, sub_file_of_scenario, frame_index, truth)
                        else:
                            try:
                                if person_num > 0:
                                    logging.error(
                                        f"人头框人头点无值,但有逆行人数{scenario_name},{sub_dir},{sub_file_of_scenario},{person_num}")
                            except Exception:
                                print(f"{sub_dir},{frame_index},{person_num},f{type(person_num)}")
                    if scenario_name in ["retrograde"]:
                        if file_data["step_11"].get("result") and file_data["step_13"].get("result"):
                            head_point_results = file_data["step_13"].get("result")
                            head_frame_results = file_data["step_11"].get("result")
                            get_head_point_and_frame(head_point_results, head_frame_results, range_of_head_coordinates,
                                                     person_num,
                                                     scenario_name, sub_dir, sub_file_of_scenario, frame_index, truth)
                        else:
                            try:
                                if person_num > 0:
                                    logging.error(
                                        f"人头框人头点无值,但有逆行人数{scenario_name},{sub_dir},{sub_file_of_scenario},{person_num}")
                            except Exception:
                                print(f"{sub_dir},{frame_index},{person_num},f{type(person_num)}")
            truth_file = None
            if scenario_name in ["cross_line"]:
                pass
            else:
                if scenario_name not in os.listdir(write_truth_dir):
                    os.popen(f"cd {write_truth_dir};mkdir {scenario_name}")
                scenario_truth_dir = os.path.join(write_truth_dir, scenario_name, sub_dir + ".txt")
                truth_file = scenario_truth_dir.split("/")[-1]
                with open(scenario_truth_dir, "w") as fp:
                    fp.write(json.dumps(truth))
            video_name = sub_dir.split("image")[0][0:-1] + "_" + sub_dir.split("_")[-1] + ".mp4"
            if scenario_name in ["density"]:
                write_table.append(
                    [scenario_id, scenario_desc, video_name, json.dumps(pixel), json.dumps(labeled_person),
                     json.dumps(roi), json.dumps({"truth": truth_file})])
            if scenario_name in ["strand", "intrusion", "social_distance", "congregate_scatter"]:
                write_table.append(
                    [scenario_id, scenario_desc, video_name, json.dumps(pixel), json.dumps(labeled_person),
                     json.dumps(roi),
                     json.dumps({"truth": truth_file, "range_of_head_coordinates": range_of_head_coordinates})])
            if scenario_name in ["cross_line"]:
                write_table.append(
                    [scenario_id, scenario_desc, video_name, json.dumps(pixel), json.dumps(labeled_person),
                     json.dumps(roi), json.dumps(directions), json.dumps(truth)])
            if scenario_name in ["retrograde"]:
                write_table.append(
                    [scenario_id, scenario_desc, video_name, json.dumps(pixel), json.dumps(labeled_person),
                     json.dumps(roi), json.dumps(directions),
                     json.dumps({"truth": truth_file, "range_of_head_coordinates": range_of_head_coordinates})])
        write_workbook.save(write_path)


def get_person_num(person_num, scenario_name, person_num_attribution, frame_index, truth, sub_dir=None):
    queue_pass = None
    queue_ongoing = None
    queue_drop = None
    if frame_index == "1144":
        pass
    try:
        person_num = int(person_num) if person_num else 0
    except Exception:
        if scenario_name == "queue_management":
            person_num_list = person_num.split(";")
            person_num_attribution = person_num_list[0]
            queue_pass = person_num_list[1][-1]
            queue_ongoing = person_num_list[2][-1]
            queue_drop = person_num_list[3][-1]
        if person_num in ["\n", "", " "]:
            person_num = 0
        else:
            person_num_attribution = person_num.split(":")[0]
            try:
                person_num = int(person_num.split(":")[-1])
            except Exception:
                print(person_num)
                raise Exception(person_num)

    if scenario_name in ["strand", "retrograde", "social_distance", "intrusion", "density"]:
        if person_num_attribution:
            if person_num_attribution == "false":
                if truth.get("roi_1"):
                    truth["roi_1"].update({frame_index: {"num": person_num}})
                else:
                    truth.update({"roi_1": {frame_index: {"num": person_num}}})
            else:
                if truth.get("roi_2"):
                    truth["roi_2"].update({frame_index: {"num": person_num}})
                else:
                    truth.update({"roi_2": {frame_index: {"num": person_num}}})
        else:
            if truth.get("roi_1"):
                if truth["roi_1"].get(frame_index):
                    truth["roi_1"][frame_index].update({"num": person_num})
                else:
                    truth["roi_1"].update({frame_index: {"num": person_num}})
            else:
                truth.update({"roi_1": {frame_index: {"num": person_num}}})
    elif scenario_name in ["queue_management"]:
        if person_num_attribution:
            if person_num_attribution == "false":
                if truth.get("roi_1"):
                    truth["roi_1"].update(
                        {frame_index: {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing}})
                else:
                    truth.update(
                        {"roi_1": {frame_index: {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing}}})
            else:
                if truth.get("roi_2"):
                    truth["roi_2"].update(
                        {frame_index: {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing}})
                else:
                    truth.update(
                        {"roi_2": {frame_index: {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing}}})
        else:
            if truth.get("roi_1"):
                if truth["roi_1"].get(frame_index):
                    truth["roi_1"][frame_index].update(
                        {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing})
                else:
                    truth["roi_1"].update(
                        {frame_index: {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing}})
            else:
                truth.update(
                    {"roi_1": {frame_index: {"pass": queue_pass, "drop": queue_drop, "ongoing": queue_ongoing}}})
    else:
        truth.update({frame_index: person_num})
    if scenario_name == "queue_management":
        return int(queue_ongoing)
    else:
        return int(person_num)


def get_head_point_and_frame(head_point_results, head_frame_results, range_of_head_coordinates, person_num,
                             scenario_name, sub_dir, sub_file_of_scenario, frame_index, truth):
    head_point_results_cp = copy.deepcopy(head_point_results)
    head_frame_results_cp = copy.deepcopy(head_frame_results)
    px_r_result = None
    px_m_result = None
    px_u_result = None
    for head_point_result in head_point_results_cp:
        if head_point_result.get("attribute") == "px_m":
            px_m_result = head_point_result
            head_point_results.remove(head_point_result)
        if head_point_result.get("attribute") == "px_r":
            px_r_result = head_point_result
            head_point_results.remove(head_point_result)
        if head_point_result.get("attribute") == "px_u":
            px_u_result = head_point_result
            head_point_results.remove(head_point_result)

    for head_frame_result in head_frame_results_cp:
        if head_frame_result["valid"] is False:
            head_frame_results.remove(head_frame_result)
    if px_u_result:
        range_of_head_coordinates.update(x=abs(px_r_result["x"] - px_m_result["x"]),
                                         y=abs(px_u_result["y"] - px_m_result["y"]))

    head_frame_results = sorted(head_frame_results, key=lambda e: e["id"])
    head_point_results = sorted(head_point_results, key=lambda e: e["sourceID"])
    num = None
    tag = None
    if isinstance(person_num, int):
        num = int(person_num)
    if isinstance(person_num, dict):
        num = int(person_num.get("person_num"))
        tag = person_num.get("tag")
    if px_u_result:
        pass
    else:
        if len(head_frame_results) != num or len(head_point_results) != num:
            logging.error(f"人头点人头框和人数的值不相等,{scenario_name},{sub_dir},{sub_file_of_scenario},{num}")

    person_infos_2 = []
    person_infos_1 = []

    if head_frame_results and head_point_results:
        for head_frame_result, head_point_result in zip(head_frame_results, head_point_results):
            coordinate = {"x": head_point_result["x"], "y": head_point_result["y"]}
            rectangle = [{"x": head_frame_result["x"], "y": head_frame_result["y"]},
                         {"x": head_frame_result["x"] + head_frame_result["width"],
                          "y": head_frame_result["y"] + head_frame_result["height"]}]
            if scenario_name in ["congregate_scatter"]:

                if head_frame_result["valid"] is True and head_point_result["valid"] is True:
                    person_infos_1.append({"coordinate": coordinate, "rectangle": rectangle})
                else:
                    person_infos_2.append({"coordinate": coordinate, "rectangle": rectangle})

                if person_infos_1:
                    if truth.get("roi_1"):
                        if truth["roi_1"].get(frame_index):
                            truth["roi_1"][frame_index].update(
                                {tag: {"group_persons": [{"persons": person_infos_1, "num": num}]}})
                        else:
                            truth["roi_1"].update({
                                frame_index: {tag: {"group_persons": [{"persons": person_infos_1, "num": num}]}}})
                    else:
                        truth.update({"roi_1": {
                            frame_index: {tag: {"group_persons": [{"persons": person_infos_1, "num": num}]}}}})

                if person_infos_2:
                    if truth.get("roi_2"):
                        if truth["roi_2"].get(frame_index):
                            truth["roi_2"][frame_index].update(
                                {tag: {"group_persons": [{"persons": person_infos_1}]}})
                        else:
                            truth["roi_2"].update({
                                frame_index: {tag: {"group_persons": [{"persons": person_infos_1, "num": num}]}}})
                    else:
                        truth.update({"roi_2": {
                            frame_index: {tag: {"group_persons": [{"persons": person_infos_1, "num": num}]}}}})

            if scenario_name in ["retrograde", "strand", "intrusion", "social_distance"]:
                if head_frame_result["valid"] is True and head_point_result["valid"] is True:
                    person_infos_1.append({"coordinate": coordinate, "rectangle": rectangle})
                else:
                    person_infos_2.append({"coordinate": coordinate, "rectangle": rectangle})
                if person_infos_1:
                    if truth.get("roi_1"):
                        if truth["roi_1"].get(frame_index):
                            truth["roi_1"][frame_index].update({"persons": person_infos_1})
                        else:
                            truth["roi_1"].update({frame_index: {"persons": person_infos_1, "num": num}})
                    else:
                        truth.update({"roi_1": {frame_index: {"persons": person_infos_1, "num": num}}})
                if person_infos_2:
                    if truth.get("roi_2"):
                        if truth["roi_2"].get(frame_index):
                            truth["roi_2"][frame_index].update({"persons": person_infos_2})
                        else:
                            truth["roi_2"].update({frame_index: {"persons": person_infos_2, "num": num}})
                    else:
                        truth.update({"roi_2": {frame_index: {"persons": person_infos_2, "num": num}}})

            # if scenario_name in ["social_distance"]:
            #     if head_frame_result["valid"] is False and head_point_result["valid"] is False:
            #         truth.update({"roi_1": {frame_index: num}})
            #     else:
            #         truth.update({"roi_2": {frame_index: num}})


if __name__ == "__main__":
    format_data_from_sensebee()
