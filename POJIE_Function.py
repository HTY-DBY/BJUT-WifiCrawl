import requests
from bs4 import BeautifulSoup


def login(zhang_hao_data, mima_data, Typr_wifi=1):
    # 登录
    if Typr_wifi == 1:
        url = 'https://wlgn.bjut.edu.cn/drcom/login'
        payload = {'callback': 'dr1003',
                   'DDDDD': zhang_hao_data,
                   'upass': mima_data,
                   '0MKKey': '123456',
                   'R1': '0',
                   'R2': '',
                   'R3': '0',
                   'R6': '0',
                   'para': '00',
                   'v6ip': '',
                   'terminal_type': '1',
                   'lang': 'zh-cn',
                   'jsVersion': '4.1',
                   'v': '4699',
                   'lang':  'zh'
                   }
        res = requests.get(url=url, params=payload)
        res_text = str(res.text)
        flow_start_index = find_n_sub_str(res_text, 'result', 0)
        ldap_index = find_n_sub_str(res_text, 'ldap auth error', 0)
        if int(res_text[flow_start_index+8]) == 1 & ldap_index == -1:
            return 'ture'
        elif ldap_index != -1:
            return 'flase'
        else:
            return
    if Typr_wifi == 2:
        url = "https://lgn.bjut.edu.cn/"
        data = {'DDDDD': zhang_hao_data,
                'upass': mima_data,
                'v46s': '1',
                'v6ipL': '',
                'f4serip': '172.30.201.2',
                '0MKKey': ''
                }
        res = requests.post(url=url, data=data)
        soup_login_res = BeautifulSoup(res.text, 'html.parser')
        login_res_str = str(soup_login_res.script)
        ldap_index = find_n_sub_str(login_res_str, 'ldap auth error', 0)
        if ldap_index == -1:
            return 'ture'
        else:
            return 'flase'


def find_n_sub_str(src, sub, pos, start=0):
    # 找到第pos个sub在src的位置，start默认填0
    index = src.find(sub, start)
    if index != -1 and pos > 0:
        return find_n_sub_str(src, sub, pos - 1, index + 1)
    return index


def find_is_used(zhang_hao_data, mima_data, Typr_wifi):
    '''
    再次登录获取余额等信息
    flow_finall:已用流量
    fee_finall:余额
    false:1,可用
    false:0,不可用
    '''
    try:
        login_return = login(zhang_hao_data, mima_data, Typr_wifi)
        if login_return == 'flase':
            print('已用流量:', 0, '余额', 0, '状态', '密码错误')
            return [0, 0, '密码错误']
        r = requests.get('http://lgn.bjut.edu.cn/')
        soup = BeautifulSoup(r.text, 'html.parser')
        ALL_str = str(soup.script)
        # flow
        flow_start_index = find_n_sub_str(ALL_str, '\'', 2)
        flow_end_index = find_n_sub_str(ALL_str, '\'', 3)
        flow = ALL_str[flow_start_index+1:flow_end_index]
        try:
            flow = float(flow)
        except:
            try:
                r = requests.get('http://lgn.bjut.edu.cn/')
                soup = BeautifulSoup(r.text, 'html.parser')
                ALL = soup.script
                ALL_str = str(soup.script)
                # flow
                flow_start_index = find_n_sub_str(ALL_str, '\'', 2, 0)
                flow_end_index = find_n_sub_str(ALL_str, '\'', 3, 0)
                flow = ALL_str[flow_start_index+1:flow_end_index]
                try:
                    flow = float(flow)
                except:
                    flow = 0
            except:
                flow = 0
        # false
        false_index = find_n_sub_str(ALL_str, 'fsele', 0)
        try:
            false = int(ALL_str[false_index+6:false_index+7])
        except:
            try:
                r = requests.get('http://lgn.bjut.edu.cn/')
                soup = BeautifulSoup(r.text, 'html.parser')
                ALL = soup.script
                ALL_str = str(soup.script)
                # flow
                false_index = find_n_sub_str(ALL_str, 'fsele', 0, 0)
                try:
                    false = int(ALL_str[false_index+6:false_index+7])
                except:
                    false = '流量已用完'
            except:
                false = '流量已用完'

        # fee
        fee_start_index = find_n_sub_str(ALL_str, '\'', 4)
        fee_end_index = find_n_sub_str(ALL_str, '\'', 5)
        try:
            fee = float(ALL_str[fee_start_index+1:fee_end_index])
        except:
            try:
                r = requests.get('http://lgn.bjut.edu.cn/')
                soup = BeautifulSoup(r.text, 'html.parser')
                ALL = soup.script
                ALL_str = str(soup.script)
                # flow
                fee_start_index = find_n_sub_str(ALL_str, '\'', 4, 0)
                fee_end_index = find_n_sub_str(ALL_str, '\'', 5, 0)
                try:
                    fee = float(ALL_str[fee_start_index+1:fee_end_index])
                except:
                    fee = 0
            except:
                fee = 0
        flow0 = flow % 1024
        flow1 = flow-flow0
        flow0 = flow0 * 1000
        flow0 = flow0-flow0 % 1024
        fee1 = fee-fee % 100
        fee_finall = fee1/10000
        flow_finall = flow1/1024+flow0/1024/1000
    except:
        [flow_finall, fee_finall, false] = ['error', 'error', 'error']
    print('已用流量:', flow_finall, '余额', fee_finall, '状态', false)
    return [flow_finall, fee_finall, false]


if __name__ == '__main__':
    zhang_hao_data = 18374215
    mima_data = 214602
    find_is_used(zhang_hao_data=zhang_hao_data,
                 mima_data=mima_data,
                 Typr_wifi=1)
