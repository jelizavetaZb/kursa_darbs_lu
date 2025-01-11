import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = "news.csv" 
data = pd.read_csv(file_path)

days_translation = {
    "Monday": "Pirmdiena",
    "Tuesday": "Otrdiena",
    "Wednesday": "Trešdiena",
    "Thursday": "Ceturtdiena",
    "Friday": "Piektdiena",
    "Saturday": "Sestdiena",
    "Sunday": "Svētdiena"
}
days_order = ["Pirmdiena", "Otrdiena", "Trešdiena", "Ceturtdiena", "Piektdiena", "Sestdiena", "Svētdiena"]
data["published_at"] = pd.to_datetime(data["published_at"])
data["day_of_week"] = data["published_at"].dt.day_name()
data["hour"] = data["published_at"].dt.hour
data["day_of_week_latvian"] = data["day_of_week"].map(days_translation)
data["engagement_percent"] = (data["likes"] + data["comments"]) / data["subscribers"] * 100
data["view_percent"] = (data["views"] / data["subscribers"]) * 100
data["like_percent"] = (data["likes"] / data["subscribers"]) * 100
data["comment_percent"] = (data["comments"] / data["subscribers"]) * 100

engagement_by_day = data.groupby("day_of_week_latvian").mean(numeric_only=True)["engagement_percent"]
engagement_by_day = engagement_by_day.reindex(days_order)

engagement_by_channel = data.groupby("channel_title").mean(numeric_only=True)["engagement_percent"]
activity_by_hour = data.groupby("hour").mean(numeric_only=True)[["views", "likes", "comments"]]
percent_activity_by_hour = data.groupby("hour").mean(numeric_only=True)[["view_percent", "like_percent", "comment_percent"]]
data["hour"] = data["published_at"].dt.hour
activity_by_hour = data.groupby("hour").mean(numeric_only=True)[["views", "likes", "comments"]]

views_by_day = data.groupby("day_of_week_latvian").mean(numeric_only=True)["views"]
views_by_day = views_by_day.reindex(days_order) 

views_by_hour_and_day = data.groupby(["day_of_week_latvian", "hour"]).mean(numeric_only=True)[["views", "likes", "comments"]]


