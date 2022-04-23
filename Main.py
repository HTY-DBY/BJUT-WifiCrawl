from typing import final
import xlrd
import openpyxl as op
import POJIE_Function
# wifi请调整为1，有线网络请调整为2
Typr_wifi = 2

workbook = xlrd.open_workbook('ALL.xlsx')  # 打开文件
sheet_name = workbook.sheet_names()[0]  # 获取所有sheet
sheet = workbook.sheet_by_index(0)  # 根据sheet索引或者名称获取sheet内容,sheet索引从0开始
OK_tonji = 0
OK_not_tonji = 0

fileName = 'Finall.xlsx'
wb = op.Workbook()  # 创建工作簿对象
ws = wb['Sheet']  # 创建子表
ws.append(['账号', '密码', '已用流量', '余额', '状态'])   # 设置表头

lines = sheet.nrows
print('一共有', lines-1, '组账号数据')

for i in range(lines-1):
    zhang_hao_data = sheet.cell_value(i+1, 0)   # 读取账号
    mima_data = sheet.cell_value(i+1, 1)       # 读取密码
    if isinstance(zhang_hao_data, float):
        zhang_hao_data = str(int(zhang_hao_data))
    if isinstance(mima_data, float):
        mima_data = str(int(mima_data))
    print('数据：', OK_tonji+1, '账号为：', zhang_hao_data,
          '密码为：', mima_data, ' ', end='')
    try:
        OK_tonji = OK_tonji+1
        [flow_finall, fee_finall, false] = POJIE_Function.find_is_used(
            zhang_hao_data=zhang_hao_data,
            mima_data=mima_data,
            Typr_wifi=Typr_wifi)
    except:
        [flow_finall, fee_finall, false] = ['error', 'error', 'error']
    ws.append([zhang_hao_data, mima_data, flow_finall, fee_finall, false])

wb.save(fileName)
print('共', OK_tonji, '组数据成功')
