import requests
import json
import time
from datetime import datetime

class GongXueYun:
    def __init__(self, phone, password):
        self.phone = phone
        self.password = password
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
            "Content-Type": "application/json; charset=UTF-8"
        }
        self.token = None
        self.plan_id = None

    def login(self):
        url = "https://api.moguding.net:9000/session/user/v1/login"
        data = {
            "phone": self.phone,
            "password": self.password,
            "loginType": "phone",
            "uuid": ""
        }
        
        try:
            response = self.session.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result["code"] == 200:
                    self.token = result["data"]["token"]
                    self.headers["Authorization"] = self.token
                    print("登录成功！")
                    return True
            print("登录失败，请检查账号密码")
            return False
        except Exception as e:
            print(f"登录异常: {str(e)}")
            return False

    def get_plan_id(self):
        url = "https://api.moguding.net:9000/practice/plan/v3/getPlanByStu"
        data = {"state": ""}
        
        try:
            response = self.session.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result["code"] == 200 and result["data"]:
                    self.plan_id = result["data"][0]["planId"]
                    return True
            return False
        except Exception as e:
            print(f"获取计划ID失败: {str(e)}")
            return False

    def sign(self):
        if not self.get_plan_id():
            print("获取计划ID失败")
            return False

        url = "https://api.moguding.net:9000/attendence/clock/v2/save"
        data = {
            "planId": self.plan_id,
            "longitude": "116.123456",  # 修改为你的经度
            "latitude": "39.123456",    # 修改为你的纬度
            "address": "某某农商银行",   # 修改为你的地址
            "type": "START",
            "device": "iOS",
            "description": ""
        }

        try:
            response = self.session.post(url, headers=self.headers, json=data)
            if response.status_code == 200:
                result = response.json()
                if result["code"] == 200:
                    print(f"签到成功！时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    return True
            print("签到失败")
            return False
        except Exception as e:
            print(f"签到异常: {str(e)}")
            return False

def main():
    # 在这里填写你的账号密码
    phone = "你的手机号"
    password = "你的密码"
    
    # 创建工学云对象
    gxy = GongXueYun(phone, password)
    
    # 登录并签到
    if gxy.login():
        gxy.sign()

if __name__ == "__main__":
    main() 
