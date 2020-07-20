import json
import requests
import boto3


def get_s3(region=None):
    """
    Get a Boto 3 Amazon S3 resource with a specific AWS Region or with your
    default AWS Region.
    """
    return boto3.resource('s3', region_name=region) if region else boto3.resource('s3')

def readS3file(bucket, key):

    # s3 = session.resource('s3')
    region = 'ap-southeast-2'
    s3 = get_s3(region)
    
    # get a handle on the bucket that holds your file
    bucket = s3.Bucket(bucket) # example: energy_market_procesing
    
    # get a handle on the object you want (i.e. your file)
    obj = bucket.Object(key) # example: market/zone1/data.csv
    
    # get the object
    response = obj.get()
    
    # read the contents of the file
    lines = response['Body'].read()
    
    return lines

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    print(event)
    # print("event['pathParameters'] -> " + event['pathParameters'])
    # print("event['path'] -> " + event['path'])

    try:
        
        bucket = 'zhangshen20-gamble'        
    
        if(event['resource'] == '/race'):
            
            key = 'API/OUT/race/meetingDate_' + "2020-06-01" + '.json'
            
        elif(event['resource'] == '/race/{meetingDate}'):
            
            print('-----' + event['pathParameters']['meetingDate'] + '--------')

            key = 'API/OUT/race/meetingDate_' + event['pathParameters']['meetingDate'] + '.json'
            
        elif(event['resource'] == '/runner'):            
            
            
            
            key = 'API/OUT/runner/runnerNameKey_' + "CINEMATOGRAPHY 2" + '.json'
            
        elif(event['resource'] == '/runner/{runnerName}'): 
            
            runner_name = event['pathParameters']['runnerName'].replace('%20', ' ')
            
            key = 'API/OUT/runner/runnerNameKey_' + runner_name + '.json'            
            
        file_content = readS3file(bucket, key)
        
    except requests.RequestException as e:
        # Send some context about this error to Lambda Logs
        print(e)
        # file_content = 'Data is not available'
        
        raise e

    # return file_content

    return {
        "statusCode": 200,
        "body": file_content
    }
    
    
        # "body": json.dumps({
        #     "message": bucket + '/' + key,
        #     "location": file_content.text.replace("\n", "")
        # }),    

# if __name__ == '__main__':
#     # main()
#     print(lambda_handler('',''))
