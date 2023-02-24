def location_transfer_by_height_and_width(location_list, height=1080, width=1920, location_type=None,
                                          is_labeled_y=False):
    location_list_new = []
    location_list_labeled_person = []

    if location_type == "labeled_person":
        for ll in location_list:
            element_dict = {}
            element_dict.update({"x": round(ll[0] / width, 10)})
            element_dict.update({"y": round(ll[1] / height, 10)})
            location_list_labeled_person.append(element_dict)
    else:
        for location in location_list:
            x = round(location[0] / width, 10)
            y = round(location[1] / height, 10)
            location_dict = {"x": x, "y": y}
            location_list_new.append(location_dict)

    if location_type == "labeled_person":
        element_dict = {}
        if is_labeled_y:
            for i, element in enumerate(location_list_labeled_person):
                element_dict.update(head_y=element["x"], foot_y=element["y"])
                location_list_new.append(element_dict)
                element_dict = {}
        else:
            for i, element in enumerate(location_list_labeled_person):

                if i & 1 == 0:
                    x = element["y"]
                    element_dict.update(head_y=x)
                else:
                    y = element["y"]
                    element_dict.update(foot_y=y)
                    location_list_new.append(element_dict)
                    element_dict = {}

    return location_list_new


def relocation_transfer_by_height_and_width(location_list, height, width):
    new_location = []
    for l in location_list:
        new_l = []
        x = round(l["x"] * width)
        y = round(l["y"] * height)
        new_l.append(x)
        new_l.append(y)
        new_location.append(new_l)
    return new_location


if __name__ == "__main__":
    location_list = [
        [
          344.4137931034483,
          441.1379310344828
        ],
        [
          682.344827586207,
          773.896551724138
        ],
        [
          1515.9655172413793,
          348.89655172413796
        ]
      ]
    print(location_transfer_by_height_and_width(location_list, height=1080, width=1920))
    # print(location_transfer_by_height_and_width(location_list, height=2160, width=2160, location_type="labeled_person",
    #                                             is_labeled_y=True))
    # print(relocation_transfer_by_height_and_width(location_list, height=1080, width=1920))
