# Mattermost Channel Info

## Overview
Mattermost Channel Info is a Dockerized Python application designed to fetch and display various metrics from a specified Mattermost channel. It retrieves basic channel information like member count and file count, as well as engagement metrics such as the number of posts, replies, and reactions.

## Prerequisites
- Docker installed on your machine.
- Access to a Mattermost server and an API access token.
- The Channel ID of the Mattermost channel for which you want to fetch metrics.

## Installation

1. **Pull the Docker Image**

   Pull the pre-built Docker image from GHCR using:
   ```bash
   docker pull ghcr.io/maxwellpower/mm-channel-info
   ```

2. **Environment Setup**

   Create a `.env` file in your working directory with the following content:
   ```
   MATTERMOST_URL=https://your-mattermost-url.com
   CHANNEL_ID=your-channel-id
   ACCESS_TOKEN=your-access-token
   ```
   Replace these values with your actual Mattermost server URL, the channel ID, and your access token.

## Usage

To run the application, execute the following command in the directory where your `.env` file is located:
```bash
docker run --env-file .env ghcr.io/maxwellpower/mm-channel-info
```

This command runs the application inside the Docker container, using the environment variables defined in your `.env` file. The script will output the channel metrics to the console.

## Note

- Ensure that the access token used has the necessary permissions to access channel details on your Mattermost server.
- Handle the access token securely and adhere to your organization's data privacy and security policies.
