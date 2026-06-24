# sms_utils.py
# import requests
# from django.conf import settings


# def send_sms(to_number, message):
#     """BulkSMS BD দিয়ে SMS পাঠাও"""

#     # নম্বর format করো: 01712345678 → 8801712345678
#     number = to_number.strip().replace(' ', '').replace('-', '')
#     if number.startswith('0'):
#         number = '88' + number  # 01712... → 8801712...

#     url = "http://bulksmsbd.net/api/smsapi"

#     params = {
#         'api_key':  settings.BULKSMS_API_KEY,
#         'type':     'text',
#         'number':   number,
#         'senderid': settings.BULKSMS_SENDER_ID,
#         'message':  message,
#     }

#     try:
#         response = requests.get(url, params=params, timeout=10)
#         data = response.json()

#         if data.get('response_code') == 202:
#             print(f"✅ SMS sent to {number}")
#             return True
#         else:
#             print(f"❌ SMS failed: {data}")
#             return False

#     except Exception as e:
#         print(f"❌ SMS error: {e}")
#         return False


# def send_attendance_sms(student, status, date):
#     """Absent/Late guardian-কে notify করো"""

#     if status not in ('absent', 'late'):
#         return

#     status_text = "অনুপস্থিত" if status == 'absent' else "দেরিতে এসেছে"

#     message = (
#     f"প্রিয় অভিভাবক,\n\n"
#     f"আপনাকে জানানো যাচ্ছে যে আপনার সন্তান {student.full_name} "
#     f"আজ ({date.strftime('%d/%m/%Y')}) তার নির্ধারিত ক্লাসে {status_text}।\n\n"
#     f"ধন্যবাদান্তে,\n"
#     f"কর্ণফুলী বিজ্ঞান একাডেমি"
# )

#     if student.guardian_phone_1:
#         send_sms(student.guardian_phone_1, message)

#     if student.guardian_phone_2:
#         send_sms(student.guardian_phone_2, message)