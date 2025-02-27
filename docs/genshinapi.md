# Udpated 1/2024

il finish it with hsr endpoints within next few days

---
I dont have a cn account but these should work for other regions with their localisations
if you just replace en-us with a language that hoyo supports and os_asia should be replacable with os_euro, os_usa
china has its own extra headers for some of the endpoints so go to the bottom if you want to find how these were found

The larger schemas for battle chronical will probably be wrong as they get changed a lot,
for more accurate informaiton i suggest checking out the enka api or dims github

Anything labled with Battle Chronical comes form battle chonical, these ones are labeled since they a large amount of data.
Rest is mostly self explanitory

Code endpoints and sometimes login ones may return `-3101` this indicates a captcha and
data to solve the captcha will be in the header `x-rpc-aigis` if youre going this deep then
go thorugh most of the source of genshinpy that will give you a much better understanding on how to handle
resopnses

The primary cookies are `ltoken_v2`, `ltuid_v2`, `stoken`, `cookie_token_v2`. ltoken has
effectively infinite time before they expire, however this depends on account and for some people will expire
within a month and others it still works. A pattern is that when you dont request from the token for a while
it will expire. ltuid is a static value, linked to account. stoken should be a 1 year timeout, but cookietoken will expire
within a few days some say 24h but its worked longer for me. stoken is used to refresh ltoken and cookietoken

|Tokens|Beginning Characters|Type Number|
|--|--|--|
|ltoken_v2|v2_CAI|2|
|cookie_token_v2|v2_CAQ|4|
|stoken|v2_CAE|1|

---

## Table Of Contents

