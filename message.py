import requests
import json


# Steps for Jokes Delivery
# 1. Retrieve page access token from https://developers.facebook.com/tools/explorer/666615676843865?method=GET&path=667782319960906%2Fconversations%20&version=v2.9
# 2. Read all the conversations
# 3. Register all conversations in database, 
# 4. If Jokes not delivered, deliver joke

# Read all conversations
# payload = {
# 	"access_token":"EAAJeSI6et1kBAG0PhzkRHIh1Wk5VZBQbhWj2tFIatrzqnvPdXct1yYWfkgLOu66a9oerFcaZCrxqtbE5wLYKZCZBF5NbjKfkc3BfCvGSLnZCZAG1HiZCJzjhYR2UbwhlEm2KcxgHxbk2ZCNiagRoXOjTVv3TUvTr4CoZD"
# }

# response = requests.get(
# 	"https://graph.facebook.com/v2.9/667782319960906/conversations?access_token=EAAJeSI6et1kBAG0PhzkRHIh1Wk5VZBQbhWj2tFIatrzqnvPdXct1yYWfkgLOu66a9oerFcaZCrxqtbE5wLYKZCZBF5NbjKfkc3BfCvGSLnZCZAG1HiZCJzjhYR2UbwhlEm2KcxgHxbk2ZCNiagRoXOjTVv3TUvTr4CoZD", 
# )

# print(response.json())

# Get Conversation ID, Send Message
payload = {
		"message": "Hello Suman! Thank you for contating us. Please call 9840063224 for coupon delivery.",
		"access_token":"EAAJeSI6et1kBAG0PhzkRHIh1Wk5VZBQbhWj2tFIatrzqnvPdXct1yYWfkgLOu66a9oerFcaZCrxqtbE5wLYKZCZBF5NbjKfkc3BfCvGSLnZCZAG1HiZCJzjhYR2UbwhlEm2KcxgHxbk2ZCNiagRoXOjTVv3TUvTr4CoZD"
}

response = requests.post(
	"https://graph.facebook.com/v2.9/t_mid.$cAAIFrnoyzmViWhEOQVcKMvFJaCYe/messages", 
     data=json.dumps(payload),
     headers = {"Content-Type": "application/json"}
)

print(response.json())
