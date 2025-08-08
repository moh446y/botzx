import requests
import time

owner = "01021024210"  # ممكن تحط بياناتك هنا أو تغيرها من البوت
password_owner = "Am#@01021024210"

member1 = "01090969508"
# password_member1 = ""

member2 = "01019028571"
password_member2 = "Am#@01019028571"

def login(number, password):    
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'silentLogin': 'false',
        'x-dynatrace': 'MT_3_17_3569497752_11-0_a556db1b-4506-43f3-854a-1d2527767923_0_25993_455',
        'x-agent-operatingsystem': '13',
        'clientId': 'AnaVodafoneAndroid',
        'Accept-Language': 'ar',
        'x-agent-device': 'Xiaomi M2101K9AG',
        'x-agent-version': '2025.7.3',
        'x-agent-build': '1068',
        'User-Agent': 'okhttp/4.11.0',
        'Host': 'mobile.vodafone.com.eg',
        'Accept-Encoding': 'gzip',
    }

    data = {
        "username": number,
        "password": password,
        "grant_type": "password",
        "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        "client_id": "my-vodafone-app"
    }

    try:
        res = requests.post(
            "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token",
            headers=headers,
            data=data
        )
        
        if res.status_code == 200:
            access_token = res.json().get("access_token")
            return True, access_token
        else:
            return False, 'فشل تسجيل الدخول: رقم الهاتف أو كلمة المرور غير صحيحة ❌'
            
    except Exception as e:
        return False, f'حدث خطأ أثناء الاتصال: {str(e)}'

url_Global = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"

headers_Global = {
        "x-dynatrace": "MT_3_5_3797388217_8-0_a556db1b-4506-43f3-854a-1d2527767923_0_34216_238",
        "Authorization": "",
        "api-version": "v2",
        "x-agent-operatingsystem": "13",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Xiaomi M2101K9AG",
        "x-agent-version": "2025.7.3",
        "x-agent-build": "1068",
        "msisdn":"",
        "Accept": "application/json",
        "Accept-Language": "ar",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "mobile.vodafone.com.eg",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.11.0"
    }

def send_invitation(type_str, owner_num, member_num, access_token, quota):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn']= owner_num
    data = {
        "category": [
            {"listHierarchyId": "PackageID", "value": "523"},
            {"listHierarchyId": "TemplateID", "value": "47"},
            {"listHierarchyId": "TierID", "value": "523"}
        ],
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "quotaDist1", "type": "percentage", "value": quota}
                ]
            },
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": owner_num}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member_num}], "type": "Member"}
            ]
        },
        "type": "SendInvitation"
    }
    response = requests.post(url, headers=headers, json=data).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        return send_invitation(type_str, owner_num, member_num, access_token, quota)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return send_invitation(type_str, owner_num, member_num, access_token, quota)
    return type_str, response

def Accept_invitation(type_str, owner_num, member_num, access_token):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn']= member_num
    payload = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "name": "FlexFamily",
        "parts": {
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": owner_num}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member_num}], "type": "Member"}
            ]
        },
        "type": "AcceptInvitation"
    }
    response = requests.patch(url, headers=headers, json=payload).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        return Accept_invitation(type_str, owner_num, member_num, access_token)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return Accept_invitation(type_str, owner_num, member_num, access_token)
    return type_str, response

def Change_quota(type_str, owner_num, member_num, access_token, quota):
    url= url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = owner_num
    
    payload = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "createdBy": {"value": "MobileApp"},
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [
                    {"characteristicName": "quotaDist1", "type": "percentage", "value": quota}
                ]
            },
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": owner_num}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member_num}], "type": "Member"}
            ]
        },
        "type": "QuotaRedistribution"
    }
    response = requests.patch(url, headers=headers, json=payload).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        return Change_quota(type_str, owner_num, member_num, access_token, quota)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return Change_quota(type_str, owner_num, member_num, access_token, quota)
    return type_str, response

def Delete_member(type_str, owner_num, member_num, access_token):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = owner_num
    data = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "createdBy": {"value": "MobileApp"},
        "parts": {
            "characteristicsValue": [
                {"characteristicName": "Disconnect", "value": "0"},
                {"characteristicName": "LastMemberDeletion", "value": "1"}
            ],
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": owner_num}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member_num}], "type": "Member"}
            ]
        },
        "type": "FamilyRemoveMember"
    }
    response = requests.patch(url, headers=headers, json=data).text
    if '"API rate limit exceeded"' in response:
          time.sleep(8)
          return Delete_member(type_str, owner_num, member_num, access_token)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return Delete_member(type_str, owner_num, member_num, access_token)
    return type_str, response

def info_felix(number, password, access_token):
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup?type=Family"
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = number
    try:
        response = requests.get(url, headers=headers).json()
        value = response[0]['parts']['member'][0]['characteristic']['characteristicsValue'][0]['value']
        return f"Flexes => {value}"
    except Exception as e:
        return f"خطأ في جلب الفليكس: {str(e)}"


def run_full_cycle(owner_num, password_owner, member1_num, member2_num, password_member2):
    # نعيد تكرار نفس العمليات اللي انت كتبتها
    access_owner = None
    access_member2 = None
    
    success, token_or_msg = login(owner_num, password_owner)
    if not success:
        return token_or_msg
    access_owner = token_or_msg
    
    success, token_or_msg = login(member2_num, password_member2)
    if not success:
        return token_or_msg
    access_member2 = token_or_msg
    
    time.sleep(10)
    send_invitation("send invitation member 2 =>", owner_num, member2_num, access_owner, quota="40")
    time.sleep(10)
    Change_quota("Change percentage member1 from 1300 to 5200 =>", owner_num, member1_num, access_owner, quota="40")
    time.sleep(10)
    Accept_invitation("Accept member 2=>", owner_num, member2_num, access_member2)
    time.sleep(10)
    Delete_member("Remove member 2=>", owner_num, member2_num, access_owner)
    time.sleep(10)
    info_msg = info_felix(owner_num, password_owner, access_owner)
    time.sleep(660)  # 11 دقيقة

    Change_quota("Change percentage member1 1300=>", owner_num, member1_num, access_owner, quota="10")
    return info_msg

# لو حبيت تجرب كود مستقل هنا:
if __name__ == "__main__":
    print("جاري تشغيل السكريبت مباشرة")
    print(run_full_cycle(owner, password_owner, member1, member2, password_member2))
