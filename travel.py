import streamlit as st
import requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = "AIzaSyBJjgYVASelNgVKBy8j5oQDelkPVCHPK2Q"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of broader keywords
keywords = ["Russia Ukraine War Latest Update", "China Taiwan Military Tension", "F-35 Fighter Jet News 2024","US Navy Modern Destroyer Review","Hypersonic Missile Technology Explained","NATO Exercise Drills Full Footage","World Military Power Ranking 2024", "Abrams Tank vs T-14 Armata Analysis", "Military Drone Warfare Tactics",
    "New Defense Budget Breakdown", "Special Forces Training Documentary", "Future of Warfare AI and Robots",
    "North Korea Missile Launch Report", "Top 10 Military Technologies 2024", "Aircraft Carrier Operations Footage",
    "Geopolitical Security News Briefing", "Cyber Warfare Attacks Latest", "Submarine Technology Deep Dive",
    "Military History Underrated Battles", "Aerospace Defense Industry News", "Space Force Capabilities Update",
    "M-142 HIMARS in Action","Middle East Conflict Drone Tactics",
    "Baltic Sea NATO Patrols",
    "China's Stealth Bomber Program",
    "Russian Military Weaknesses Analysis",
    "Iran Nuclear Program Update",
    "Autonomous Weapon Systems Ethical Debate",
    "Hypersonic Defense Systems vs Offense",
    "Laser Weapon Development Breakthrough",
    "Internet of Military Things (IoMT) Explained",
    "Next Generation Submarine Design",
    "Why Aircraft Carriers Are Obsolete",
    "US vs China Military Budget Comparison",
    "Military Spending Debate **(Your Country)**",
    "Lessons Learned Ukraine War Drones",
    "Recruitment Crisis Solutions Military","Trump Latest RALLY Speech 2025", 
    "Trump vs Biden Polls November",
    "Trump LEGAL Case Manhattan Verdict",
    "Trump Policy on China Trade",
    "Donald Trump Federal Reserve Attack",
    "Xi Jinping Taiwan War Strategy",
    "China Economic Collapse Warning 2025",
    "Xi Jinping PURGE Military Leaders",
    "China Naval Power vs US Navy",
    "China Spy Balloon Technology Explained","Russia Breakthrough Pokrovsk Front",
    "Ukraine Counteroffensive Strategy 2025 Analysis",
    "Putin NUCLEAR Threat Latest",
    "Western Weapon Failures Ukraine",
    "Tomahawk Missile Shipment Ukraine","Kim Jong Un Missile Launch Warning",
    "North Korea Satellite Program Success",
    "North Korea South Korea DMZ Clashes",
    "Kim Jong Un Meets Trump Analysis",
    "North Korea Cyber War Hacking"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            # Define search parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            # Fetch video data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            # Check if "items" key exists
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")
                continue

            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"Failed to fetch video statistics for keyword: {keyword}")
                continue

            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # Collect results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs > 1000:  # Only include channels with fewer than 3,000 subscribers
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            for result in all_results:
                st.markdown(
                    f"**Title:** {result['Title']}  \n"
                    f"**Description:** {result['Description']}  \n"
                    f"**URL:** [Watch Video]({result['URL']})  \n"
                    f"**Views:** {result['Views']}  \n"
                    f"**Subscribers:** {result['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

