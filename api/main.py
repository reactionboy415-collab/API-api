from fastapi import FastAPI, HTTPException, Query
import requests
import random

app = FastAPI()

# 🔱 Security & Spoofing Config
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
    return {"status": "Online", "service": "Ultimate Key Intelligence API", "owner": "CHIRAGX9"}

@app.get("/get-key")
def get_detailed_key(key: str = Query(None)):
    # Authentication Check
    if key != AUTH_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized Access.")

    url = "https://api.unsecuredapikeys.com/API/GetRandomKey"
    
    try:
        res = requests.get(url, headers=get_spoofed_headers(), timeout=12)
        raw_data = res.json()
        
        # Decide which data source to use (Main or Fallback)
        is_fallback = "fallbackApiKey" in raw_data
        target = raw_data["fallbackApiKey"] if is_fallback else raw_data

        if target and "apiKey" in target:
            # Extracting Reference Info (Github details)
            ref = target.get("references", [{}])[0]
            
            return {
                "success": True,
                "engine_status": "Bypassed" if not is_fallback else "Fallback_Mode",
                "developer": "@dex4dev",
                "owner": "CHIRAGX9",
                "intel": {
                    "api_key": target.get("apiKey"),
                    "service": target.get("apiType"),
                    "key_status": target.get("status"),
                    "dates": {
                        "first_found": target.get("firstFoundUTC"),
                        "last_found": target.get("lastFoundUTC"),
                        "last_checked": target.get("lastCheckedUTC")
                    },
                    "metrics": {
                        "times_displayed": target.get("timesDisplayed"),
                        "error_count": target.get("errorCount")
                    },
                    "source_leak": {
                        "provider": ref.get("provider"),
                        "repo_name": ref.get("repoName"),
                        "repo_owner": ref.get("repoOwner"),
                        "repo_url": ref.get("repoURL"),
                        "file_name": ref.get("fileName"),
                        "file_path": ref.get("filePath"),
                        "leak_date": ref.get("foundUTC")
                    }
                }
            }
        
        return {"success": False, "message": "Zero results from upstream."}

    except Exception as e:
        return {"success": False, "error": str(e)}
