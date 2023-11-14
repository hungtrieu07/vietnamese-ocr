import importlib.util

from paddleocr import PaddleOCR


def get_module_path(my_module_name):
    spec = importlib.util.find_spec(my_module_name)
    if spec and spec.origin:
        return spec.origin
    return None

def modify_paddleocr_file(my_file_path):
    with open(my_file_path, "r", encoding="utf-8") as file_to_check:
        lines = file_to_check.readlines()
    # Check if the file has enough lines
    if len(lines) > 674:
        # Modify the specified line
        if "if not dt_boxes" in lines[673]:
            print("content of line 674: ", lines[673])
            lines[673] = "                if not dt_boxes.any():\n"
        else:
            print("The content of line 674 doesn't match the expected content.")
            return
    with open(my_file_path, "w", encoding="utf-8") as file_to_modify:
        file_to_modify.writelines(lines)
    print("File modified successfully!")


module_name = "paddleocr"
file_path = get_module_path(module_name).replace("__init__.py", "paddleocr.py")

if file_path:
    print(f"Found at: {file_path}")
    modify_paddleocr_file(file_path)
else:
    print("Module not found!")


PaddleOCR(use_angle_cls=True, lang="en", ocr_version="PP-OCRv4")