1. [Table Of Contents](#table-of-contents)
2. [General](#general)
   1. [Default headers for web endpoints](#default-headers-for-web-endpoints)
   2. [DS](#ds)
   3. [App Login](#app-login)
   4. [Refreshing Tokens](#refreshing-tokens)
   5. [Web Login](#web-login)
3. [Genshin](#genshin)
   1. [Genshin Live Notes](#genshin-live-notes)
   2. [Genshin Daily Rewards](#genshin-daily-rewards)
   3. [Genshin monthly primogems](#genshin-monthly-primogems)
   4. [Genshin events](#genshin-events)
   5. [Genshin Battle Chronical Characer](#genshin-battle-chronical-characer)
   6. [Genshin Battle Chronicals Index](#genshin-battle-chronicals-index)
   7. [Genshin Battle Chronical Activities](#genshin-battle-chronical-activities)
   8. [Genshin Battle Chronical Spiral Abyss](#genshin-battle-chronical-spiral-abyss)
   9. [Genshin banners](#genshin-banners)
   10. [Genshin Artifact Substats](#genshin-artifact-substats)
4. [HSR](#hsr)
   1. [HSR Live Notes](#hsr-live-notes)
   2. [HSR month prmios](#hsr-month-prmios)
   3. [How to find endpoints yourself](#how-to-find-endpoints-yourself)

---

## General

### Default headers for web endpoints

```
  "+ any user agent"
  "+ host, just point to base url"
```

### DS

Genshins dynamic secret for headers there is a web version and one for the app
the dynamic secret, the web version is used for endpoints that are on the web and app ...

|Salt Type| Salt Value|
|--|--|
|Web OS|6s25p5ox5y14umn1p61aqyyvbvvl3lrt|
|App OS|IZPgfb0dRPtBeLuFkdDznSZ6f4wWt6y2|

|App CN|not sure, how to potentially find will be at bottom|

```py
import time
import random
import hashlib
def generate_dynamic_secret(salt: str) -> str:
    """Create a new overseas dynamic secret."""
    t = int(time.time())
    r = "".join(random.choices(string.ascii_letters, k=6))
    h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
    return f"{t},{r},{h}"

```

```rust
use std::time::{SystemTime, UNIX_EPOCH}
use rand;
use md5;
fn generate_ds(ds_salt: String) -> String {
    let time: u64 = SystemTime::now()
        .duration_since(UNIX_EPOCH).expect("system time set to pre 1970")
        .as_secs();
    let random_string: String = rand::thread_rng()
        .sample_iter(&Alphanumeric)
        .take(6)
        .map(char::from)
        .collect();
    let hash = md5::compute(format!("salt={}&t={}&r={}", ds_salt, time, random_string));
    format!("{},{},{:x}", time, random_string, hash)
}
```

### App Login

I can actually explain how to get this since i found the method, granted its not complicated or protect
like the games communication🙏

The main purpose of this is to retrieve an `stoken` which can then be used to refresh `cookie_token_v2`
and `ltoken_v2` can return a captcha but in my experience aftr 20min it will go away and you dont need
to deal with the captcha again

Youre mainly looking at the token list for login itl return a token look at teh table from the beginning

```
  Method: Post
  base_url: "https://sg-public-api.hoyolab.com/account/ma-passport/api/appLoginByPassword"
```

|Headers|Value|
|--|--|
|Host|sg-public-api.hoyoverse.com|
|DS|app ds|
|x-rpc-game_biz|bbs_oversea|
|x-rpc-sdk_version|1.4.0|
|x-rpc-client_type|1|
|x-rpc-app_id|c9oqaq3s3gu8|

#### Payload

```json
{
  "account": (encrypted pass),
  "password": (encrypted pass)
}
```

#### App RSA Key

2 different formats, one with pyton another, a raw string

```py
HOYO_APP_RSA_PUBLIC = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4PMS2JVMwBsOIrYWRluY
wEiFZL7Aphtm9z5Eu/anzJ09nB00uhW+ScrDWFECPwpQto/GlOJYCUwVM/raQpAj
/xvcjK5tNVzzK94mhk+j9RiQ+aWHaTXmOgurhxSp3YbwlRDvOgcq5yPiTz0+kSeK
ZJcGeJ95bvJ+hJ/UMP0Zx2qB5PElZmiKvfiNqVUk8A8oxLJdBB5eCpqWV6CUqDKQ
KSQP4sM0mZvQ1Sr4UcACVcYgYnCbTZMWhJTWkrNXqI8TMomekgny3y+d6NX/cFa6
6jozFIF4HCX5aW8bp8C8vq2tFvFbleQ/Q3CU56EWWKMrOcpmFtRmC18s9biZBVR/
8QIDAQAB
-----END PUBLIC KEY-----
"""

```

```rust
pub const HOYO_APP_RSA_PUBLIC: &[u8; 450] = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArXCPrbEFo75elvyABdMX\nyRFC/FZAklYdvCPOV0YdOMWabNd7td4k08DeaZUji01u7vp/wX6EV8ainfZ/AVR5\nBD642Ab/bmrvVAJhKvXJEruGagm7jmGAeKnRI0hAjopDbj9PCzfDACkUbQOWVDpN\nFHYYN+pA0WEY7m491Chwo/JBjEfYi9VJdkjnr7VWVqokgwVe1LDkaGOW9Sso4dJO\nm5UaBZRGzXYDHe5u12J+v2PDGN1VkRT6VtytlL7n1JdG9m1uxM2KXjHreHaqYYay\n+XW3erdbpNQkZJEkgrcRR6MMNAIqzzO7EHqtOs+vxQyOW8rstK0nILAqgeVuF0x1\n1QIDAQAB\n-----END PUBLIC KEY-----";
```

#### Encryption Function

```py
def encrypt_geetest_password(text: str) -> str:
    """Encrypt text for geetest."""
    import rsa

    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(HOYO_APP_RSA_PUBLIC)
    crypto = rsa.encrypt(text.encode("utf-8"), public_key)
    return base64.b64encode(crypto).decode("utf-8")
```

```rust
use base64::prelude::BASE64_STANDARD;
use openssl::pkey::Public;
use openssl::rsa::{Padding, Rsa};

fn hoyo_encrypt(data: String) -> String {
    let public_key = net_constants::HOYO_APP_RSA_PUBLIC;

    let pem_public_key = Rsa::public_key_from_pem(public_key).unwrap();
    let mut buf: Vec<u8> = vec![0; pem_public_key.size() as usize];
    pem_public_key
        .public_encrypt(data.as_bytes(), &mut buf, Padding::PKCS1)
        .unwrap();

    BASE64_STANDARD.encode(&buf) 
}
```

#### Full Example

```py
import time
import random
import string
import hashlib
import base64
import requests

HOYO_APP_RSA_PUBLIC = b"""
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4PMS2JVMwBsOIrYWRluY
wEiFZL7Aphtm9z5Eu/anzJ09nB00uhW+ScrDWFECPwpQto/GlOJYCUwVM/raQpAj
/xvcjK5tNVzzK94mhk+j9RiQ+aWHaTXmOgurhxSp3YbwlRDvOgcq5yPiTz0+kSeK
ZJcGeJ95bvJ+hJ/UMP0Zx2qB5PElZmiKvfiNqVUk8A8oxLJdBB5eCpqWV6CUqDKQ
KSQP4sM0mZvQ1Sr4UcACVcYgYnCbTZMWhJTWkrNXqI8TMomekgny3y+d6NX/cFa6
6jozFIF4HCX5aW8bp8C8vq2tFvFbleQ/Q3CU56EWWKMrOcpmFtRmC18s9biZBVR/
8QIDAQAB
-----END PUBLIC KEY-----
"""


def generate_dynamic_secret(salt) -> str:
    """Create a new overseas dynamic secret."""
    t = int(time.time())
    r = "".join(random.choices(string.ascii_letters, k=6))
    h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
    return f"{t},{r},{h}"

def encrypt_geetest_password(text: str) -> str:
    """Encrypt text for geetest."""
    import rsa

    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(HOYO_APP_RSA_PUBLIC)
    crypto = rsa.encrypt(text.encode("utf-8"), public_key)
    return base64.b64encode(crypto).decode("utf-8")

HEADERS = {
    'User-Agent':'HoYoLAB/10 CFNetwork/1474 Darwin/23.0.0',
    'Host':'sg-public-api.hoyoverse.com',
    'x-rpc-sdk_version':'1.4.0',
    'DS':generate_dynamic_secret(salt),
    'x-rpc-game_biz':'bbs_oversea',
    'x-rpc-client_type':'1',
    'x-rpc-app_id':'c9oqaq3s3gu8',
}

payload = {
    "account": encrypt_geetest_password(account),
    "password": encrypt_geetest_password(password),
}

r = requests.post(
    "https://sg-public-api.hoyolab.com/account/ma-passport/api/appLoginByPassword",
    json=payload,
    headers=HEADERS,
)
print(r.json())
```

#### Returns

see bellow, same a refreshing tokens

### Refreshing Tokens

This endpoint gives you another `ltoken_v2` and `cookie_token_v2`, types 2 and 4 respectively
all you need to do is provide `stoken` and `mid`, which is `ltmid_v2` renamed

You can only send 4 and 2, any othe rnumber will return an error

```
  Method: Post
  base_url: https://sg-public-api.hoyoverse.com/account/ma-passport/token/getBySToken
```

|Cookie name|Cookie Value|
|--|--|
|mid|static tied to account|
|stoken|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|host isnt required||
|ds|app ds|
|x-rpc-app_id|c9oqaq3s3gu8|

#### Payload

```json
{
    "dst_token_types": [
        4,
        2
    ]
}


```

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "token": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "token_type": {
            "type": "number"
          },
          "token": {
            "type": "string"
          }
        },
        "required": [
          "token_type",
          "token"
        ]
      }
    },
    "user_info": {
      "type": "object",
      "properties": {
        "aid": {
          "type": "string"
        },
        "mid": {
          "type": "string"
        },
        "account_name": {
          "type": "string"
        },
        "email": {
          "type": "string"
        },
        "is_email_verify": {
          "type": "number"
        },
        "area_code": {
          "type": "string"
        },
        "mobile": {
          "type": "string"
        },
        "safe_area_code": {
          "type": "string"
        },
        "safe_mobile": {
          "type": "string"
        },
        "realname": {
          "type": "string"
        },
        "identity_code": {
          "type": "string"
        },
        "rebind_area_code": {
          "type": "string"
        },
        "rebind_mobile": {
          "type": "string"
        },
        "rebind_mobile_time": {
          "type": "string"
        },
        "links": {
          "type": "array",
          "items": {}
        },
        "country": {
          "type": "string"
        },
        "unmasked_email": {
          "type": "string"
        },
        "unmasked_email_type": {
          "type": "number"
        }
      },
      "required": [
        "aid",
        "mid",
        "account_name",
        "email",
        "is_email_verify",
        "area_code",
        "mobile",
        "safe_area_code",
        "safe_mobile",
        "realname",
        "identity_code",
        "rebind_area_code",
        "rebind_mobile",
        "rebind_mobile_time",
        "links",
        "country",
        "unmasked_email",
        "unmasked_email_type"
      ]
    },
    "ext_user_info": {
      "type": "object",
      "properties": {
        "guardian_email": {
          "type": "string"
        }
      },
      "required": [
        "guardian_email"
      ]
    },
    "reactivate_action_ticket": {
      "type": "string"
    },
    "bind_email_action_ticket": {
      "type": "string"
    }
  },
  "required": [
    "token",
    "user_info",
    "ext_user_info",
    "reactivate_action_ticket",
    "bind_email_action_ticket"
  ]
}
```

</details>

### Web Login

## Genshin

### Genshin Live Notes

provides live information on account, schema isnt long so look at it

```
  Method: Get
  base_url: https://sg-hk4e-api.hoyolab.com/event/sol/sign
```

|Parameter Name|Value|
|---|---|
|server|os_asia|
|role_id|(player uid)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "current_resin": {
      "type": "number"
    },
    "max_resin": {
      "type": "number"
    },
    "resin_recovery_time": {
      "type": "string"
    },
    "finished_task_num": {
      "type": "number"
    },
    "total_task_num": {
      "type": "number"
    },
    "is_extra_task_reward_received": {
      "type": "boolean"
    },
    "remain_resin_discount_num": {
      "type": "number"
    },
    "resin_discount_num_limit": {
      "type": "number"
    },
    "current_expedition_num": {
      "type": "number"
    },
    "max_expedition_num": {
      "type": "number"
    },
    "expeditions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_side_icon": {
            "type": "string"
          },
          "status": {
            "type": "string"
          },
          "remained_time": {
            "type": "string"
          }
        },
        "required": [
          "avatar_side_icon",
          "status",
          "remained_time"
        ]
      }
    },
    "current_home_coin": {
      "type": "number"
    },
    "max_home_coin": {
      "type": "number"
    },
    "home_coin_recovery_time": {
      "type": "string"
    },
    "calendar_url": {
      "type": "string"
    },
    "transformer": {
      "type": "object",
      "properties": {
        "obtained": {
          "type": "boolean"
        },
        "recovery_time": {
          "type": "object",
          "properties": {
            "Day": {
              "type": "number"
            },
            "Hour": {
              "type": "number"
            },
            "Minute": {
              "type": "number"
            },
            "Second": {
              "type": "number"
            },
            "reached": {
              "type": "boolean"
            }
          },
          "required": [
            "Day",
            "Hour",
            "Minute",
            "Second",
            "reached"
          ]
        },
        "wiki": {
          "type": "string"
        },
        "noticed": {
          "type": "boolean"
        },
        "latest_job_id": {
          "type": "string"
        }
      },
      "required": [
        "obtained",
        "recovery_time",
        "wiki",
        "noticed",
        "latest_job_id"
      ]
    },
    "daily_task": {
      "type": "object",
      "properties": {
        "total_num": {
          "type": "number"
        },
        "finished_num": {
          "type": "number"
        },
        "is_extra_task_reward_received": {
          "type": "boolean"
        },
        "task_rewards": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "status": {
                "type": "string"
              }
            },
            "required": [
              "status"
            ]
          }
        },
        "attendance_rewards": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "status": {
                "type": "string"
              },
              "progress": {
                "type": "number"
              }
            },
            "required": [
              "status",
              "progress"
            ]
          }
        },
        "attendance_visible": {
          "type": "boolean"
        }
      },
      "required": [
        "total_num",
        "finished_num",
        "is_extra_task_reward_received",
        "task_rewards",
        "attendance_rewards",
        "attendance_visible"
      ]
    },
    "archon_quest_progress": {
      "type": "object",
      "properties": {
        "list": {
          "type": "array",
          "items": {}
        },
        "is_open_archon_quest": {
          "type": "boolean"
        },
        "is_finish_all_mainline": {
          "type": "boolean"
        },
        "is_finish_all_interchapter": {
          "type": "boolean"
        },
        "wiki_url": {
          "type": "string"
        }
      },
      "required": [
        "list",
        "is_open_archon_quest",
        "is_finish_all_mainline",
        "is_finish_all_interchapter",
        "wiki_url"
      ]
    }
  },
  "required": [
    "current_resin",
    "max_resin",
    "resin_recovery_time",
    "finished_task_num",
    "total_task_num",
    "is_extra_task_reward_received",
    "remain_resin_discount_num",
    "resin_discount_num_limit",
    "current_expedition_num",
    "max_expedition_num",
    "expeditions",
    "current_home_coin",
    "max_home_coin",
    "home_coin_recovery_time",
    "calendar_url",
    "transformer",
    "daily_task",
    "archon_quest_progress"
  ]
}
```

</details>

### Genshin Daily Rewards

```
  2 separate urls, this one is for actual sign in
  Method: Post, no payload required
  base_url: https://sg-hk4e-api.hoyolab.com/event/sol/sign
  known to sometimes have captcha, return with have a cookie called x-rpc-aigis, contains shit on the captcha
  i forgot what it returns
```

|Parameter Name|Value|
|---|---|
|act_id|e202102251931481|
|lang|(whatever language)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

```
  second url gets data about sign in
  Method: Get
  base_url: https://sg-hk4e-api.hoyolab.com/event/sol/info
```

|Parameter Name|Value|
|---|---|
|act_id|e202102251931481|
|lang|(whatever language)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "total_sign_day": {
      "type": "number"
    },
    "today": {
      "type": "string"
    },
    "is_sign": {
      "type": "boolean"
    },
    "first_bind": {
      "type": "boolean"
    },
    "is_sub": {
      "type": "boolean"
    },
    "region": {
      "type": "string"
    },
    "month_last_day": {
      "type": "boolean"
    }
  },
  "required": [
    "total_sign_day",
    "today",
    "is_sign",
    "first_bind",
    "is_sub",
    "region",
    "month_last_day"
  ]
}
```

</details>

### Genshin monthly primogems

Just look at schema, not a long one, last is either last day for the day things or last month
for the month data

```
  Method: Get
  base_url: https://sg-hk4e-api.hoyolab.com/event/ysledgeros/month_info
```

|Parameter Name|Value|
|---|---|
|uid|DYNAMIC|
|region|(whatever region)|
|month|(month as int form 1-12)|
|lang|(whatever language)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "uid": {
      "type": "number"
    },
    "region": {
      "type": "string"
    },
    "nickname": {
      "type": "string"
    },
    "optional_month": {
      "type": "array",
      "items": {
        "type": "number"
      }
    },
    "month": {
      "type": "number"
    },
    "data_month": {
      "type": "number"
    },
    "month_data": {
      "type": "object",
      "properties": {
        "current_primogems": {
          "type": "number"
        },
        "current_mora": {
          "type": "number"
        },
        "last_primogems": {
          "type": "number"
        },
        "last_mora": {
          "type": "number"
        },
        "primogem_rate": {
          "type": "number"
        },
        "mora_rate": {
          "type": "number"
        },
        "group_by": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "action_id": {
                "type": "number"
              },
              "action": {
                "type": "string"
              },
              "num": {
                "type": "number"
              },
              "percent": {
                "type": "number"
              }
            },
            "required": [
              "action_id",
              "action",
              "num",
              "percent"
            ]
          }
        }
      },
      "required": [
        "current_primogems",
        "current_mora",
        "last_primogems",
        "last_mora",
        "primogem_rate",
        "mora_rate",
        "group_by"
      ]
    },
    "day_data": {
      "type": "object",
      "properties": {
        "current_primogems": {
          "type": "number"
        },
        "current_mora": {
          "type": "number"
        }
      },
      "required": [
        "current_primogems",
        "current_mora"
      ]
    }
  },
  "required": [
    "uid",
    "region",
    "nickname",
    "optional_month",
    "month",
    "data_month",
    "month_data",
    "day_data"
  ]
}
```

</details>

### Genshin events

contains currently ongoing event data, actual data from [this site](https://webstatic-sea.mihoyo.com/hk4e/announcement/index.html?auth_appid=announcement&bundle_id=hk4e_global&game=hk4e&game_biz=hk4e_global&lang=en&level=60&platform=pc&region=os_euro&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&uid=99999999#/)

```
    Method: Get
    base_url: https://sg-hk4e-api.hoyoverse.com/common/hk4e_global/announcement/api/getAnnList?game=hk4e&game_biz=hk4e_global&lang=en&auth_appid=announcement&bundle_id=hk4e_global&level=60&platform=pc&region=os_euro&sdk_presentation_style=fullscreen&sdk_screen_transparent=true&uid=99999999
```

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "list": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "ann_id": {
                  "type": "number"
                },
                "title": {
                  "type": "string"
                },
                "subtitle": {
                  "type": "string"
                },
                "banner": {
                  "type": "string"
                },
                "content": {
                  "type": "string"
                },
                "type_label": {
                  "type": "string"
                },
                "tag_label": {
                  "type": "string"
                },
                "tag_icon": {
                  "type": "string"
                },
                "login_alert": {
                  "type": "number"
                },
                "lang": {
                  "type": "string"
                },
                "start_time": {
                  "type": "string"
                },
                "end_time": {
                  "type": "string"
                },
                "type": {
                  "type": "number"
                },
                "remind": {
                  "type": "number"
                },
                "alert": {
                  "type": "number"
                },
                "tag_start_time": {
                  "type": "string"
                },
                "tag_end_time": {
                  "type": "string"
                },
                "remind_ver": {
                  "type": "number"
                },
                "has_content": {
                  "type": "boolean"
                },
                "extra_remind": {
                  "type": "number"
                },
                "tag_icon_hover": {
                  "type": "string"
                }
              },
              "required": [
                "ann_id",
                "title",
                "subtitle",
                "banner",
                "content",
                "type_label",
                "tag_label",
                "tag_icon",
                "login_alert",
                "lang",
                "start_time",
                "end_time",
                "type",
                "remind",
                "alert",
                "tag_start_time",
                "tag_end_time",
                "remind_ver",
                "has_content",
                "extra_remind",
                "tag_icon_hover"
              ]
            }
          },
          "type_id": {
            "type": "number"
          },
          "type_label": {
            "type": "string"
          }
        },
        "required": [
          "list",
          "type_id",
          "type_label"
        ]
      }
    },
    "total": {
      "type": "number"
    },
    "type_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number"
          },
          "name": {
            "type": "string"
          },
          "mi18n_name": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name",
          "mi18n_name"
        ]
      }
    },
    "alert": {
      "type": "boolean"
    },
    "alert_id": {
      "type": "number"
    },
    "timezone": {
      "type": "number"
    },
    "t": {
      "type": "string"
    },
    "pic_list": {
      "type": "array",
      "items": {}
    },
    "pic_total": {
      "type": "number"
    },
    "pic_type_list": {
      "type": "array",
      "items": {}
    },
    "pic_alert": {
      "type": "boolean"
    },
    "pic_alert_id": {
      "type": "number"
    },
    "static_sign": {
      "type": "string"
    }
  },
  "required": [
    "list",
    "total",
    "type_list",
    "alert",
    "alert_id",
    "timezone",
    "t",
    "pic_list",
    "pic_total",
    "pic_type_list",
    "pic_alert",
    "pic_alert_id",
    "static_sign"
  ]
}
```

</details>

### Genshin Battle Chronical Characer

exact same character data as in index, but now there is which artifact(no substat)
, weapon and constellation names

```
    Method: Post
    base_url: https://bbs-api-os.hoyolab.com/game_record/genshin/api/character
    requires json payload
```

#### Returns

```json
{
    "server": region(os_asia),
    "role_id": (player uid)
}
```

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "role": {
      "type": "object",
      "properties": {
        "AvatarUrl": {
          "type": "string"
        },
        "nickname": {
          "type": "string"
        },
        "region": {
          "type": "string"
        },
        "level": {
          "type": "number"
        },
        "game_head_icon": {
          "type": "string"
        }
      },
      "required": [
        "AvatarUrl",
        "nickname",
        "region",
        "level",
        "game_head_icon"
      ]
    },
    "avatars": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "number"
          },
          "image": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "element": {
            "type": "string"
          },
          "fetter": {
            "type": "number"
          },
          "level": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          },
          "actived_constellation_num": {
            "type": "number"
          },
          "card_image": {
            "type": "string"
          },
          "is_chosen": {
            "type": "boolean"
          }
        },
        "required": [
          "id",
          "image",
          "name",
          "element",
          "fetter",
          "level",
          "rarity",
          "actived_constellation_num",
          "card_image",
          "is_chosen"
        ]
      }
    },
    "stats": {
      "type": "object",
      "properties": {
        "active_day_number": {
          "type": "number"
        },
        "achievement_number": {
          "type": "number"
        },
        "anemoculus_number": {
          "type": "number"
        },
        "geoculus_number": {
          "type": "number"
        },
        "avatar_number": {
          "type": "number"
        },
        "way_point_number": {
          "type": "number"
        },
        "domain_number": {
          "type": "number"
        },
        "spiral_abyss": {
          "type": "string"
        },
        "precious_chest_number": {
          "type": "number"
        },
        "luxurious_chest_number": {
          "type": "number"
        },
        "exquisite_chest_number": {
          "type": "number"
        },
        "common_chest_number": {
          "type": "number"
        },
        "electroculus_number": {
          "type": "number"
        },
        "magic_chest_number": {
          "type": "number"
        },
        "dendroculus_number": {
          "type": "number"
        },
        "hydroculus_number": {
          "type": "number"
        },
        "field_ext_map": {
          "type": "object",
          "properties": {
            "hydroculus_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "luxurious_chest_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "magic_chest_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "spiral_abyss": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "common_chest_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "electroculus_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "anemoculus_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "exquisite_chest_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "avatar_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "domain_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "geoculus_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "precious_chest_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "dendroculus_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            },
            "way_point_number": {
              "type": "object",
              "properties": {
                "link": {
                  "type": "string"
                },
                "backup_link": {
                  "type": "string"
                }
              },
              "required": [
                "link",
                "backup_link"
              ]
            }
          },
          "required": [
            "hydroculus_number",
            "luxurious_chest_number",
            "magic_chest_number",
            "spiral_abyss",
            "common_chest_number",
            "electroculus_number",
            "anemoculus_number",
            "exquisite_chest_number",
            "avatar_number",
            "domain_number",
            "geoculus_number",
            "precious_chest_number",
            "dendroculus_number",
            "way_point_number"
          ]
        }
      },
      "required": [
        "active_day_number",
        "achievement_number",
        "anemoculus_number",
        "geoculus_number",
        "avatar_number",
        "way_point_number",
        "domain_number",
        "spiral_abyss",
        "precious_chest_number",
        "luxurious_chest_number",
        "exquisite_chest_number",
        "common_chest_number",
        "electroculus_number",
        "magic_chest_number",
        "dendroculus_number",
        "hydroculus_number",
        "field_ext_map"
      ]
    },
    "city_explorations": {
      "type": "array",
      "items": {}
    },
    "world_explorations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": {
            "type": "number"
          },
          "exploration_percentage": {
            "type": "number"
          },
          "icon": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "type": {
            "type": "string"
          },
          "offerings": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "level": {
                  "type": "number"
                },
                "icon": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "level",
                "icon"
              ]
            }
          },
          "id": {
            "type": "number"
          },
          "parent_id": {
            "type": "number"
          },
          "map_url": {
            "type": "string"
          },
          "strategy_url": {
            "type": "string"
          },
          "background_image": {
            "type": "string"
          },
          "inner_icon": {
            "type": "string"
          },
          "cover": {
            "type": "string"
          },
          "area_exploration_list": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "exploration_percentage": {
                  "type": "number"
                }
              },
              "required": [
                "name",
                "exploration_percentage"
              ]
            }
          },
          "boss_list": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "kill_num": {
                  "type": "number"
                }
              },
              "required": [
                "name",
                "kill_num"
              ]
            }
          },
          "is_hot": {
            "type": "boolean"
          }
        },
        "required": [
          "level",
          "exploration_percentage",
          "icon",
          "name",
          "type",
          "offerings",
          "id",
          "parent_id",
          "map_url",
          "strategy_url",
          "background_image",
          "inner_icon",
          "cover",
          "area_exploration_list",
          "boss_list",
          "is_hot"
        ]
      }
    },
    "homes": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "level": {
            "type": "number"
          },
          "visit_num": {
            "type": "number"
          },
          "comfort_num": {
            "type": "number"
          },
          "item_num": {
            "type": "number"
          },
          "name": {
            "type": "string"
          },
          "icon": {
            "type": "string"
          },
          "comfort_level_name": {
            "type": "string"
          },
          "comfort_level_icon": {
            "type": "string"
          }
        },
        "required": [
          "level",
          "visit_num",
          "comfort_num",
          "item_num",
          "name",
          "icon",
          "comfort_level_name",
          "comfort_level_icon"
        ]
      }
    },
    "query_tool_link": {
      "type": "string"
    },
    "query_tool_image": {
      "type": "string"
    }
  },
  "required": [
    "role",
    "avatars",
    "stats",
    "city_explorations",
    "world_explorations",
    "homes",
    "query_tool_link",
    "query_tool_image"
  ]
}
```

</details>

### Genshin Battle Chronicals Index

Contains data like character avatar and basic information on the characters,
serenitea pot data, world exploration, misc stats like days played
**THIS SCHEMA PROBABLY ISNT COMPLETE**

```
    Method: Get
    base_url: https://bbs-api-os.hoyolab.com/game_record/genshin/api/index
```

|Parameter Name|Value|
|---|---|
|server|region(os_asia)|
|role_id|(player uid)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/schema#",
  "type": "object",
  "properties": {
    "retcode": {
      "type": "integer"
    },
    "message": {
      "type": "string"
    },
    "data": {
      "type": "object",
      "properties": {
        "role": {
          "type": "object",
          "properties": {
            "AvatarUrl": {
              "type": "string"
            },
            "nickname": {
              "type": "string"
            },
            "region": {
              "type": "string"
            },
            "level": {
              "type": "integer"
            },
            "game_head_icon": {
              "type": "string"
            }
          },
          "required": [
            "AvatarUrl",
            "game_head_icon",
            "level",
            "nickname",
            "region"
          ]
        },
        "avatars": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "image": {
                "type": "string"
              },
              "name": {
                "type": "string"
              },
              "element": {
                "type": "string"
              },
              "fetter": {
                "type": "integer"
              },
              "level": {
                "type": "integer"
              },
              "rarity": {
                "type": "integer"
              },
              "actived_constellation_num": {
                "type": "integer"
              },
              "card_image": {
                "type": "string"
              },
              "is_chosen": {
                "type": "boolean"
              }
            },
            "required": [
              "actived_constellation_num",
              "card_image",
              "element",
              "fetter",
              "id",
              "image",
              "is_chosen",
              "level",
              "name",
              "rarity"
            ]
          }
        },
        "stats": {
          "type": "object",
          "properties": {
            "active_day_number": {
              "type": "integer"
            },
            "achievement_number": {
              "type": "integer"
            },
            "anemoculus_number": {
              "type": "integer"
            },
            "geoculus_number": {
              "type": "integer"
            },
            "avatar_number": {
              "type": "integer"
            },
            "way_point_number": {
              "type": "integer"
            },
            "domain_number": {
              "type": "integer"
            },
            "spiral_abyss": {
              "type": "string"
            },
            "precious_chest_number": {
              "type": "integer"
            },
            "luxurious_chest_number": {
              "type": "integer"
            },
            "exquisite_chest_number": {
              "type": "integer"
            },
            "common_chest_number": {
              "type": "integer"
            },
            "electroculus_number": {
              "type": "integer"
            },
            "magic_chest_number": {
              "type": "integer"
            },
            "dendroculus_number": {
              "type": "integer"
            },
            "hydroculus_number": {
              "type": "integer"
            },
            "field_ext_map": {
              "type": "object",
              "properties": {
                "dendroculus_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "geoculus_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "hydroculus_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "domain_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "way_point_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "precious_chest_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "common_chest_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "luxurious_chest_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "electroculus_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "anemoculus_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "spiral_abyss": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "exquisite_chest_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "magic_chest_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                },
                "avatar_number": {
                  "type": "object",
                  "properties": {
                    "link": {
                      "type": "string"
                    },
                    "backup_link": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "backup_link",
                    "link"
                  ]
                }
              },
              "required": [
                "anemoculus_number",
                "avatar_number",
                "common_chest_number",
                "dendroculus_number",
                "domain_number",
                "electroculus_number",
                "exquisite_chest_number",
                "geoculus_number",
                "hydroculus_number",
                "luxurious_chest_number",
                "magic_chest_number",
                "precious_chest_number",
                "spiral_abyss",
                "way_point_number"
              ]
            }
          },
          "required": [
            "achievement_number",
            "active_day_number",
            "anemoculus_number",
            "avatar_number",
            "common_chest_number",
            "dendroculus_number",
            "domain_number",
            "electroculus_number",
            "exquisite_chest_number",
            "field_ext_map",
            "geoculus_number",
            "hydroculus_number",
            "luxurious_chest_number",
            "magic_chest_number",
            "precious_chest_number",
            "spiral_abyss",
            "way_point_number"
          ]
        },
        "city_explorations": {
          "type": "array"
        },
        "world_explorations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "level": {
                "type": "integer"
              },
              "exploration_percentage": {
                "type": "integer"
              },
              "icon": {
                "type": "string"
              },
              "name": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "offerings": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "level": {
                      "type": "integer"
                    },
                    "icon": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "icon",
                    "level",
                    "name"
                  ]
                }
              },
              "id": {
                "type": "integer"
              },
              "parent_id": {
                "type": "integer"
              },
              "map_url": {
                "type": "string"
              },
              "strategy_url": {
                "type": "string"
              },
              "background_image": {
                "type": "string"
              },
              "inner_icon": {
                "type": "string"
              },
              "cover": {
                "type": "string"
              },
              "area_exploration_list": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "exploration_percentage": {
                      "type": "integer"
                    }
                  },
                  "required": [
                    "exploration_percentage",
                    "name"
                  ]
                }
              },
              "boss_list": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string"
                    },
                    "kill_num": {
                      "type": "integer"
                    }
                  },
                  "required": [
                    "kill_num",
                    "name"
                  ]
                }
              },
              "is_hot": {
                "type": "boolean"
              }
            },
            "required": [
              "area_exploration_list",
              "background_image",
              "boss_list",
              "cover",
              "exploration_percentage",
              "icon",
              "id",
              "inner_icon",
              "is_hot",
              "level",
              "map_url",
              "name",
              "offerings",
              "parent_id",
              "strategy_url",
              "type"
            ]
          }
        },
        "homes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "level": {
                "type": "integer"
              },
              "visit_num": {
                "type": "integer"
              },
              "comfort_num": {
                "type": "integer"
              },
              "item_num": {
                "type": "integer"
              },
              "name": {
                "type": "string"
              },
              "icon": {
                "type": "string"
              },
              "comfort_level_name": {
                "type": "string"
              },
              "comfort_level_icon": {
                "type": "string"
              }
            },
            "required": [
              "comfort_level_icon",
              "comfort_level_name",
              "comfort_num",
              "icon",
              "item_num",
              "level",
              "name",
              "visit_num"
            ]
          }
        },
        "query_tool_link": {
          "type": "string"
        },
        "query_tool_image": {
          "type": "string"
        }
      },
      "required": [
        "avatars",
        "city_explorations",
        "homes",
        "query_tool_image",
        "query_tool_link",
        "role",
        "stats",
        "world_explorations"
      ]
    }
  },
  "required": [
    "data",
    "message",
    "retcode"
  ]
}
```

</details>

### Genshin Battle Chronical Activities

Has event participation data
**THIS SCHEMA IS 2000 lines long and is probably updated per event so no point providing**

```
    Method: Get
    base_url: https://bbs-api-os.hoyolab.com/game_record/genshin/api/activities
