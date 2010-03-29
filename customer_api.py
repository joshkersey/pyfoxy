import urllib, time
from xml.dom import minidom
from datetime import date, timedelta, datetime

from django.conf import settings

url = 'https://<< URL to Foxy >>/api'

class Customer(object):

    def get_hash(self, email, key):
        action = 'customer_get'
        params = urllib.urlencode ({ 
            'customer_email': email,
            'api_action': action,
            'api_token': key
        })
        data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(data)
        pwd_hash = xml.getElementsByTagName('customer_password')[0].firstChild.data
        return pwd_hash
        
    def get_cc_info(self, customer_id, key):
        action = 'customer_get'
        params = urllib.urlencode ({
            'customer_id': customer_id,
            'api_action': action,
            'api_token': key
        })
        data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(data)
        cc_number = xml.getElementsByTagName('cc_number')[0].firstChild.data
        cc_exp_month = xml.getElementsByTagName('cc_exp_month')[0].firstChild.data
        cc_exp_year = xml.getElementsByTagName('cc_exp_year')[0].firstChild.data
        cc_data = [cc_number, cc_exp_month, cc_exp_year]
        return cc_data
        
    def reset_password(self, data, customer_id, key):
        action = 'customer_save'
        url_params = {
            'customer_id': customer_id,
            'api_action': action,
            'api_token': key,
            'customer_password': data['password'],
        }
        params = urllib.urlencode (url_params)
        fc_data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(fc_data)
        status = xml.getElementsByTagName('result')[0].firstChild.data
        if status == 'SUCCESS':
            return True
        return False
    
    def update_user(self, data, customer_id, key):
        action = 'customer_save'
        url_params = {
            'customer_id': customer_id,
            'api_action': action,
            'api_token': key,
            'customer_email': data['username'],
        }
        if data['password1'] != '':
            url_params['customer_password'] = data['password1']
        params = urllib.urlencode(url_params)
        fc_data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(fc_data)
        status = xml.getElementsByTagName('result')[0].firstChild.data
        if status == 'SUCCESS':
            return True
        return False
        
    def check_cc_expiry(self, customer_id, key):
        action = 'customer_get'
        params = urllib.urlencode ({
            'customer_id': customer_id,
            'api_action': action,
            'api_token': key
        })
        data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(data)
        cc_exp_month = xml.getElementsByTagName('cc_exp_month')[0].firstChild.data
        cc_exp_year = xml.getElementsByTagName('cc_exp_year')[0].firstChild.data
        card_date = date(int(cc_exp_year), int(cc_exp_month), 1)
        today = date.today()
        target_date = date(today.year, today.month, 1) + timedelta(weeks=10)
        if card_date < target_date:
            return True
        return False
        
    def cancel_account(self, sub_token, key):
        action = 'subscription_cancel'
        params = urllib.urlencode ({
            'sub_token': sub_token,
            'api_action': action,
            'api_token': key
        })
        data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(data)
        result = xml.getElementsByTagName('result')[0].firstChild.data
        messages = xml.getElementsByTagName('messages')
        for message in messages:
            message = message.getElementsByTagName('message'
                                                        )[0].firstChild.data
        if result == 'SUCCESS':
            return result
        return message
        
    def get_subscription(self, sub_token, key):
        action = 'subscription_get'
        params = urllib.urlencode ({
            'sub_token': sub_token,
            'api_action': action,
            'api_token': key
        })
        data = urllib.urlopen(url, params).read()
        xml = minidom.parseString(data)
        result = xml.getElementsByTagName('result')[0].firstChild.data
        messages = xml.getElementsByTagName('messages')
        for message in messages:
            message = message.getElementsByTagName('message'
                                                        )[0].firstChild.data
        if result == 'SUCCESS':
            next_sub = xml.getElementsByTagName('next_transaction_date'
                                                        )[0].firstChild.data
            next_sub_date = datetime(*time.strptime(next_sub, '%Y-%m-%d')[0:6]).date()
            return True, next_sub_date
        return False, message
        