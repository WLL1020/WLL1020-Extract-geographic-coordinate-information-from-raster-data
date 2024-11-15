# coding UTF-8
from osgeo import gdal
gdal.UseExceptions()  # 使用 GDAL 的异常处理

from pylab import *  # 支持中文

mpl.rcParams['font.sans-serif'] = ['SimHei']
from openpyxl import Workbook


def out(data, name):
    with open(name, 'w') as f:
        head = ['经度', '纬度', 'ST_B10']
        f.write(','.join(head) + '\n')
        for line in data:
            for pixel in line:
                # 只输出ST_B10不为0的值
                if pixel[2] != -124.149994:
                    f.write(','.join([str(i) for i in pixel[:3]]) + '\n')
        f.close()


if __name__ == "__main__":
    filePath = 'E:/测绘论文/BaseData/InsertPoint/结果/温度2_评论区公式忽略值.tif'  # tif文件路径
    dataset = gdal.Open(filePath)  # 打开tif


    # 获取行数列数和地理信息
	# geo_information(0):左上像素左上角的x坐标。
	# geo_information(1):w - e像素分辨率 / 像素宽度。
	# geo_information(2):行旋转（通常为零）。
	# geo_information(3):左上像素左上角的y坐标。
	# geo_information(4):列旋转（通常为零）。
	# geo_information(5):n - s像素分辨率 / 像素高度（北半球上图像为负值）

    geo_information = dataset.GetGeoTransform()
    print(geo_information)
    col = dataset.RasterXSize  # 7531
    row = dataset.RasterYSize  # 7681
    band = dataset.RasterCount
    print('col:', col, 'row:', row, 'band:', band)
    dem = dataset.GetRasterBand(1).ReadAsArray()

    splitNums = [50]  # 每隔多少个点生成一个点
    for splitNum in splitNums:
        cols = []
        print(f'开始生成{splitNum}点位坐标')
        for y in range(0, row, splitNum):  # 行
            rows = []
            for x in range(0, col, splitNum):  # 列
                lon = geo_information[0] + x * geo_information[1] + y * geo_information[2]
                lat = geo_information[3] + x * geo_information[4] + y * geo_information[5]
                child = [lon, lat, dem[y][x]]
                rows.append(child)
            cols.append(rows)
        filePath = f'{splitNum}2间隔点位坐标.csv'
        out(cols, filePath)
        print(f'表已经生成: {filePath}')
