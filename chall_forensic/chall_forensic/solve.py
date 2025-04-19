with open("endpoint", "rb") as img_file:
    hex_data = img_file.read().hex()

# Chuỗi hex cần tìm
start_sequence = "89504e470d0a"  # 89 50 4E 47 0D 0A
end_sequence = "49454e44ae4260"  # 49 45 4E 44 AE 42 60

# Tìm vị trí xuất hiện thứ hai của start_sequence
start_pos = hex_data.find(start_sequence)
start_pos = hex_data.find(start_sequence, start_pos + len(start_sequence))

# lấy 3367 bytes từ start_pos thứ 2
if start_pos != -1:
    start_chunk = hex_data[start_pos:start_pos + 3367 * 2]  # mỗi byte chiếm 2 ký tự hex

# Tìm vị trí xuất hiện thứ nhất của end_sequence
end_pos = hex_data.find(end_sequence)

#lấy 3366 bytes from end_pos thứ nhất 
if end_pos != -1:
    end_chunk = hex_data[max(0, end_pos - (3366 * 2 - len(end_sequence))):end_pos + len(end_sequence)]

full_hex_data = start_chunk + end_chunk

image_data = bytes.fromhex(full_hex_data)

with open("output_image.png", "wb") as img_output:
    img_output.write(image_data)

print("Đã tạo file ảnh từ chuỗi hex và lưu vào output_image.png.")