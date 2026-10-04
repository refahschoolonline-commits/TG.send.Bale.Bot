import time
import requests

# اطلاعات تلگرام
TELEGRAM_TOKEN = "GAPGPTMASKTOKENizc7vjw7b5X0X"
TG_SOURCE_CHAT_ID = -1002345678901   # شناسه گروه تلگرام
TARGET_TOPIC_ID = 42                 # شناسه تاپیک

# اطلاعات بله
BALE_TOKEN = "GAPGPTMASKTOKENizc7vjw7b5X1X"
BALE_CHAT_ID = "5043541096"          # شناسه بله

TG_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
BALE_URL = f"https://tapi.bale.ai/bot{BALE_TOKEN}/sendMessage"

last_update_id = 0
print(f"پل ارتباطی تاپیک {TARGET_TOPIC_ID} تلگرام به بله فعال شد...")

while True:
    try:
        response = requests.get(
            f"{TG_URL}/getUpdates",
            params={"offset": last_update_id + 1, "timeout": 20}
        ).json()
        
        if response.get("ok"):
            for update in response.get("result", []):
                last_update_id = update["update_id"]
                
                message = update.get("message")
                if not message:
                    continue
                
                chat_id = message.get("chat", {}).get("id")
                thread_id = message.get("message_thread_id")
                
                if chat_id == TG_SOURCE_CHAT_ID and thread_id == TARGET_TOPIC_ID:
                    text = message.get("text")
                    sender_name = message.get("from", {}).get("first_name", "کاربر")
                    
                    if text:
                        payload = {
                            "chat_id": BALE_CHAT_ID,
                            "text": f"📩 **{sender_name}** در تلگرام:\n\n{text}"
                        }
                        requests.post(BALE_URL, json=payload, timeout=10)
                        print(f"پیام از {sender_name} ارسال شد.")
                        
    except Exception as e:
        print(f"خطا: {e}")
        time.sleep(3)
