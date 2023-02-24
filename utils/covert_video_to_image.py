import os

if __name__ == "__main__":
    video_map = {
        # 1: "density_video",
        # 2: "cross_line_video",
        # 3: "intrusion_video",
        # 4: "retrograde_video",
        # 5: "strand_video",
        # 6: "congregate_scatter_video",
        # 7: "social_distance_video",
        # 8: "queue_management_video",
        9: "overcrowd_video"
    }
    image_map = {
        # 1: "density_image",
        # 2: "cross_line_image",
        # 3: "intrusion_image",
        # 4: "retrograde_image",
        # 5: "strand_image",
        # 6: "congregate_scatter_image",
        # 7: "social_distance_image",
        # 8: "queue_management_image",
        9: "overcrowd_image"
    }
    path = "/Users/wangsuhua/Downloads/sx"
    ls_cmd = f"cd {path};ls"
    video_dir_name_list = []
    with os.popen(ls_cmd) as fp:
        video_dir_list = fp.readlines()
    for d in video_dir_list:
        try:
            video_dir = int(d.strip("\n"))
            video_dir_name_list.append(video_dir)
        except Exception:
            pass
    for video_dir in video_dir_name_list:
        if video_dir in video_map.keys():
            os.popen(f"cd {path};mv {video_dir} {video_map[video_dir]};mkdir {image_map[video_dir]}")

            with os.popen(f"cd {os.path.join(path, video_map[video_dir])};ls") as fp:
                video_names = fp.readlines()
            for video in video_names:
                video_copy = video.strip("\n")
                x = video_copy.split(".")[0]
                image_path = os.path.join(path, image_map[video_dir])
                os.popen(f"cd {os.path.join(path, image_map[video_dir])};mkdir {image_map[video_dir]}_{x}")
                image_name = f"{image_map[video_dir]}_{x}"
                cmd = f"ffmpeg -i {os.path.join(path, video_map[video_dir])}/{video_copy} -r 25 {os.path.join(path, image_map[video_dir], image_name)}/%05d.jpg"
                os.popen(cmd)
