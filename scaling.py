def calculate_proportion(input, output):
    cumsum_input = np.cumsum(input[0], axis=0)
    cumsum_output = np.cumsum(output[0], axis=0)

    input_x = [point[0] for point in cumsum_input]
    input_y = [point[1] for point in cumsum_input]

    input_x_max = np.max(input_x)
    input_x_min = np.min(input_x)
    input_y_max = np.max(input_y)
    input_y_min = np.min(input_y)

    output_x = [point[0] for point in cumsum_output]
    output_y = [point[1] for point in cumsum_output]

    output_x_max = np.max(output_x)
    output_x_min = np.min(output_x)
    output_y_max = np.max(output_y)
    output_y_min = np.min(output_y)

    print("input: ", input_x_max, input_x_min, input_y_max, input_y_min)
    print("output: ", output_x_max, output_x_min, output_y_max, output_y_min)

    input_width = input_x_max - input_x_min
    input_height = input_y_max - input_y_min

    output_width = output_x_max - output_x_min
    output_height = output_y_max - output_y_min

    print("intput: ", input_width, input_height)
    print("output: ", output_width, output_height)

    factor_x = input_width / output_width
    factor_y = input_height / output_height

    return factor_x, factor_y

def find_first_stroke(input):
    # np.where 함수는 조건을 만족하는 요소의 인덱스를 반환합니다.
    # points 배열의 모든 요소 중에서 세 번째 열의 값이 1인 첫 번째 요소의 인덱스를 찾습니다.
    # 이때, ravel() 함수를 사용하여 다차원 배열을 1차원 배열로 펼칩니다.
    in_indices =  np.where(in_points[:, :, 2].ravel() == 1)[0]

    input_index = in_indices[0]
    
    input_1 = input[:, :(input_index + 1):, :]

    return input_1
