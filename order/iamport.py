import requests

from django.conf import settings


def get_token():
    """iamport REST api와 통신하기 위해 인증받는 함수"""
    access_data = {
        'imp_key': settings.IAM_KEY,
        'imp_secret': settings.IAM_SECRET
    }
    url = 'https://api.iamport.kr/users/getToken'

    req = requests.post(url, data=access_data)
    res = req.json()

    if res['code'] is 0:
        return res['response']['access_token']
    else:
        return None


def find_transaction(merchant_uid, *args, **kwargs):
    """iamport에서 결제한 transaction 가져오는 함수"""
    access_token = get_token()
    if access_token:
        headers = {
            'Authorization': access_token
        }
        url = 'https://api.iamport.kr/payments/find' + merchant_uid

        req = requests.post(url, headers=headers)
        res = req.json()

        if res['code'] is 0:
            context = {
                'imp_uid': res['response']['imp_uid'],
                'merchant_uid': res['response']['merchant_uid'],
                'name': res['response']['name'],
                'price': res['response']['amount'],
                'status': res['response']['status']
            }
            return context
        else:
            return None
    else:
        raise ValueError('토큰에러')


def payments_prepare(merchant_uid, price, *args, **kwargs):
    access_token = get_token()
    if access_token:
        headers = {
            'Authorization': access_token
        }
        access_data = {
            'merchant_uid': merchant_uid,
            'amount': price
        }

        url = 'https://api.iamport.kr/payments/prepare'
        req = requests(url, data=access_data, headers=headers)

        if req['code'] is not 0:
            raise ValueError('통신에러')

    else:
        raise ValueError('토큰에러')
