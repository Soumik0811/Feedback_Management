from trycourier import Courier

client = Courier(auth_token="pk_prod_5CHPPPPC914Q8GP1AGB11EYHCC26")

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