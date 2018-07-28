Chatting Service, 이은서
=========================

Directory
--------------------
* hyper_chat/
  * manage.py
  * requirements.txt
  * README.md
  * Procfile
  * api/
    * \_\_init\_\_.py
    * admin.py
    * apps.py
    * crontab_jobs.py
    * models.py
    * serializers.py
    * urls.py
    * apis/
      * \_\_init\_\_.py
      * api_chat.py
      * api_chatroom.py
      * api_chatter.py
    * tests/
      * \_\_init\_\_.py
      * test_chat.py
      * test_chatroom.py
      * test_chatter.py
      * tests.py
  * chats/
    * \_\_init\_\_.py
    * apps.py
    * consumers.py
    * custom_websocket_communicator.py
    * redis_connect.py
    * routing.py
    * tests.py
  * hyper_chat/
    * \_\_init\_\_.py
    * asgi.py
    * celery.py
    * routing.py
    * settings.py
    * token_auth.py
    * urls.py
    * wsgi.py

API Docs
-------------------
[/api/auth](#apiauth)<br/>
[/api/chatters](#apichatters)<br/>
[/api/chatters/{chatter_id}](#apichatterschatter_id)<br/>
[/api/chatrooms](#apichatrooms)<br/>
[/api/chatrooms/{chatroom_id}](#apichatroomschatroom_id)<br/>
[/api/chatrooms/{chatroom_id}/chats](#apichatroomschatroom_idchats)<br/>
[/api/chatrooms/{chatroom_id}/chats/search](#apichatroomschatroom_idchatssearch)<br/>
[/api/chats/{chat_id}](#apichatschat_id)<br/>

## /api/auth
#### -POST
Sign in

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |

**request (param)**
```
{
  "username": String,
  "password": String
}
```

**response**
```
{
  "token": String
}
```

## /api/chatters
#### -GET
Get all chat users info

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |

**request (param)**
```
```

**response**
```
[
  {
    "id": Integer,
    "username": String,
    "nickname": String,
    "fcm_reg_id": String
  },
]
```
#### -POST
Create chat user

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |

**request (param)**
```
{
  "username": String,
  "password": String,
  "nickname": String,
  "fcm_reg_id": String (Optional)
}
```

**response**
```
{
  "id": Integer,
  "username": String,
  "nickname": String,
  "fcm_reg_id": String
}
```

#### -PUT
Edit chat user

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
{
  'nickname': String (Optional)
  'fcm_reg_id': String (Optional)
}
```

**response**
```
{
  "id": Integer,
  "username": String,
  "nickname": String,
  "fcm_reg_id": String
}
```

#### -DELETE
Delete user

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
```

**response**
```
{
  "message": "Success Delete Chatter"
}
```

## /api/chatters/{chatter_id}
#### -GET
Get a chat user by chatter_id

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
```

**response**
```
{
  "id": Integer,
  "username": String,
  "nickname": String,
  "fcm_reg_id": String
}
```

## /api/chatrooms
#### -GET
Get user's chatrooms

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
```

**response**
```
[
  {
    "id": Integer,
    "last_chat_time": String,
    "create_time": String,
    "owner": {
        "id": Integer,
        "username": String,
        "nickname": String,
        "fcm_reg_id": String
    },
    "opponent": {
        "id": Integer,
        "username": String,
        "nickname": String,
        "fcm_reg_id": String
    }
  },
]
```

#### -POST
Create user's chatrooms

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
{
  opponent_id: Integer
}
```

**response**
```
{
  "id": Integer,
  "last_chat_time": String,
  "create_time": String,
  "owner": {
      "id": Integer,
      "username": String,
      "nickname": String,
      "fcm_reg_id": String
  },
  "opponent": {
      "id": Integer,
      "username": String,
      "nickname": String,
      "fcm_reg_id": String
  }
}
```

## /api/chatrooms/{chatroom_id}
#### -GET
Get a chatroom by chatroom_id

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
{
}
```

**response**
```
{
  "id": Integer,
  "last_chat_time": String,
  "create_time": String,
  "owner": {
      "id": Integer,
      "username": String,
      "nickname": String,
      "fcm_reg_id": String
  },
  "opponent": {
      "id": Integer,
      "username": String,
      "nickname": String,
      "fcm_reg_id": String
  }
}
```

#### -DELETE
Delete a chatroom by chatroom_id

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
```

**response**
```
{
    "message": "Success Delete Chatroom"
}
```

## /api/chatrooms/{chatroom_id}/chats
#### -GET
Get all chats in chatroom

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
```

**response**
```
[
  {
    "id": Integer,
    "chatroom_id": Integer,
    "sender_id": Integer,
    "receiver_id": Integer,
    "content": String,
    "create_time": String
  }
]
```

#### -POST
Send chat

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
{
  "receiver_id": Integer,
  "content": String
}
```

**response**
```
{
  "id": Integer,
  "chatroom_id": Integer,
  "sender_id": Integer,
  "receiver_id": Integer,
  "content": String,
  "create_time": String
}
```

## /api/chatrooms/{chatroom_id}/chats/search
#### -POST
Search chat by content

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
{
  "query": String
}
```

**response**
```
[
  {
    "id": Integer,
    "chatroom_id": Integer,
    "sender_id": Integer,
    "receiver_id": Integer,
    "content": String,
    "create_time": String
  }
]
```

## /api/chats/{chat_id}
#### -GET
Get a chat

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```

```

**response**
```
{
  "id": Integer,
  "chatroom_id": Integer,
  "sender_id": Integer,
  "receiver_id": Integer,
  "content": String,
  "create_time": String
}
```

#### -PUT
Edit a chat message

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```
{
  "content": String
}
```

**response**
```
{
  "id": Integer,
  "chatroom_id": Integer,
  "sender_id": Integer,
  "receiver_id": Integer,
  "content": String,
  "create_time": String
}
```

#### -DELETE
Delete a chat

**header**

|Key|Value|
|---|-----|
|Content-Type| application/json |
|Authorization| Bearer TOKEN |

**request (param)**
```

```

**response**
```
{
    "message": "Success Delete Chat"
}
```

How To Deploy
-------------------------
```
$ sudo apt-get update
$ sudo apt-get upgrade

$ sudo apt-get install python3.6-dev
$ virtualenv -p python3.6 venv
$ pip install -r requirements.txt

$ sudo snap install heroku --classic

$ heroku login
$ heroku create
$ heroku addons:create heroku-redis:hobby-dev -a [app_name]

$ git add .
$ git commit -m "Message"
$ git push heroku master

$ heroku ps:scale worker=1
```

Test
----------------
```
python manage.py test
```