```

|Parameter Name|Value|
|---|---|
|server|region(os_asia)|
|role_id|(player uid)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

### Genshin Battle Chronical Spiral Abyss

data from spiral abyss

```
    Method: Get
    base_url: https://bbs-api-os.hoyolab.com/game_record/genshin/api/spiralAbyss
```

schedule_type can be either 1 or 2, 1 refers to current abyss, 2 is previous

|Parameter Name|Value|
|---|---|
|server|region(os_asia)|
|role_id|(player uid)|
|schedule_type|1 or 2 read above|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "schedule_id": {
      "type": "number"
    },
    "start_time": {
      "type": "string"
    },
    "end_time": {
      "type": "string"
    },
    "total_battle_times": {
      "type": "number"
    },
    "total_win_times": {
      "type": "number"
    },
    "max_floor": {
      "type": "string"
    },
    "reveal_rank": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_id": {
            "type": "number"
          },
          "avatar_icon": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          }
        },
        "required": [
          "avatar_id",
          "avatar_icon",
          "value",
          "rarity"
        ]
      }
    },
    "defeat_rank": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_id": {
            "type": "number"
          },
          "avatar_icon": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          }
        },
        "required": [
          "avatar_id",
          "avatar_icon",
          "value",
          "rarity"
        ]
      }
    },
    "damage_rank": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_id": {
            "type": "number"
          },
          "avatar_icon": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          }
        },
        "required": [
          "avatar_id",
          "avatar_icon",
          "value",
          "rarity"
        ]
      }
    },
    "take_damage_rank": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_id": {
            "type": "number"
          },
          "avatar_icon": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          }
        },
        "required": [
          "avatar_id",
          "avatar_icon",
          "value",
          "rarity"
        ]
      }
    },
    "normal_skill_rank": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_id": {
            "type": "number"
          },
          "avatar_icon": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          }
        },
        "required": [
          "avatar_id",
          "avatar_icon",
          "value",
          "rarity"
        ]
      }
    },
    "energy_skill_rank": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "avatar_id": {
            "type": "number"
          },
          "avatar_icon": {
            "type": "string"
          },
          "value": {
            "type": "number"
          },
          "rarity": {
            "type": "number"
          }
        },
        "required": [
          "avatar_id",
          "avatar_icon",
          "value",
          "rarity"
        ]
      }
    },
    "floors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "index": {
            "type": "number"
          },
          "icon": {
            "type": "string"
          },
          "is_unlock": {
            "type": "boolean"
          },
          "settle_time": {
            "type": "string"
          },
          "star": {
            "type": "number"
          },
          "max_star": {
            "type": "number"
          },
          "levels": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "index": {
                  "type": "number"
                },
                "star": {
                  "type": "number"
                },
                "max_star": {
                  "type": "number"
                },
                "battles": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "index": {
                        "type": "number"
                      },
                      "timestamp": {
                        "type": "string"
                      },
                      "avatars": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "number"
                            },
                            "icon": {
                              "type": "string"
                            },
                            "level": {
                              "type": "number"
                            },
                            "rarity": {
                              "type": "number"
                            }
                          },
                          "required": [
                            "id",
                            "icon",
                            "level",
                            "rarity"
                          ]
                        }
                      },
                      "settle_date_time": {
                        "type": "object",
                        "properties": {
                          "year": {
                            "type": "number"
                          },
                          "month": {
                            "type": "number"
                          },
                          "day": {
                            "type": "number"
                          },
                          "hour": {
                            "type": "number"
                          },
                          "minute": {
                            "type": "number"
                          },
                          "second": {
                            "type": "number"
                          }
                        },
                        "required": [
                          "year",
                          "month",
                          "day",
                          "hour",
                          "minute",
                          "second"
                        ]
                      }
                    },
                    "required": [
                      "index",
                      "timestamp",
                      "avatars",
                      "settle_date_time"
                    ]
                  }
                },
                "top_half_floor_monster": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "icon": {
                        "type": "string"
                      },
                      "level": {
                        "type": "number"
                      }
                    },
                    "required": [
                      "name",
                      "icon",
                      "level"
                    ]
                  }
                },
                "bottom_half_floor_monster": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "icon": {
                        "type": "string"
                      },
                      "level": {
                        "type": "number"
                      }
                    },
                    "required": [
                      "name",
                      "icon",
                      "level"
                    ]
                  }
                }
              },
              "required": [
                "index",
                "star",
                "max_star",
                "battles",
                "top_half_floor_monster",
                "bottom_half_floor_monster"
              ]
            }
          },
          "settle_date_time": {},
          "ley_line_disorder": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "index",
          "icon",
          "is_unlock",
          "settle_time",
          "star",
          "max_star",
          "levels",
          "settle_date_time",
          "ley_line_disorder"
        ]
      }
    },
    "total_star": {
      "type": "number"
    },
    "is_unlock": {
      "type": "boolean"
    }
  },
  "required": [
    "schedule_id",
    "start_time",
    "end_time",
    "total_battle_times",
    "total_win_times",
    "max_floor",
    "reveal_rank",
    "defeat_rank",
    "damage_rank",
    "take_damage_rank",
    "normal_skill_rank",
    "energy_skill_rank",
    "floors",
    "total_star",
    "is_unlock"
  ]
}
```

