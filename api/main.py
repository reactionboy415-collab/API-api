from fastapi import FastAPI, HTTPException, Query
import requests
import random

app = FastAPI()

# Configuration
AUTH_KEY = "CHIRAGx9"
USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; LAVA Blaze) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.7559.59 Mobile Safari/537.36'
]

def get_spoofed_headers():
    fake_ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'X-Forwarded-For': fake_ip,
        'Origin': 'https://unsecuredapikeys.com',
        'Referer': 'https://unsecuredapikeys.com/',
        'X-Requested-With': 'mark.via.gp'
    }

@app.get("/")
def home():
    return {"status": "Online", "msg": "Use /get-key with auth"}

@app.get("/get-key")
def get_random_leaked_key(key: str = Query(None)):
    # 🔱 Authentication Check
    if key != AUTH_KEY:
        raise HTTPException(status_code=403, detail="Invalid Authentication Key. Access Denied.")

    url = "https://api.unsecuredapikeys.com/API/GetRandomKey"
    
    try:
        res = requests.get(url, headers=get_spoofed_headers(), timeout=10)
        data = res.json()
        
        # Logic: Extract Main Key or Fallback
        key_source = data if "apiKey" in data and "fallbackApiKey" not in data else data.get("fallbackApiKey")
        
        if key_source:
            return {
                "success": True,
                "developer": "@dex4dev",
                "owner": "CHIRAGX9",
                "data": {
                    "api_key": key_source.get("apiKey"),
                    "service": key_source.get("apiType"),
                    "status": key_source.get("status"),
                    "leak_source": key_source.get("references", [{}])[0].get("repoURL", "N/A"),
                    "last_checked": key_source.get("lastCheckedUTC")
                }
            }
        
        return {"success": False, "message": "Rate limit hit on source. Try again."}

    except Exception as e:
        return {"success": False, "error": str(e)}
