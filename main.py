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

VERSION = "1.0.4"


import os
import requests
import urllib3

# Read environment variables
mattermost_url = os.environ.get('MATTERMOST_URL')
channel_id = os.environ.get('CHANNEL_ID')
access_token = os.environ.get('ACCESS_TOKEN')
verify_ssl = os.environ.get('VERIFY_SSL', 'True') == 'True'  # Default to True

# Headers for authentication
headers = {'Authorization': f'Bearer {access_token}'}

# Suppress InsecureRequestWarning if SSL verification is turned off
if not verify_ssl:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to get channel statistics
def get_channel_stats(channel_id):
    stats_url = f"{mattermost_url}/api/v4/channels/{channel_id}/stats"
    response = requests.get(stats_url, headers=headers, verify=verify_ssl)
    return response.json() if response.status_code == 200 else None

# Function to get pinned posts
def get_pinned_posts(channel_id):
    pinned_url = f"{mattermost_url}/api/v4/channels/{channel_id}/pinned"
    response = requests.get(pinned_url, headers=headers, verify=verify_ssl)
    return response.json() if response.status_code == 200 else None

# Function to get all posts from a channel with pagination for counting files, replies, and reactions
def get_all_posts_for_metrics(channel_id, page=0, per_page=200):
    posts_url = f"{mattermost_url}/api/v4/channels/{channel_id}/posts?page={page}&per_page={per_page}"
    response = requests.get(posts_url, headers=headers, verify=verify_ssl)
    return response.json() if response.status_code == 200 else None

# Main function to get all channel metrics
def get_all_channel_metrics(channel_id):
    channel_stats = get_channel_stats(channel_id)
    pinned_posts = get_pinned_posts(channel_id)
    member_count = channel_stats['member_count'] if channel_stats else 0
    pinned_post_count = len(pinned_posts['order']) if pinned_posts else 0

    total_files = total_reactions = total_replies = total_posts = 0
    page = 0
    while True:
        posts_data = get_all_posts_for_metrics(channel_id, page=page)
        if not posts_data or len(posts_data['posts']) == 0:
            break

        total_posts += len(posts_data['posts'])
        for post in posts_data['posts'].values():
            if post['parent_id']:
                total_replies += 1
            total_files += len(post.get('file_ids', []))
            total_reactions += len(post.get('metadata', {}).get('reactions', []))
        
        page += 1

    # Output all metrics
    print(f"Member Count: {member_count}")
    print(f"Pinned Post Count: {pinned_post_count}")
    print(f"Files Count: {total_files}")
    print(f"Total Posts: {total_posts}")  # This includes original posts and replies
    print(f"Total Replies: {total_replies}")
    print(f"Total Reactions: {total_reactions}")

# Execute the main function
get_all_channel_metrics(channel_id)