</details>

### Genshin banners

This endpoint has 2 urls, 1 to get list, and another to get teh actual banner info, i recommend not using this
as this endpoint was changed at the beginning of 4.0 where the list url no longer got updated
this broke the actual gacha information until someone randomly found it again by guessing
for now though the list is updated, another way to get banner info which i recommended using
[genshin events api](#genevents)

```
    neither have and special headers
    id list endpoint
    Method: Get
    base_url: https://operation-webstatic.mihoyo.com/gacha_info/hk4e/cn_gf01/gacha/list.json
```

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "data": {
      "type": "object",
      "properties": {
        "list": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "begin_time": {
                "type": "string"
              },
              "end_time": {
                "type": "string"
              },
              "gacha_id": {
                "type": "string"
              },
              "gacha_name": {
                "type": "string"
              },
              "gacha_type": {
                "type": "number"
              }
            },
            "required": [
              "begin_time",
              "end_time",
              "gacha_id",
              "gacha_name",
              "gacha_type"
            ]
          }
        }
      },
      "required": [
        "list"
      ]
    },
    "message": {
      "type": "string"
    },
    "retcode": {
      "type": "number"
    }
  },
  "required": [
    "data",
    "message",
    "retcode"
  ]
}
```

</details>

```
    where {gacha_id} put id you got from the list above
    looks like: "gacha_id":"7cd22d479503bd9c47816a6c9a73aaac3613f61c"

    Method: Get
    base_url: https://operation-webstatic.hoyoverse.com/gacha_info/hk4e/os_asia/{gacha_id}/en-us.json
