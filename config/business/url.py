business_path = {
    "DeviceManagement": {
        "device_group_add": "/api/camera-device-management/api/v1/device-groups",
        "device_add": "/api/camera-device-management/api/v1/devices"
    },
    "TaskManagement": {
        "face_attribute_add": "/api/task-management/api/v1/task/createTask",
        "face_attribute_query": "/api/timedb-management/api/v1/search/query/attributesSearch",
        "crowd_cam_add": "/api/task-management/api/v1/task/createTask",
        "task_delete": "/api/task-management/api/v1/task/{}",
        "query_alert": "/api/incident-record-management/api/v1/incident/records",
        "query_search_center": "/api/timedb-management/api/v1/search/query/search"
    },
    "MapManagement": {
        "map_upload": "/api/map-management/api/v1/map/upload",
        "device_add_to_map": "/api/map-management/api/v1/map/device/{}"
    }
}
