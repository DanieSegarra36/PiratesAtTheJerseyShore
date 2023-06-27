import requests
from bs4 import BeautifulSoup

# List of URLs
JSSeasonLinks = [
  "https://www.mtv.com/shows/jersey-shore/ekx91a/season-1",
  "https://www.mtv.com/shows/jersey-shore/q9phmw/season-2",
  "https://www.mtv.com/shows/jersey-shore/b9nsaq/season-3",
  "https://www.mtv.com/shows/jersey-shore/vq7tvt/season-4",
  "https://www.mtv.com/shows/jersey-shore/kodhqy/season-5",
  "https://www.mtv.com/shows/jersey-shore/c8jfkf/season-6"
]

# File to write the links
output_file = "JSFull.sh"

# Iterate over the URLs
for url in JSSeasonLinks:
  # Send a GET request to the URL
  response = requests.get(url)

  # Create BeautifulSoup object
  soup = BeautifulSoup(response.text, "html.parser")

  # Find the element with classes "module-container" and "video-guide-container"
  element = soup.find("section",
                      class_="has-load-more")
  if element is not None:
    # print(element)
    button = element.select_one(".container>.expand-wrap>button")
    if button is not None:
      print(button)
      button.click()

  # Check if the element has the class "has-load-more"
  # if element is not None:
  #   print("Found section")
  #   if "has-load-more" in element.get("class", []):
  #     while True:
  #       # Find and click the "Show More Episodes" button
  #       button = element.select_one(".container > .expand-wrap > button")
  #       if button is None or button.text.strip() != "Show More Episodes":
  #         break
  #       button.click()

  # Extract the links
  links = []
  episode_list = soup.find("div", id="content-full-episodes-season")
  if episode_list:
    items = episode_list.select("ul > li > a")
    links = [item["href"] for item in items]

  # Write the links to the output file
  with open(output_file, "a") as file:
    # file.write("#!/bin/bash\n\n")
    for link in links:
      file.write(
        f"yt-dlp https://www.mtv.com{link} --concat-playlist always\n")
    file.write("\n")

  # Print the status
  print(f"Processed: {url}")

print("Extraction complete.")