```

#### Returns

<details>

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "banner": {
      "type": "string"
    },
    "content": {
      "type": "string"
    },
    "date_range": {
      "type": "string"
    },
    "gacha_type": {
      "type": "number"
    },
    "r3_baodi_prob": {
      "type": "string"
    },
    "r3_prob": {
      "type": "string"
    },
    "r3_prob_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "is_up": {
            "type": "number"
          },
          "item_id": {
            "type": "number"
          },
          "item_name": {
            "type": "string"
          },
          "item_type": {
            "type": "string"
          },
          "order_value": {
            "type": "number"
          },
          "rank": {
            "type": "number"
          }
        },
        "required": [
          "is_up",
          "item_id",
          "item_name",
          "item_type",
          "order_value",
          "rank"
        ]
      }
    },
    "r4_baodi_prob": {
      "type": "string"
    },
    "r4_prob": {
      "type": "string"
    },
    "r4_prob_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "is_up": {
            "type": "number"
          },
          "item_id": {
            "type": "number"
          },
          "item_name": {
            "type": "string"
          },
          "item_type": {
            "type": "string"
          },
          "order_value": {
            "type": "number"
          },
          "rank": {
            "type": "number"
          }
        },
        "required": [
          "is_up",
          "item_id",
          "item_name",
          "item_type",
          "order_value",
          "rank"
        ]
      }
    },
    "r4_up_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_attr": {
            "type": "string"
          },
          "item_color": {
            "type": "string"
          },
          "item_id": {
            "type": "number"
          },
          "item_img": {
            "type": "string"
          },
          "item_name": {
            "type": "string"
          },
          "item_type": {
            "type": "string"
          },
          "item_type_cn": {
            "type": "string"
          }
        },
        "required": [
          "item_attr",
          "item_color",
          "item_id",
          "item_img",
          "item_name",
          "item_type",
          "item_type_cn"
        ]
      }
    },
    "r4_up_prob": {
      "type": "string"
    },
    "r5_baodi_prob": {
      "type": "string"
    },
    "r5_prob": {
      "type": "string"
    },
    "r5_prob_list": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "is_up": {
            "type": "number"
          },
          "item_id": {
            "type": "number"
          },
          "item_name": {
            "type": "string"
          },
          "item_type": {
            "type": "string"
          },
          "order_value": {
            "type": "number"
          },
          "rank": {
            "type": "number"
          }
        },
        "required": [
          "is_up",
          "item_id",
          "item_name",
          "item_type",
          "order_value",
          "rank"
        ]
      }
    },
    "r5_up_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_attr": {
            "type": "string"
          },
          "item_color": {
            "type": "string"
          },
          "item_id": {
            "type": "number"
          },
          "item_img": {
            "type": "string"
          },
          "item_name": {
            "type": "string"
          },
          "item_type": {
            "type": "string"
          },
          "item_type_cn": {
            "type": "string"
          }
        },
        "required": [
          "item_attr",
          "item_color",
          "item_id",
          "item_img",
          "item_name",
          "item_type",
          "item_type_cn"
        ]
      }
    },
    "r5_up_prob": {
      "type": "string"
    },
    "title": {
      "type": "string"
    }
  },
  "required": [
    "banner",
    "content",
    "date_range",
    "gacha_type",
    "r3_baodi_prob",
    "r3_prob",
    "r3_prob_list",
    "r4_baodi_prob",
    "r4_prob",
    "r4_prob_list",
    "r4_up_items",
    "r4_up_prob",
    "r5_baodi_prob",
    "r5_prob",
    "r5_prob_list",
    "r5_up_items",
    "r5_up_prob",
    "title"
  ]
}
```

