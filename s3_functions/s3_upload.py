import requests

# The presigned S3 URL you provided
presigned_url = "https://dev-aitech-marketplace-blob-storage.s3.ap-southeast-1.amazonaws.com/0029781988958338526/1d8b3fb7-951d-4916-a6f1-bdc77ebc9269-apple.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAVRUVRKXLLDFHXXZT%2F20240910%2Fap-southeast-1%2Fs3%2Faws4_request&X-Amz-Date=20240910T094947Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEoaDmFwLXNvdXRoZWFzdC0xIkYwRAIgUlU1tyzj8gtYxA7slYnAfix2QHnzZp7BzeDpOQTUVNICIA%2Fb99kMSmgIl7hWh00RLR0mTxP%2FoYx8WeJGEp%2F%2F7zNWKrMFCHMQABoMMzgxNDkxOTU5MjU0IgycK%2FCneMhSV2fzLwgqkAWyFn3CcxqiJtkoZVV%2BbH7xMcml%2BZNptb5tX64%2B2KjeJW%2FqllBD%2BNRb1bwrkt4AwJ%2FZq%2Bn91K4ThdQKXRqbntkRXIg7rIdjCQWxZRFp2cX6qNFK0OzGMGg%2BCb7wJUXed0AmLFIy%2BVN1%2FaiJHZY%2FLbA7ZfyXY45Qalv3kZqtp4tpGDf%2FvjiAyvKi4rhTM2q7HOUbPXAQEUW69IEBLi9XCprNbmX4tALrAqOYj9tNpCbW%2BiraEb6NVmPbD2H7V67CYUxJS5DijJk1dGi%2B604adzwHEnk7KUe%2FsVyTCW1%2FgVJbGi2tPEg9RYovg4BGOgDS9%2B9fABPgWD8k7iMiIb4LbouE7IBDIXZVES%2BZsXGGn658fQ7hUFCRUqWdaHnPI4E4wIQ9CtLaqO07upSKz%2Fp5PlcpzXmNyln0VpoRhP4mhFgrILs710Nf3XBM8%2BuPgClTZsjHlsDfSTWZDd3i5RYKvAjbWeWvBeokCJRgNGqsa6mj78pVIYB8yfTVLhO41tj3tYVl66q2L0DFu54L7UDNN%2BZIsjVulhHsYu7u88VIM9KxdjSI70l%2BsEmxfpt%2FcV45FBxZt1aOwja6tUS1BWYM12sny10sYsHndjTOjqB2ec6Lqk9mt6ce6mOH7LLr0liukIXHGbC55zaqMmFIy3qYpoR2lJfsfs28%2BbDyYHl8sPe5YBmU9ttnJtcUIIiRLztfFffvuzszj3bKXPBoujriPh2iZtufw1F4BlPcRyIvldAjv7Tbpl4es%2BIqxXNdg5JUjCkm86OTyagiUoFkumeEoHPkgdq%2BkIfapw0tdlmKtP3N4sL0vn2TZ96pfBkS4FiIYaeAaFEvriViqJTIJUBUSmRgLXb9xisbJhWKpRdp9xZWVDC8rIC3BjqcAdfuRVROSN5c7%2Fc8JbX3Ejc9V5aUCrl7rA%2BLJ5tG3sEa1YpqJMcIK9gSN3uQPlVUWGyDzDU3Mjo4xsai1jejKgv0Yz4%2F5NiaGxRtFVFjv3lEMNWJrwZU%2Fi0KBHFNxG50JfoV%2BXTeAnKUam8gx9yT9Iwnqq6e%2BuuoyXY7nY0Wb34x%2BVPSUfDeiCV%2F1yf0w38THYvWxXc5JNRsatGwfQ%3D%3D&X-Amz-Signature=58789ed2a0db90d7ad67b7341bdec465b191157e5c4675b9bbe80dfa97a1a8d1&X-Amz-SignedHeaders=host&x-id=PutObject"

# Path to the file you want to upload
file_path = "C:\\Users\\USER\\Desktop\\AI_APPS_templates\\s3_functions\\apple.png"

# Open the file in binary mode
with open(file_path, 'rb') as file_data:
    # Perform the PUT request to upload the file
    response = requests.put(presigned_url, data=file_data)

    # Check if the upload was successful
    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(f"Response: {response.text}")
