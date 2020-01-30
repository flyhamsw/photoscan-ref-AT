from innophotoscan import Innophotoscan


def reference_image_AT(query_fname, query_x, query_y, query_z, distance_thr, query_accuracy=100):
    # Search nearby images
    reference_image_data_list = []
    with open('reference_image_adjusted_EOs.txt') as f:
        for row in f.readlines():
            reference_image_data_list.append(row.split(','))

    # Select nearby images
    selected_fname_list = []
    for reference_image_data in reference_image_data_list:
        dx = query_x - float(reference_image_data[2])
        dy = query_y - float(reference_image_data[3])
        current_distance = (dx**2 + dy**2) ** 0.5
        if current_distance < distance_thr:
            selected_fname_list.append(reference_image_data[0])

    # Append query image to selected images
    selected_fname_list.append(query_fname)

    # Write a new reference file with reference images and the query image
    with open('reference_query_merged.txt', 'w') as f:
        for reference_image_data in reference_image_data_list:
            f.write('%s,%s,%s,%s,%s' % (reference_image_data[0], reference_image_data[1], reference_image_data[2], reference_image_data[3], reference_image_data[4]))
        f.write('%s,%s,%s,%s,%s' % (query_fname, query_accuracy, query_x, query_y, query_z))

    ip = Innophotoscan()
    EO = ip.photoscan_alignphotos(selected_fname_list)


reference_image_AT('DJI_0411.JPG', 240773.156605, 543483.567496, 59.052039, 50)
