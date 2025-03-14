#!/usr/bin/env python3

from google.cloud import storage

def test_bucket_access(bucket_name: str):
    """Test if we can access a specific GCP bucket."""
    try:
        # Initialize the client
        storage_client = storage.Client()
        
        # Try to get the bucket
        bucket = storage_client.bucket(bucket_name)
        
        # List a few blobs to test access (limit to 1 for quick test)
        blobs = list(bucket.list_blobs(max_results=1))
        
        print(f"✅ Successfully accessed bucket: {bucket_name}")
        if blobs:
            print(f"Found file in bucket: {blobs[0].name}")
        else:
            print("Bucket is empty or you don't have access to list its contents")
            
    except Exception as e:
        print(f"❌ Error accessing bucket: {str(e)}")
        print("\nPossible reasons:")
        print("1. You're not authenticated with GCP")
        print("2. You don't have permission to access this bucket")
        print("3. The bucket name is incorrect")
        print("\nTo authenticate, you can:")
        print("a) Run 'gcloud auth application-default login'")
        print("b) Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("c) Use a service account key file")

if __name__ == "__main__":
    # Replace with your bucket name
    BUCKET_NAME = "your-bucket-name"
    
    print("Testing GCP bucket access...")
    test_bucket_access(BUCKET_NAME) 