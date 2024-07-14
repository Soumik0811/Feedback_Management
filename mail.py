from trycourier import Courier

client = Courier(auth_token="Your authentication token")

resp = client.send_message(
        message={
          "to": {
            "email": "pameshsharma87@gmail.com"
          },
          "content": {
            "title": "Welcome to Courier!",
            "body": "Want to hear a joke? {{joke}}"
          },
          "data":{
            "joke": "Why does Python live on land? Because it is above C level"
          }
        }
      )      