</details>

### Genshin Artifact Substats

Currently not in hoyoapi however, as of 06/02/2024 HSR has implemented a way to get substats throughh the battle chornical equivalent in Hoyolab. For now the only alternative is either the enka api or mihomo

## HSR

Mostly the smae as genshin, except for notes, that one is more complicated and as of 06/02/2024 they have artifact substats for everyone 🎉

### HSR Live Notes

provides live information on account, schema isnt long so look at it

```
    Method: Get
    base_url: https://sg-hk4e-api.hoyolab.com/event/sol/sign
```

|Parameter Name|Value|
|---|---|
|server|os_asia|
|role_id|(player uid)|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

### HSR month prmios

this is the only endpoint other than codes that requires cookie_token_v2

```
    Method: Get
    base_url: https://sg-public-api.hoyolab.com/event/srledger/month_info?uid={uid}&region=prod_official_asia&month=202312&lang=en-us
```

|Parameter Name|Value|
|---|---|
|server|region(os_asia)|
|role_id|(player uid)|
|schedule_type|1 or 2 read above|

|Cookie name|Cookie Value|
|--|--|
|ltoken_v2|DYNAMIC|
|ltuid_v2|DYNAMIC|

|Extra Header Name|Value|
|--|--|
|ds|web ds|
|x-rpc-app-version|1.5.0|
|x-rpc-client_type|5|
|x-rpc-language|en-us|

### How to find endpoints yourself

literally just go to a place where you can see the data you want and f12
then go to tet box called filter, that searches all network traffic that you have selected(default all)
it i honestly cant say more
search for headings in hte data you want or specific values eg if it says
data = 124 search 124
