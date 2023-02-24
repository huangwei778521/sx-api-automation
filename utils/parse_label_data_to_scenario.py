import copy
import json
import xlrd
import openpyxl
from utils.coordinate_transfer import location_transfer_by_height_and_width


def parse_label_data_to_scenario():
    vis_request_body = {
        "source_info": {
            "source_id": {
                "region_id": 10,
                "camera_idx": 10
            },
            "source": {
                "type": "VN_RTSP",
                "parameter": {
                    "rtsp": {
                        "url": "rtsp://{}/{}",
                        "protocol_type": "TCP"
                    }
                }
            }
        }
    }
    cross_line_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"cross_line": {
                        "configs": [
                            {
                                "roi_id": "integer (int32)",
                                "border_offset": 400,
                                "line_points": [
                                    {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    }
                                ],
                                "direction": {
                                    "start_point": {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    },
                                    "end_point": {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    }
                                },
                                "output_interval": 3
                            }
                        ],
                        "use_detection_mode": "LOCALIZATION"
                    }}]
                }
            }
        }
    }
    retrograde_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"retrograde": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "direction": {
                                    "start_point": {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    },
                                    "end_point": {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    }
                                },
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    congregate_scatter_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"congregate": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "cnt_thresh": 5,
                                "time_thresh": 10,
                                "distance_thresh": 1.5,
                                "enable_scatter_analyze": True,
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    density_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"density": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "density_thresh": 1,
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    strand_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"strand": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "strand_thresh": 1,
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    intrusion_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"intrusion": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    social_distance_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"social_distance": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "time_thresh": 10,
                                "distance_thresh": 1.5,
                                "pair_thresh": 1,
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }

    area_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"area": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    queue_management_vps_request_body = {
        "task": {
            "object_type": "OBJECT_CROWD",
            "source_address": "",
            "camera_info": {
                "camera_id": "",
                "internal_id": {
                    "region_id": 20,
                    "camera_idx": 20
                }
            },
            "task_object_config": {
                "crowd_v2": {
                    "panoramic_mode": "OutputForever",
                    "labeled_persons": [{
                        "head_y": "number (float)",
                        "foot_y": "number (float)"
                    }],
                    "crowd_event_rules": [{"queue": {
                        "configs": [
                            {
                                "roi_config": {
                                    "roi_id": "integer (int32)",
                                    "vertices": [
                                        {
                                            "x": "number (float)",
                                            "y": "number (float)"
                                        }
                                    ]
                                },
                                "queue_line": {
                                    "start_point": {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    },
                                    "end_point": {
                                        "x": "number (float)",
                                        "y": "number (float)"
                                    }
                                },
                                "output_interval": 1
                            }
                        ]
                    }}]
                }
            }
        }
    }
    vps_request_map = {"cross_line": cross_line_vps_request_body,
                       "congregate_scatter": congregate_scatter_vps_request_body,
                       "retrograde": retrograde_vps_request_body,
                       "density": density_vps_request_body,
                       "strand": strand_vps_request_body,
                       "intrusion": intrusion_vps_request_body,
                       "social_distance": social_distance_vps_request_body,
                       "area": area_vps_request_body,
                       "queue_management": queue_management_vps_request_body}
    roi_map = {"cross_line": "cross_line",
               "congregate_scatter": "congregate",
               "retrograde": "retrograde",
               "density": "density",
               "strand": "strand",
               "intrusion": "intrusion",
               "social_distance": "social_distance",
               "area": "area",
               "queue_management": "queue"}
    roi_id_map = {"roi_1": 0,
                  "roi_2": 1}
    video_parameter = {
        "height": "",
        "width": ""
    }

    read_path = "/Users/wangsuhua/Downloads/sx1.3_accuracy_truth.xlsx"
    write_path = "/Users/wangsuhua/Downloads/sx_test_accuracy_scenario_new.xlsx"

    write_workbook = openpyxl.Workbook()
    with xlrd.open_workbook(read_path) as read_data:
        sheet_names = read_data.sheet_names()
        for read_index, sheet_name in enumerate(sheet_names):
            vps_request_body_sheet_name = vps_request_map[sheet_name]
            roi_name = roi_map[sheet_name]
            write_table = write_workbook.create_sheet(index=read_index, title=sheet_name)
            table = read_data.sheet_by_name(sheet_name)
            rows = table.nrows  # 行
            cols = table.ncols  # 列
            titles = table.row_values(0)
            title_map = {}
            for index, title in enumerate(titles):
                title_map.update({index: title})
            for r in range(0, rows):
                vps_request_body = copy.deepcopy(vps_request_body_sheet_name)
                if r == 0:
                    write_table.append(
                        ["scenario_desc", "scenario_id", "vis_request_body", "vps_request_body", "truth"])
                else:
                    write_data = []
                    row_values = table.row_values(r)
                    for c in range(0, cols):
                        try:
                            row_value = json.loads(row_values[c])
                        except Exception:
                            row_value = row_values[c]

                        if title_map[c] == "scenario_desc":
                            scenario_desc = row_value
                        elif title_map[c] == "pixel":
                            pixel_width = row_value["width"]
                            pixel_height = row_value["height"]
                            if pixel_width != 1920:
                                video_parameter["width"] = pixel_width
                                video_parameter["height"] = pixel_height
                                vps_request_body["task"]["video_parameter"] = video_parameter
                        elif title_map[c] == "scenario_id":
                            scenario_id = row_value
                        elif title_map[c] == "truth":
                            if isinstance(row_value, dict):
                                truth = row_value
                                # if sheet_name not in ["cross_line"]:
                                #     truth.update({"actual_start_play_frame": 295})
                                truth = json.dumps(truth)

                        elif title_map[c] == "video_name":
                            video_name = row_value
                            vis_request_body_copy = copy.deepcopy(vis_request_body)
                            vis_request_body_copy["source_info"]["source"]["parameter"]["rtsp"]["url"] = \
                                vis_request_body_copy["source_info"]["source"]["parameter"]["rtsp"]["url"].format(
                                    "{}", video_name)
                        else:
                            if title_map[c] == "labeled_person":
                                labeled_person = location_transfer_by_height_and_width(row_value, pixel_height,
                                                                                       pixel_height, "labeled_person",
                                                                                       is_labeled_y=True)
                                vps_request_body["task"]["task_object_config"]["crowd_v2"][
                                    "labeled_persons"] = labeled_person
                            elif title_map[c] == "roi":
                                roi_dicts = row_value
                                if len(roi_dicts.keys()) > 1:
                                    roi_0 = copy.deepcopy(
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                            0][roi_name]["configs"][0])
                                    for x in range(1, len(roi_dicts.keys())):
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                            0][roi_name]["configs"].append(roi_0)
                                for roi_key, roi_value in roi_dicts.items():
                                    roi = location_transfer_by_height_and_width(roi_value, pixel_height, pixel_width)
                                    if sheet_name not in ["cross_line"]:
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                            0][roi_name]["configs"][roi_id_map[roi_key]]["roi_config"]["vertices"] = roi
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                            0][roi_name]["configs"][roi_id_map[roi_key]]["roi_config"]["roi_id"] = \
                                            roi_id_map[roi_key]
                                    else:
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                            0][roi_name]["configs"][roi_id_map[roi_key]]["line_points"] = roi
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                            0][roi_name]["configs"][roi_id_map[roi_key]]["roi_id"] = roi_id_map[roi_key]
                            elif title_map[c] == "line":
                                cross_line_dicts = row_value
                                if len(cross_line_dicts.keys()) > 1:
                                    for x in range(1, len(cross_line_dicts.keys())):
                                        roi_0 = \
                                            vps_request_body["task"]["task_object_config"]["crowd_v2"][roi_name][0]
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"][
                                            roi_name].append(roi_0)
                                for cross_line_key, cross_line_value in cross_line_dicts.items():
                                    cross_line = location_transfer_by_height_and_width(cross_line_value)
                                    if len(cross_line) == 6:
                                        for x in range(0, int(6 / 2)):
                                            y = x * 2
                                            cross_lines_0 = \
                                                vps_request_body["task"]["task_object_config"]["crowd_v2"][
                                                    roi_name][roi_id_map[cross_line_key]]["cross_lines"][0]
                                            vps_request_body["task"]["task_object_config"]["crowd_config"][
                                                roi_name][roi_id_map[cross_line_key]]["cross_lines"].append(
                                                cross_lines_0)
                                            vps_request_body["task"]["task_object_config"]["crowd_v2"][
                                                roi_name][roi_id_map[cross_line_key]]["cross_lines"][x][
                                                "vertices"] = cross_line[y:y + 2]
                                    else:
                                        vps_request_body["task"]["task_object_config"]["crowd_v2"][
                                            roi_name][roi_id_map[cross_line_key]]["cross_lines"][0][
                                            "vertices"] = cross_line
                            elif title_map[c] == "directions":
                                directions = row_value
                                for direction_key, direction_value in directions.items():
                                    vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                        0][roi_name]["configs"][roi_id_map[direction_key]]["direction"][
                                        "start_point"] = direction_value[0]
                                    vps_request_body["task"]["task_object_config"]["crowd_v2"]["crowd_event_rules"][
                                        0][roi_name]["configs"][roi_id_map[direction_key]]["direction"]["end_point"] = \
                                        direction_value[1]
                            elif title_map[c] == "queue_line":
                                queue_lines = row_value
                                for queue_line_key, queue_line_value in queue_lines.items():
                                    queue_line_v = location_transfer_by_height_and_width(queue_line_value)
                                    vps_request_body["task"]["task_object_config"]["crowd_v2"][roi_name][
                                        roi_id_map[queue_line_key]]["queue_line"]["start_point"] = queue_line_v[0]
                                    vps_request_body["task"]["task_object_config"]["crowd_v2"][roi_name][
                                        roi_id_map[queue_line_key]]["queue_line"]["end_point"] = queue_line_v[1]
                    write_data.extend(
                        [scenario_desc, scenario_id, json.dumps(vis_request_body_copy), json.dumps(vps_request_body),
                         truth])
                    write_table.append(write_data)
        write_workbook.save(write_path)


if __name__ == "__main__":
    parse_label_data_to_scenario()
