from googleapiclient.discovery import build
import pandas as pd
import os
import time

# ========== CONFIGURATION ==========
API_KEY = ""  # YouTube API key
CHANNEL_IDS = [""]  # List of channel IDs
START_DATE = "2024-01-01" 
END_DATE = "2024-12-31"   
OUTPUT_FILE = "news.csv"  # Output file name
QUOTA_LIMIT = 10000  # Daily quota limit for API
# ===================================

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Track used quota
used_quota = 0

# Function to check quota usage
def check_quota_usage(required_quota):
    global used_quota
    if used_quota + required_quota > QUOTA_LIMIT:
        print(f"Quota exceeded! Used: {used_quota}, Required: {required_quota}")
        return False
    used_quota += required_quota
    return True

# Function to fetch videos from a channel within a date range
def fetch_videos(channel_id, start_date, end_date, max_results=50):
    global used_quota
    videos = []
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        publishedAfter=f"{start_date}T00:00:00Z",
        publishedBefore=f"{end_date}T23:59:59Z",
        maxResults=max_results,
        order="date",
        type="video"
    )
    while request:
        if not check_quota_usage(100):  # Each search request costs 100 units
            break
        response = request.execute()
        for item in response.get("items", []):
            if item["id"]["kind"] == "youtube#video":
                videos.append({
                    "channel_id": channel_id,
                    "channel_title": item["snippet"]["channelTitle"],
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"]
                })
        request = youtube.search().list_next(request, response)
    return videos

# Function to fetch channel statistics (e.g., subscriber count)
def fetch_channel_stats(channel_id):
    if not check_quota_usage(1):  # Channel stats request costs 1 unit
        return 0
    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()
    stats = response.get("items", [])[0]["statistics"]
    return stats.get("subscriberCount", 0)

# Function to fetch statistics for a list of video IDs
def fetch_video_stats(video_ids):
    stats = []
    for i in range(0, len(video_ids), 50):  # API allows max 50 IDs per request
        if not check_quota_usage(1):  # Videos stats request costs 1 unit per video
            break
        request = youtube.videos().list(
            part="statistics",
            id=",".join(video_ids[i:i + 50])
        )
        response = request.execute()
        for item in response.get("items", []):
            stats.append({
                "video_id": item["id"],
                "views": item["statistics"].get("viewCount", 0),
                "likes": item["statistics"].get("likeCount", 0),
                "comments": item["statistics"].get("commentCount", 0)
            })
    return stats

# Main function to fetch and save data for multiple channels
def fetch_channel_data(channel_ids, start_date, end_date, output_file="all_channels_videos.csv"):
    all_data = []

    for channel_id in channel_ids:
        print(f"Fetching data for channel: {channel_id}")

        # Fetch subscriber count
        subscribers = fetch_channel_stats(channel_id)

        # Fetch videos
        videos = fetch_videos(channel_id, start_date, end_date)
        if not videos:
            print(f"No videos found or quota exhausted for channel: {channel_id}")
            continue

        # Add subscriber count to each video entry
        for video in videos:
            video["subscribers"] = subscribers

        video_ids = [video["video_id"] for video in videos]
        stats = fetch_video_stats(video_ids)

        # Combine video metadata and statistics
        videos_df = pd.DataFrame(videos)
        stats_df = pd.DataFrame(stats)
        combined_df = pd.merge(videos_df, stats_df, on="video_id")

        # Add video link column
        combined_df["video_link"] = combined_df["video_id"].apply(
            lambda vid: f"https://www.youtube.com/watch?v={vid}"
        )

        # Collect data for all channels
        all_data.append(combined_df)

        # Log the last processed video date
        if videos:
            last_video_date = videos[-1]["published_at"]
            print(f"Last processed video date for channel {channel_id}: {last_video_date}")

    # Combine all data into a single DataFrame
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)

        # Save or append to CSV
        if os.path.exists(output_file):
            existing_data = pd.read_csv(output_file, encoding="utf-8")
            combined_data = pd.concat([existing_data, final_df]).drop_duplicates(subset=["video_id"])
        else:
            combined_data = final_df

        combined_data.to_csv(output_file, index=False, encoding="utf-8")
        print(f"Data saved to {output_file}")
    else:
        print("No data collected for the given channels.")

# Fetch data for channels
fetch_channel_data(CHANNEL_IDS, START_DATE, END_DATE, OUTPUT_FILE)
