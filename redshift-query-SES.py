#!/usr/bin/python
# coding=utf-8
import datetime
import redshift_connector
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from IPython.display import HTML

#Connect to Redshift cluster using AWS credentials. Passing the plaintext user information is not recommended in a production code and check this document for different available options to connect to Redshift https://github.com/aws/amazon-redshift-python-driver/blob/master/tutorials/001%20-%20Connecting%20to%20Amazon%20Redshift.ipynb 
conn = redshift_connector.connect(
            host='<redshift-host-name>',
            port= <port name e.g. 5439>,
	        database='<db name e.g. dev>',
            user='<username e.g. awsuser',
            password='<Redshift user password>',
            )

# Run the sample query against a sample request_table in dev database
query = "select \
         requestid, \
         stateid, \
         requesttype, \
         requesterid, \
         requester_org, \
         primarytopic, \
         customerlocationregion, \
         datediff(day, date(lastassignmentdate), CURRENT_DATE) as age_of_request \
         from request_table \
         where requester_org = 'ABC' \
         and domainid = 'BUSINESS' \
         and stateid NOT IN ('COMPLETED', 'CANCELLED')"


#define cursor
cursor = redshift_connector.Cursor = conn.cursor()

#execute SQL query
cursor.execute(query)

#define column names for the dataframe
col_Names = ["Request-id", "Request-State", "Request-Type", "Requester-id", "Requester-ORG", "Primary-Topic", "Customer-Location-Region", "Age-of-Request"]

#dataframe containing Redshift query outputs
data = pd.DataFrame(cursor.fetchall(), columns=col_Names)

#Convert request-id to clickable link pointing to webpage where you have more data
data['Request-id'] = data['Request-id'].apply(lambda x: f'<a href="https://example.com/request/{x}">{x}</a>')
HTML(data.to_html(escape=False))

#Closing cursor and redshift conection
cursor.close
conn.close()

# Style Dataframe with HTML
data_html = data.style
data_html = data_html.set_table_styles([{'selector': 'table', 'props': [('border-collapse', 'collapse')]}, {'selector': 'table, td, th', 'props': [('border', '1px solid black')]}])
data_html = data_html.render()
#HTML_BODY = (data_html,'html')

########### Email ###############
# Set up E-mail

date = datetime.datetime.now()
date = date.strftime('%a %b %d')

SENDER = 'sender@xyz.com'
RECIPIENT = ['recipient-1@xyz.com', 'recipient-2@xyz.com']

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-west-2"

SUBJECT = 'Sample Report - ' + date
#msg.attach(HTML_BODY)

# The character encoding for the email.
CHARSET = "UTF-8"
# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': RECIPIENT,
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': data_html,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])
