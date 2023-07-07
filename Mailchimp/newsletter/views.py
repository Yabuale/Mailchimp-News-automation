from django.shortcuts import render
import requests
import json
import datetime

# Create your views here.

api_key = 'api key'
audience_id = 'audience id'
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subscription = request.POST.get('subscription')
        
        endpoint = f"https://us21.api.mailchimp.com/3.0/lists/{{audience_id}}/members"  
        data = {
            'email_address': email,
            'status': 'subscribed',
            'merge_fields': {
                'STYPE': subscription
            }
        }

        headers = {
            'Authorization': f'apikey {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            
            print('User subscribed:', email)
        else:
           
            print('An error occurred:', response.text)

    return render(request, 'index.html')



def send(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        news_type = request.POST.get('newsType')


        ''' 
      There should be two audiences in the Mailchimp form, 
      so when the admin  sends a message, the system should switch the audience id based on
      the news_type.
      '''
        
        if news_type == 'News':
            campaign_id = 'News Audience id'
        else:
            campaign_id = 'Tender Audience id'

        campaign_url = "https://us21.api.mailchimp.com/3.0/campaigns"
        send_url = "https://us21.api.mailchimp.com/3.0/campaigns/{{campaign_id}}/actions/send"

        headers = {
            'Authorization': f'apikey {api_key}',
            'Content-Type': 'application/json'
        }

        try:
            # Create a new campaign
            campaign_data = {
            'recipients': {
            'list_id': audience_id
                  },
            'type': 'regular',
            'settings': {
            'subject_line': title,
            'preview_text': description,
            'title': title,
            'from_name': 'Yeabsra Alebchew',
            'from_email': 'yeabsraalebachew@gmail.com',
            'content': {
            'body': 'Hello, recipients! This is the content of the campaign email.',
            'html': '<html><body><p>Hello, recipients!</p><p>This is the content of the campaign email.</p></body></html>'
            },
            'send_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tracking': {
            'opens': True,
            'clicks': True
                  }
               }
            }

            response = requests.post(campaign_url, headers=headers, data=json.dumps(campaign_data))
            response.raise_for_status()
            campaign_id = response.json()['id']

            
            campaign_content_url = f"{campaign_url}/{campaign_id}/content"
            content_data = {
                'html': '<html><body><p>Hello, recipients!</p><p>This is the content of the campaign email.</p></body></html>'
            }
            response = requests.put(campaign_content_url, headers=headers, data=json.dumps(content_data))
            response.raise_for_status()

            
            send_campaign_url = send_url.replace('{{campaign_id}}', campaign_id)
            response = requests.post(send_campaign_url, headers=headers)
            response.raise_for_status()

            print('Email sent successfully.')
        except requests.exceptions.RequestException as e:
           
            print('An error occurred:', str(e))

    return render(request, 'send.html')