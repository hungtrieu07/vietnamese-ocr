import paddle
print(paddle.device.cuda.device_count())
print(paddle.device.cuda.get_device_name())
print(paddle.device.cuda.get_device_capability())
print(paddle.device.cuda.get_device_properties())