# Karstuma karte kopējai iesaistei pēc stundām
percent_activity_by_hour["engagement_percent"] = (percent_activity_by_hour["like_percent"] + percent_activity_by_hour["comment_percent"])
plt.figure(figsize=(12, 6))
sns.heatmap(percent_activity_by_hour[["engagement_percent"]].T, cmap="OrRd", annot=True, fmt=".1f", cbar=True)
plt.title("Karstuma karte kopējai iesaistei pēc stundām", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Iesaistes procents (%)", fontsize=14)
plt.tight_layout()
plt.show()

# Karstuma karte kopējai iesaistei pēc nedēļas dienām
data["engagement_percent"] = (data["like_percent"] + data["comment_percent"])
engagement_by_day = data.groupby("day_of_week_latvian").mean(numeric_only=True)["engagement_percent"].reindex(days_order)
plt.figure(figsize=(10, 6))
sns.heatmap(engagement_by_day.to_frame().T, cmap="OrRd", annot=True, fmt=".1f", cbar=True)
plt.title("Karstuma karte kopējai iesaistei pēc nedēļas dienām", fontsize=16)
plt.xlabel("Nedēļas diena", fontsize=14)
plt.ylabel("Iesaistes procents (%)", fontsize=14)
plt.tight_layout()
plt.show()

# Karstuma karte kopējai iesaistei pēc stundām un nedēļas dienām
heatmap_data_engagement = data.pivot_table(index="day_of_week_latvian", columns="hour", values="engagement_percent", aggfunc="mean").reindex(days_order)
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data_engagement, cmap="YlGnBu", annot=True, fmt=".1f", cbar=True)
plt.title("Karstuma karte kopējai iesaistei pēc stundām un nedēļas dienām", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Nedēļas diena", fontsize=14)
plt.tight_layout()
plt.show()


# Karstuma karte kopējai aktivitātei pēc stundām
percent_activity_by_hour["total_activity_percent"] = (percent_activity_by_hour["view_percent"] + percent_activity_by_hour["like_percent"] + percent_activity_by_hour["comment_percent"])
plt.figure(figsize=(12, 6))
sns.heatmap(percent_activity_by_hour[["total_activity_percent"]].T, cmap="YlOrRd", annot=True, fmt=".1f", cbar=True)
plt.title("Karstuma karte kopējai aktivitātei pēc stundām", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Kopējā aktivitāte (%)", fontsize=14)
plt.tight_layout()
plt.show()

# Karstuma karte kopējai aktivitātei pēc nedēļas dienām
data["total_activity_percent"] = (data["view_percent"] + data["like_percent"] + data["comment_percent"])
activity_by_day = data.groupby("day_of_week_latvian").mean(numeric_only=True)["total_activity_percent"].reindex(days_order)
plt.figure(figsize=(10, 6))
sns.heatmap(activity_by_day.to_frame().T, cmap="YlOrRd", annot=True, fmt=".1f", cbar=True)
plt.title("Karstuma karte kopējai aktivitātei pēc nedēļas dienām", fontsize=16)
plt.xlabel("Nedēļas diena", fontsize=14)
plt.ylabel("Kopējā aktivitāte (%)", fontsize=14)
plt.tight_layout()
plt.show()

#Karstuma karte kopējai aktivitātei pēc stundām un nedēļas dienām
heatmap_data_total = data.pivot_table(index="day_of_week_latvian", columns="hour", values="total_activity_percent",aggfunc="mean").reindex(days_order)
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data_total,cmap="YlGnBu",annot=True,fmt=".1f",cbar=True)
plt.title("Karstuma karte kopējai aktivitātei pēc stundām un nedēļas dienām", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Nedēļas diena", fontsize=14)
plt.tight_layout()
plt.show()


# Skatījumu, patīk un komentāru sadalījums pa stundām ({day})
views_by_hour_and_day = data.groupby(["day_of_week_latvian", "hour"]).mean(numeric_only=True)[["views", "likes", "comments"]]
for day in days_order:
    day_data = views_by_hour_and_day.loc[day]
    plt.figure(figsize=(12, 6))
    plt.plot(day_data.index, day_data["views"], marker="o", label="Skatījumi", color="blue")
    plt.plot(day_data.index, day_data["likes"], marker="o", label="Patīk", color="orange")
    plt.plot(day_data.index, day_data["comments"], marker="o", label="Komentāri", color="green")
    plt.title(f"Skatījumu, patīk un komentāru sadalījums pa stundām ({day})", fontsize=16)
    plt.xlabel("Stunda", fontsize=14)
    plt.ylabel("Vidējais skaits", fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

# Karstuma karte skatījumu procentuālā sadalījumam pēc stundām un nedēļas dienām
heatmap_data_view_percent = data.pivot_table(index="day_of_week_latvian", columns="hour", values="view_percent", aggfunc="mean").reindex(days_order)
sns.heatmap(heatmap_data_view_percent, cmap="YlOrRd", annot=False, cbar=True)
plt.title("Karstuma karte skatījumu (%) sadalījumam pēc stundām un nedēļas dienām", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Nedēļas diena", fontsize=14)
plt.tight_layout()
plt.show()


# Karstuma karte skatījumu sadalījumam pēc stundām un nedēļas dienām
heatmap_data_views = data.pivot_table(index="day_of_week_latvian", columns="hour", values="views", aggfunc="mean").reindex(days_order)
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data_views, cmap="YlGnBu", annot=False, cbar=True)
plt.title("Karstuma karte skatījumu sadalījumam pēc stundām un nedēļas dienām", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Nedēļas diena", fontsize=14)
plt.tight_layout()
plt.show()

# Vidējais skatījumu skaits pēc nedēļas dienā
plt.figure(figsize=(10, 6))
plt.plot(views_by_day.index, views_by_day, marker="o", color="blue", label="Skatījumi")
plt.title("Vidējais skatījumu skaits pēc nedēļas dienām", fontsize=16)
plt.xlabel("Nedēļas diena", fontsize=14)
plt.ylabel("Vidējais skatījumu skaits", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Skatījumu sadalījums
plt.figure(figsize=(10, 6))
plt.hist(data["views"], bins=30, color="blue", edgecolor="black", alpha=0.7, log=True)
plt.title("Skatījumu sadalījums", fontsize=16)
plt.xlabel("Skatījumi", fontsize=14)
plt.ylabel("Video skaits", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Patīk sadalījums
plt.figure(figsize=(10, 6))
plt.hist(data["likes"], bins=30, color="orange", edgecolor="black", alpha=0.7, log=True)
plt.title("Patīk sadalījums", fontsize=16)
plt.xlabel("Patīk", fontsize=14)
plt.ylabel("Video skaits", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# Komentāru sadalījums
plt.figure(figsize=(10, 6))
plt.hist(data["comments"], bins=30, color="green", edgecolor="black", alpha=0.7, log=True)
plt.title("Komentāru sadalījums", fontsize=16)
plt.xlabel("Komentāri", fontsize=14)
plt.ylabel("Video skaits", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()


# Skatījumu sadalījums starp kanāliem
grouped_views = data.groupby("channel_title")["views"].sum()
plt.figure(figsize=(8, 8))
plt.pie(grouped_views, labels=grouped_views.index, autopct="%.1f%%", startangle=140, colors=sns.color_palette("pastel"))
plt.title("Skatījumu sadalījums starp kanāliem", fontsize=16)
plt.tight_layout()
plt.show()


# Vidējais skatījumu procents pēc stundām (%)
plt.figure(figsize=(12, 6))
plt.plot(percent_activity_by_hour.index, percent_activity_by_hour["view_percent"], marker="o", color="blue", label="Skatījumi (%)")
plt.title("Vidējais skatījumu procents pēc stundām (%)", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Vidējais skatījumu procents", fontsize=14) 
plt.xticks(ticks=np.arange(0, 24, 1))
plt.grid(True)
plt.tight_layout()
plt.show()

# Vidējais patīk un komentāru procents pēc stundām  (%)
plt.figure(figsize=(12, 6))
plt.plot(percent_activity_by_hour.index, percent_activity_by_hour["like_percent"], marker="o", color="orange", label="Patīk (%)")
plt.plot(percent_activity_by_hour.index, percent_activity_by_hour["comment_percent"], marker="o", color="green", label="Komentāri (%)")
plt.title("Vidējais patīk un komentāru procents pēc stundām (%)", fontsize=16)
plt.xlabel("Stunda", fontsize=14)
plt.ylabel("Vidējais procents", fontsize=14)
plt.xticks(ticks=np.arange(0, 24, 1))
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# Vidējais skatījumu skaits pēc stundām
plt.figure(figsize=(12, 6))
plt.plot(activity_by_hour.index, activity_by_hour["views"], marker="o", color="blue", label="Skatījumi")
plt.title("Vidējais skatījumu skaits pēc stundām", fontsize=16) 
plt.xlabel("Stunda", fontsize=14) 
plt.ylabel("Vidējais skatījumu skaits", fontsize=14)  
plt.xticks(ticks=np.arange(0, 24, 1)) 
plt.grid(True)
plt.tight_layout()
plt.show()

# Vidējie patīk un komentāri pēc stundām
plt.figure(figsize=(12, 6))
plt.plot(activity_by_hour.index, activity_by_hour["likes"], marker="o", color="orange", label="Patīk")
plt.plot(activity_by_hour.index, activity_by_hour["comments"], marker="o", color="green", label="Komentāri")
plt.title("Vidējie patīk un komentāri pēc stundām", fontsize=16) 
plt.xlabel("Stunda", fontsize=14) 
plt.ylabel("Vidējais skaits", fontsize=14) 
plt.xticks(ticks=np.arange(0, 24, 1))
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()


# Vidējā iesaiste pēc nedēļas dienām

plt.figure(figsize=(10, 6))
plt.plot(engagement_by_day.index, engagement_by_day, marker="o", color="skyblue", label="Iesaiste (%)")
plt.title("Vidējā iesaiste pēc nedēļas dienām (%)", fontsize=16)
plt.xlabel("Nedēļas diena", fontsize=14)
plt.ylabel("Vidējā iesaiste (%)", fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()


# Vidējā iesaiste pēc kanāla 
engagement_by_channel = engagement_by_channel.sort_values(ascending=False)

plt.figure(figsize=(12, 6))
engagement_by_channel.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Vidējā iesaiste pēc kanāla (%)", fontsize=16) 
plt.xlabel("Kanāls", fontsize=14) 
plt.ylabel("Iesaiste (%)", fontsize=14)  
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
