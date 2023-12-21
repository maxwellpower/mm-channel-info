# Mattermost Channel Info

# Copyright (c) 2023 Maxwell Power
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# -*- coding: utf-8 -*-

VERSION = "1.0.3"

import os
import requests
import urllib3

# Read environment variables
mattermost_url = os.environ.get('MATTERMOST_URL')
channel_id = os.environ.get('CHANNEL_ID')
access_token = os.environ.get('ACCESS_TOKEN')
verify_ssl = os.environ.get('VERIFY_SSL', 'True') == 'True'  # Default to True

# Suppress InsecureRequestWarning if SSL verification is turned off
if not verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Headers for authentication
headers = {
    'Authorization': f'Bearer {access_token}',
}

# Function to get channel details
def get_channel_details(channel_id):
    channel_url = f"{mattermost_url}/api/v4/channels/{channel_id}"
    response = requests.get(channel_url, headers=headers, verify=verify_ssl)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching channel details: {response.status_code}")
        return None

# Function to get posts from a channel with pagination
def get_channel_posts(channel_id, page=0, per_page=60):
    posts_url = f"{mattermost_url}/api/v4/channels/{channel_id}/posts?page={page}&per_page={per_page}"
    response = requests.get(posts_url, headers=headers, verify=verify_ssl)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching posts: {response.status_code}")
        return None

# Function to count reactions for a post
def count_reactions(post_id):
    reactions_url = f"{mattermost_url}/api/v4/posts/{post_id}/reactions"
    response = requests.get(reactions_url, headers=headers, verify=verify_ssl)
    if response.status_code == 200:
        return len(response.json())
    else:
        print(f"Error counting reactions: {response.status_code}")
        return 0

# Main function to get all channel metrics
def get_all_channel_metrics(channel_id):
    channel_details = get_channel_details(channel_id)
    if not channel_details or 'member_count' not in channel_details:
        print("Error: Unable to fetch channel details or 'member_count' not found in response.")
        return
    
    # Extracting metrics from channel details
    member_count = channel_details.get('member_count', 0)
    guest_count = channel_details.get('guest_count', 0)
    pinned_post_count = channel_details.get('pinnedpost_count', 0)
    files_count = channel_details.get('files_count', 0)

    # Engagement metrics
    page = 0
    total_posts, total_replies, total_reactions = 0, 0, 0
    while True:
        posts_data = get_channel_posts(channel_id, page=page)
        if not posts_data or len(posts_data['posts']) == 0:
            break

        total_posts += len(posts_data['posts'])
        total_replies += sum(1 for post in posts_data['posts'].values() if post['parent_id'] != '')
        total_reactions += sum(count_reactions(post_id) for post_id in posts_data['posts'])

        page += 1

    # Output all metrics
    print(f"Member Count: {member_count}")
    print(f"Guest Count: {guest_count}")
    print(f"Pinned Post Count: {pinned_post_count}")
    print(f"Files Count: {files_count}")
    print(f"Total Posts: {total_posts}")
    print(f"Total Replies: {total_replies}")
    print(f"Total Reactions: {total_reactions}")

# Execute the main function
get_all_channel_metrics(channel_id)
