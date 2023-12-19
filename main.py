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

VERSION = "1.0.0"

import os
import requests

# Read environment variables
mattermost_url = os.environ.get('MATTERMOST_URL')
channel_id = os.environ.get('CHANNEL_ID')
access_token = os.environ.get('ACCESS_TOKEN')

# Headers for authentication
headers = {
    'Authorization': f'Bearer {access_token}',
}

# Function to get channel details
def get_channel_details(channel_id):
    channel_url = f"{mattermost_url}/api/v4/channels/{channel_id}"
    response = requests.get(channel_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching channel details: {response.status_code}")
        return None

# Function to get posts from a channel with pagination
def get_channel_posts(channel_id, page=0, per_page=60):
    posts_url = f"{mattermost_url}/api/v4/channels/{channel_id}/posts?page={page}&per_page={per_page}"
    response = requests.get(posts_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching posts: {response.status_code}")
        return None

# Function to count reactions for a post
def count_reactions(post_id):
    reactions_url = f"{mattermost_url}/api/v4/posts/{post_id}/reactions"
    response = requests.get(reactions_url, headers=headers)
    if response.status_code == 200:
        return len(response.json())
    else:
        print(f"Error counting reactions: {response.status_code}")
        return 0

# Main function to get all channel metrics
def get_all_channel_metrics(channel_id):
    channel_details = get_channel_details(channel_id)
    if not channel_details:
        return

    # Channel basic metrics
    member_count = channel_details['member_count']
    guest_count = channel_details['guest_count']
    pinned_post_count = channel_details['pinnedpost_count']
    files_count = channel_details['files_count']

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
