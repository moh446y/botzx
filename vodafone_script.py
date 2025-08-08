import requests
import time

owner = "01021024210"  # رقم Owner
password_owner = "Am#@01021024210"  # باسورد Owner

member1 = "01090969508"  # رقم Member1
password_member1 = ""  # لو عايز تضيف باسورد Member1
member2 = "01019028571"  # رقم Member2
password_member2 = "Am#@01019028571"  # باسورد Member2

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
    "msisdn": "",
    "Accept": "application/json",
    "Accept-Language": "ar",
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "mobile.vodafone.com.eg",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/4.11.0"
}

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
            print('تم تسجيل الدخول بنجاح ✅')
            return access_token
        else:
            print('فشل تسجيل الدخول: رقم الهاتف أو كلمة المرور غير صحيحة ❌')
            return None

    except Exception as e:
        print(f'حدث خطأ أثناء الاتصال: {str(e)}')
        return None

def send_invitation(type_, owner, member, access_token, quota):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = owner
    data = {
        "category": [
            {
                "listHierarchyId": "PackageID",
                "value": "523"
            },
            {
                "listHierarchyId": "TemplateID",
                "value": "47"
            },
            {
                "listHierarchyId": "TierID",
                "value": "523"
            }
        ],
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [
                    {
                        "characteristicName": "quotaDist1",
                        "type": "percentage",
                        "value": quota
                    }
                ]
            },
            "member": [
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": owner
                        }
                    ],
                    "type": "Owner"
                },
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": member
                        }
                    ],
                    "type": "Member"
                }
            ]
        },
        "type": "SendInvitation"
    }
    response = requests.post(url, headers=headers, json=data).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        print('again....')
        return send_invitation(type_, owner, member, access_token, quota)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return send_invitation(type_, owner, member, access_token, quota)
    print(type_, response)

def Accept_invitation(type_, owner, member, access_token):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = member
    payload = {
        "category": [
            {
                "listHierarchyId": "TemplateID",
                "value": "47"
            }
        ],
        "name": "FlexFamily",
        "parts": {
            "member": [
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": owner
                        }
                    ],
                    "type": "Owner"
                },
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": member
                        }
                    ],
                    "type": "Member"
                }
            ]
        },
        "type": "AcceptInvitation"
    }

    response = requests.patch(url, headers=headers, json=payload).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        print('again....')
        return Accept_invitation(type_, owner, member, access_token)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return Accept_invitation(type_, owner, member, access_token)
    print(type_, response)

def Change_quota(type_, owner, member, access_token, quota):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = owner

    payload = {
        "category": [
            {
                "listHierarchyId": "TemplateID",
                "value": "47"
            }
        ],
        "createdBy": {
            "value": "MobileApp"
        },
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [
                    {
                        "characteristicName": "quotaDist1",
                        "type": "percentage",
                        "value": quota
                    }
                ]
            },
            "member": [
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": owner
                        }
                    ],
                    "type": "Owner"
                },
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": member
                        }
                    ],
                    "type": "Member"
                }
            ]
        },
        "type": "QuotaRedistribution"
    }

    response = requests.patch(url, headers=headers, json=payload).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        print('again....')
        return Change_quota(type_, owner, member, access_token, quota)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return Change_quota(type_, owner, member, access_token, quota)

    print(type_, response)

def Delete_member(type_, owner, member, access_token):
    url = url_Global
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = owner
    data = {
        "category": [
            {
                "listHierarchyId": "TemplateID",
                "value": "47"
            }
        ],
        "createdBy": {
            "value": "MobileApp"
        },
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [
                    {
                        "characteristicName": "Disconnect",
                        "value": "0"
                    },
                    {
                        "characteristicName": "LastMemberDeletion",
                        "value": "1"
                    }
                ]
            },
            "member": [
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": owner
                        }
                    ],
                    "type": "Owner"
                },
                {
                    "id": [
                        {
                            "schemeName": "MSISDN",
                            "value": member
                        }
                    ],
                    "type": "Member"
                }
            ]
        },
        "type": "FamilyRemoveMember"
    }
    response = requests.patch(url, headers=headers, json=data).text
    if '"API rate limit exceeded"' in response:
        time.sleep(8)
        print('again....')
        return Delete_member(type_, owner, member, access_token)
    elif '"code":"3999"' in response:
        time.sleep(20)
        return Delete_member(type_, owner, member, access_token)
    print(type_, response)

def info_felix(number, password, access_token):
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup?type=Family"
    headers = headers_Global.copy()
    headers['Authorization'] = "Bearer "+access_token
    headers['msisdn'] = owner
    response = requests.get(url, headers=headers).json()
    print('Flexes =>', response[0]['parts']['member'][0]['characteristic']['characteristicsValue'][0]['value'])
