import boto3
from botocore.exceptions import ClientError

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/zac9nk"
sqs = boto3.client('sqs')

def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])

def process_messages():
    try:
        messages = []  
        while len(messages) < 10:
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10 - len(messages),  
                MessageAttributeNames=['All']
            )
            if "Messages" in response:
                for msg in response['Messages']:
                    order = int(msg['MessageAttributes']['order']['StringValue'])
                    word = msg['MessageAttributes']['word']['StringValue']
                    handle = msg['ReceiptHandle']
                    messages.append({'order': order, 'word': word, 'handle': handle})
            else:
                print("No more messages in the queue")
                break

        # Reassemble the phrase
        messages.sort(key=lambda x: x['order'])
        phrase = ' '.join(msg['word'] for msg in messages)

        # Write the phrase to a file
        with open('output.txt', 'w') as file:
            file.write(phrase)

        Delete messages from the queue
        for msg in messages:
            delete_message(msg['handle'])

    except ClientError as e:
        print(e.response['Error']['Message'])

if __name__ == "__main__":
    process_messages()
