# Vietnamese OCR

1. Crawler: Cào dữ liệu từ 1 website, với các hệ điều hành khác nhau, cần phải tải [Chrome Driver](https://googlechromelabs.github.io/chrome-for-testing/#stable) tương ứng

## Cách clone repo

```bash
git clone --recurse-submodules https://github.com/hungtrieu07/vietnamese-ocr
```

## Cài đặt môi trường (khuyến khích sử dụng Miniconda)

```bash
conda create -n ocr python=3.8
conda activate ocr
pip install -r requirement.txt
```

Bạn có thể sửa batch size trong file [predict.py](predict.py) để tăng tốc dự đoán trên các card đồ họa cao cấp

```python
batch_size = 16         # 32, 64, 128, 256, 512, 1024, 2048, 4096
```
