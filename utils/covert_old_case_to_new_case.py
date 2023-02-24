import copy
import json
import openpyxl
import xlrd


def covert_old_case_to_new_case():
    read_path = "/Users/wangsuhua/Downloads/sx_accuracy_scenario.xlsx"
    write_path = "/Users/wangsuhua/Downloads/sx_accuracy_scenario_all.xlsx"

    vps_request_body_common = {
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
                    "labeled_persons": [
                        {
                            "head_y": "number (float)",
                            "foot_y": "number (float)"
                        }
                    ],
                    "enable_head_map": "boolean (boolean)",
                    "crowd_event_rules": []
                }
            }
        }
    }

    cross_line_vps_request_body = {
        "cross_line": {
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
                    "output_interval": "integer (int32)"
                }
            ],
            "use_detection_mode": "LOCALIZATION"
        }
    }
    retrograde_vps_request_body = {"retrograde": {
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
                "output_interval": "integer (int32)"
            }
        ]
    }}
    congregate_scatter_vps_request_body = {"congregate": {
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
                "cnt_thresh": "integer (int32)",
                "time_thresh": "number (float)",
                "distance_thresh": "number (float)",
                "enable_scatter_analyze": "boolean (boolean)",
                "output_interval": "integer (int32)"
            }
        ]
    }}
    density_vps_request_body = {"density": {
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
                "density_thresh": "integer (int32)",
                "output_interval": "integer (int32)"
            }
        ]
    }}
    strand_vps_request_body = {"strand": {
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
                "strand_thresh": "integer (int32)",
                "output_interval": "integer (int32)"
            }
        ]
    }}
    intrusion_vps_request_body = {"intrusion": {
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
                "output_interval": "integer (int32)"
            }
        ]
    }}
    social_distance_vps_request_body = {"social_distance": {
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
                "time_thresh": "number (float)",
                "distance_thresh": "number (float)",
                "pair_thresh": "integer (int32)",
                "output_interval": "integer (int32)"
            }
        ]
    }}

    area_vps_request_body = {"area": {
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
                "output_interval": "integer (int32)"
            }
        ]
    }}
    queue_management_vps_request_body = {"queue": {
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
                "output_interval": "integer (int32)"
            }
        ]
    }}

    write_workbook = openpyxl.Workbook()
    with xlrd.open_workbook(read_path) as read_data:
        sheet_names = read_data.sheet_names()
        for read_index, sheet_name in enumerate(sheet_names):
            write_table = write_workbook.create_sheet(index=read_index, title=sheet_name)
            table = read_data.sheet_by_name(sheet_name)
            rows = table.nrows  # 行
            cols = table.ncols  # 列
            titles = table.row_values(0)
            title_map = {}
            for index, title in enumerate(titles):
                title_map.update({index: title})
            for r in range(0, rows):
                if r == 0:
                    write_table.append(titles)
                else:
                    write_data = []
                    row_values = table.row_values(r)
                    for c in range(0, cols):
                        try:
                            row_value = json.loads(row_values[c], strict=False)
                        except Exception:
                            row_value = row_values[c]

                        if title_map[c] not in ["vis_request_body", "vps_request_body"]:
                            if isinstance(row_value, (dict, list)):
                                data = json.dumps(row_value)
                            else:
                                data = row_value
                            write_data.append(data)

                        elif title_map[c] == "vps_request_body":
                            vps_request_body = row_value
                            decoder_config = vps_request_body["task"]["task_object_config"].get("decoder_config")
                            if not vps_request_body["task"]["task_object_config"].get("crowd_config"):
                                write_data.append(json.dumps(vps_request_body))
                                break
                            crowd_config = vps_request_body["task"]["task_object_config"]["crowd_config"]
                            label_persons = crowd_config["labeled_person"]["vertices"]
                            if crowd_config.get("enable_density_map"):
                                enable_density_map = crowd_config["enable_density_map"]
                            else:
                                enable_density_map = False
                            panoramic_mode = crowd_config.get("panoramic_mode") if crowd_config.get(
                                "panoramic_mode") else "OutputOnAlarm"
                            for label_person in label_persons:
                                label_person["head_y"] = label_person["x"]
                                label_person["foot_y"] = label_person["y"]
                                label_person.pop("x")
                                label_person.pop("y")
                            vps_request_body_common_cp = copy.deepcopy(vps_request_body_common)

                            vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                "labeled_persons"] = label_persons
                            vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                "panoramic_mode"] = panoramic_mode
                            vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                "enable_head_map"] = enable_density_map

                            if "density" in sheet_name or "density_rois" in json.dumps(vps_request_body):
                                density_vps_request_body_cp = copy.deepcopy(density_vps_request_body)
                                total_crowd_thresh = crowd_config.get("total_crowd_thresh")
                                density_rois = crowd_config.get("density_rois")
                                density_output_interval = crowd_config.get("density_output_interval")
                                if density_rois:
                                    for r in range(0, len(density_rois)):
                                        if r > 0:
                                            roi_config_0 = copy.deepcopy(
                                                density_vps_request_body["density"]["configs"][0])
                                            density_vps_request_body_cp["density"]["configs"].append(roi_config_0)
                                    for roi_configs, rois in zip(density_vps_request_body_cp["density"]["configs"],
                                                                 density_rois):
                                        roi_configs["roi_config"]["roi_id"] = rois["roi_id"]
                                        roi_configs["roi_config"]["vertices"] = rois["roi"]["vertices"]
                                        roi_configs["density_thresh"] = total_crowd_thresh
                                        if density_output_interval:
                                            roi_configs["output_interval"] = density_output_interval
                                        else:
                                            roi_configs["output_interval"] = 1
                                else:
                                    for roi_configs in density_vps_request_body_cp["density"]["configs"]:
                                        roi_configs["density_thresh"] = total_crowd_thresh
                                        if density_output_interval:
                                            roi_configs["output_interval"] = density_output_interval
                                        else:
                                            roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(density_vps_request_body_cp)
                            if "cross_line" in sheet_name or "cross_line_configs" in json.dumps(vps_request_body):
                                cross_line_vps_request_body_cp = copy.deepcopy(cross_line_vps_request_body)
                                cross_line_configs = crowd_config.get("cross_line_configs")
                                cross_line_output_interval = crowd_config.get("cross_line_output_interval")
                                for r in range(0, len(cross_line_configs)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(
                                            cross_line_vps_request_body["cross_line"]["configs"][0])
                                        cross_line_vps_request_body_cp["cross_line"]["configs"].append(roi_config_0)
                                for roi_configs, rois in zip(cross_line_vps_request_body_cp["cross_line"]["configs"],
                                                             cross_line_configs):
                                    roi_configs["roi_id"] = rois["roi_id"]
                                    cross_lines = rois["cross_lines"][0]["vertices"]
                                    roi_configs["line_points"] = cross_lines
                                    roi_configs["direction"]["start_point"] = rois["directions"][0]
                                    roi_configs["direction"]["end_point"] = rois["directions"][1]
                                    if cross_line_output_interval:
                                        roi_configs["output_interval"] = cross_line_output_interval
                                    else:
                                        roi_configs["output_interval"] = 3
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(cross_line_vps_request_body_cp)
                            if "intrusion" in sheet_name:
                                intrusion_vps_request_body_cp = copy.deepcopy(intrusion_vps_request_body)
                                intrusion_rois = crowd_config.get("intrusion_rois")
                                intrusion_output_interval = crowd_config.get("intrusion_output_interval")
                                for r in range(0, len(intrusion_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(
                                            intrusion_vps_request_body["intrusion"]["configs"][0])
                                        intrusion_vps_request_body_cp["intrusion"]["configs"].append(roi_config_0)
                                for roi_configs, rois in zip(intrusion_vps_request_body_cp["intrusion"]["configs"],
                                                             intrusion_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_id"]
                                    roi_configs["roi_config"]["vertices"] = rois["roi"]["vertices"]
                                    if intrusion_output_interval:
                                        roi_configs["output_interval"] = intrusion_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(intrusion_vps_request_body_cp)
                            if "strand" in sheet_name:
                                strand_vps_request_body_cp = copy.deepcopy(strand_vps_request_body)
                                strand_rois = crowd_config.get("strand_rois")
                                strand_thresh = crowd_config.get("strand_thresh")
                                strand_output_interval = crowd_config.get("strand_output_interval")
                                for r in range(0, len(strand_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(strand_vps_request_body["intrusion"]["configs"][0])
                                        strand_vps_request_body_cp["strand"]["configs"].append(roi_config_0)
                                for roi_configs, rois in zip(strand_vps_request_body_cp["strand"]["configs"],
                                                             strand_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_id"] if rois.get("roi_id") else 0
                                    roi_configs["strand_thresh"] = strand_thresh
                                    try:
                                        roi_configs["roi_config"]["vertices"] = rois["roi"]["vertices"]
                                    except Exception:
                                        roi_configs["roi_config"]["vertices"] = rois["vertices"]
                                    if strand_output_interval:
                                        roi_configs["output_interval"] = strand_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(strand_vps_request_body_cp)

                            if "retrograde" in sheet_name or "retrograde_rois" in json.dumps(vps_request_body):
                                retrograde_vps_request_body_cp = copy.deepcopy(retrograde_vps_request_body)
                                retrograde_rois = crowd_config.get("retrograde_rois")
                                retrograde_output_interval = crowd_config.get("retrograde_output_interval")
                                for r in range(0, len(retrograde_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(
                                            retrograde_vps_request_body["retrograde"]["configs"][0])
                                        retrograde_vps_request_body_cp["retrograde"]["configs"].append(roi_config_0)
                                for roi_configs, rois in zip(retrograde_vps_request_body_cp["retrograde"]["configs"],
                                                             retrograde_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_cfg"]["roi_id"]
                                    roi_configs["roi_config"]["vertices"] = rois["roi_cfg"]["roi"]["vertices"]
                                    roi_configs["direction"]["start_point"] = rois["directions"][0]
                                    roi_configs["direction"]["end_point"] = rois["directions"][1]
                                    if retrograde_output_interval:
                                        roi_configs["output_interval"] = retrograde_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(retrograde_vps_request_body_cp)

                            if "congregate" in sheet_name or "scatter" in sheet_name or "frame_skip_vps" in sheet_name or "func_time_vps_push_to_kafka_10" in sheet_name or "congregate_configs" in json.dumps(
                                    vps_request_body):
                                congregate_scatter_vps_request_body_cp = copy.deepcopy(
                                    congregate_scatter_vps_request_body)
                                congregate_scatter_rois = crowd_config.get("congregate_configs")
                                congregate_scatter_output_interval = crowd_config.get("congregate_output_interval")
                                for r in range(0, len(congregate_scatter_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(
                                            congregate_scatter_vps_request_body_cp["congregate"]["configs"][0])
                                        congregate_scatter_vps_request_body_cp["congregate"]["configs"].append(
                                            roi_config_0)
                                for roi_configs, rois in zip(
                                        congregate_scatter_vps_request_body_cp["congregate"]["configs"],
                                        congregate_scatter_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_cfg"]["roi_id"]
                                    roi_configs["roi_config"]["vertices"] = rois["roi_cfg"]["roi"]["vertices"]
                                    roi_configs["cnt_thresh"] = rois["cnt_thresh"]
                                    roi_configs["time_thresh"] = rois["time_thresh"]
                                    roi_configs["distance_thresh"] = rois["distance_thresh"]
                                    enable_scatter_analyze = rois["enable_scatter_analyze"]
                                    if enable_scatter_analyze:
                                        roi_configs["enable_scatter_analyze"] = enable_scatter_analyze
                                    else:
                                        roi_configs["enable_scatter_analyze"] = False
                                    if congregate_scatter_output_interval:
                                        roi_configs["output_interval"] = congregate_scatter_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                if sheet_name == "frame_skip_vps":
                                    decoder_config = crowd_config.get("decoder_config")
                                    vps_request_body_common_cp["task"]["task_object_config"].update(
                                        decoder_config=decoder_config)

                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(congregate_scatter_vps_request_body_cp)

                            if "social_distance" in sheet_name:
                                social_distance_vps_request_body_cp = copy.deepcopy(
                                    social_distance_vps_request_body)
                                social_distance_rois = crowd_config.get("social_distance_configs")
                                social_distance_output_interval = crowd_config.get("social_distance_output_interval")
                                for r in range(0, len(social_distance_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(
                                            social_distance_vps_request_body_cp["social_distance"]["configs"][0])
                                        social_distance_vps_request_body_cp["social_distance"]["configs"].append(
                                            roi_config_0)
                                for roi_configs, rois in zip(
                                        social_distance_vps_request_body_cp["social_distance"]["configs"],
                                        social_distance_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_cfg"]["roi_id"]
                                    roi_configs["roi_config"]["vertices"] = rois["roi_cfg"]["roi"]["vertices"]
                                    roi_configs["pair_thresh"] = rois["pair_thresh"]
                                    roi_configs["time_thresh"] = rois["time_thresh"]
                                    roi_configs["distance_thresh"] = rois["distance_thresh"]
                                    if social_distance_output_interval:
                                        roi_configs["output_interval"] = social_distance_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(social_distance_vps_request_body_cp)
                            if "queue" in sheet_name:
                                queue_vps_request_body_cp = copy.deepcopy(
                                    queue_management_vps_request_body)
                                queue_rois = crowd_config.get("queue_rois")
                                queue_output_interval = crowd_config.get("queue_output_interval")
                                for r in range(0, len(queue_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(
                                            queue_management_vps_request_body["queue"]["configs"][0])
                                        queue_vps_request_body_cp["queue"]["configs"].append(
                                            roi_config_0)
                                for roi_configs, rois in zip(
                                        queue_vps_request_body_cp["queue"]["configs"],
                                        queue_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_cfg"]["roi_id"]
                                    roi_configs["roi_config"]["vertices"] = rois["roi_cfg"]["roi"]["vertices"]
                                    roi_configs["queue_line"]["start_point"] = rois["queue_line"]["vertices"][0]
                                    roi_configs["queue_line"]["end_point"] = rois["queue_line"]["vertices"][1]

                                    if queue_output_interval:
                                        roi_configs["output_interval"] = queue_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(queue_vps_request_body_cp)
                            if "region_statistics" in sheet_name:
                                area_vps_request_body_cp = copy.deepcopy(area_vps_request_body)
                                area_rois = crowd_config.get("area_rois")
                                area_output_interval = crowd_config.get("area_output_interval")
                                for r in range(0, len(area_rois)):
                                    if r > 0:
                                        roi_config_0 = copy.deepcopy(area_vps_request_body["area"]["configs"][0])
                                        area_vps_request_body_cp["area"]["configs"].append(roi_config_0)
                                for roi_configs, rois in zip(area_vps_request_body_cp["area"]["configs"],
                                                             area_rois):
                                    roi_configs["roi_config"]["roi_id"] = rois["roi_id"]
                                    roi_configs["roi_config"]["vertices"] = rois["roi"]["vertices"]
                                    if area_output_interval:
                                        roi_configs["output_interval"] = area_output_interval
                                    else:
                                        roi_configs["output_interval"] = 1
                                vps_request_body_common_cp["task"]["task_object_config"]["crowd_v2"][
                                    "crowd_event_rules"].append(area_vps_request_body_cp)
                            if decoder_config:
                                vps_request_body_common_cp["task"]["task_object_config"][
                                    "decoder_config"] = decoder_config
                            write_data.append(json.dumps(vps_request_body_common_cp))

                        elif title_map[c] == "vis_request_body":
                            vis_request_body = row_value
                            url = vis_request_body["source_info"]["source"]["parameter"]["rtsp"]["url"].replace(
                                "10.8.10.253:554", "{}")
                            vis_request_body["source_info"]["source"]["parameter"]["rtsp"]["url"] = url
                            write_data.append(json.dumps(vis_request_body))
                    write_table.append(write_data)
        write_workbook.save(write_path)


if __name__ == "__main__":
    covert_old_case_to_new_case()
