import subprocess
import csv
import pathlib

def search_exploits(search_term):
  """
  Executes searchsploit with the given search term, parses the output,
  and returns a list of dictionaries containing exploit titles and URLs.

  Args:
      search_term: The term to search for in Exploit-DB.

  Returns:
      A list of dictionaries, where each dictionary contains keys:
          'title': The exploit title.
          'url': The URL to the exploit on Exploit-DB.
  """
  exploits = []
  try:
    # Execute searchsploit command and capture output
    process = subprocess.run(['searchsploit','--disable-color' ,search_term], capture_output=True, text=True, check=True)
    # print(process)
    output = process.stdout.strip()
    # print(output)

    if not output:
      print(f"No exploits found for search term: {search_term}")
      return exploits

    # Split output into lines, handle potential leading/trailing spaces
    lines = output.splitlines()
    lines = [line.strip() for line in lines]
    
    # Iterate over lines, extract title and URL for each exploit
    for line in lines:
        # print(line)
        if '---' not in line and "Title" not in line and "|" in line:
            # Extract title (between brackets)
            if "https" in line:
              title, url= line.split("| h")
              url = "h" + url
            else:
              # print(line)
              title, url= line.split("|")
            # print(title.strip(), url.strip())
        # elif line.startswith("php"):
        #     # Extract URL (assuming the first valid URL is the Exploit-DB link)
        #     url = line.strip()
            exploits.append({'title': title.strip(), 'url': url.strip()})
        

  except subprocess.CalledProcessError as e:
    print(f"Error running searchsploit: {e}")

  return exploits

def write_exploits_to_csv(exploits, filename):
  """
  Writes a list of exploits (dictionaries) to a CSV file.

  Args:
      exploits: A list of dictionaries containing exploit data.
      filename: The name of the CSV file to write to.
  """
  if not exploits:
    print("No exploits found to write to CSV.")
    return

  try:
    with open(filename, 'w', newline='') as csvfile:
      fieldnames = ['Exploit Title', 'URL']
      writer = csv.DictWriter(csvfile, fieldnames=['title', 'url'])
      writer.writeheader()
      writer.writerows(exploits)
      print(f"Exploits written to CSV file: {filename}")

  except OSError as e:
    print(f"Error writing exploits to CSV: {e}")
    

def rename_files(exploits, dirpath):
  # 
  dirpath=pathlib.Path(dirpath)
  for entry in dirpath.iterdir():
    if entry.is_file():  # Check if it's actually a file
      for i in exploits:
        # Consider exact filename matching (including extension)
        if entry.name == i["url"].split("/")[-1]:  # Assuming URL is the filename
          new_name = i["title"].replace(" ", "_") + "_" + \
                      "".join([i['url'].split("/")[2] if len(i["url"].split("/")) > 2 else i['url'].split("/")[1]])
          new_name = new_name.replace("/","_")
          new_name = new_name.replace("$","_")
          new_name = new_name.replace("&","_")
          new_name = new_name.replace("?","_")
          new_name = new_name.replace("\"","_")
          new_name = new_name.replace("*","_")
          print(f"Renaming {entry} to {new_name}")
          try:
            entry.rename(entry.parent / new_name)
          except FileNotFoundError:
            print(f"Error: File not found: {entry}")
            # Handle missing file gracefully (e.g., log or skip)

def download_list(exploits, dir_path):
  import requests
 
  if not any(pathlib.Path(dir_path).iterdir()):
    url_list = [u['url'].split("/")[2].split(".")[0] if len(u["url"].split("/")) >2 else u['url'].split("/")[1].split(".")[0] for u in exploits]
    # print([u['url'] for u in exploits])
    # print(len(url_list))
    # print(len(set(url_list)))
    for url in set(url_list):
      subprocess.run(['searchsploit','--disable-color', "-m" ,url], cwd=dir_path, check=False)
  
  return 0
  for u in exploits:
    if "https" in u['url']:
      url = u['url'].replace("exploits", "download")
      requests.get(url)
    else:
      url = u['url'].split("/")
      url = url[2].split(".")
      # process1 = subprocess.run(['cd', dir_path], check=True)
      # subprocess.call('cd {}'.format(dir_path), shell=True)
      subprocess.run(['searchsploit','--disable-color', "-m" ,url[0]], cwd=dir_path, check=False)
      
    # print(u['url'])
    # break
    # requests.get(u.url)

if __name__ == "__main__":
  # search_term = input("Enter search term for exploits (e.g., 'windows remote code execution'): ")
  search_term = ".NET remote code"
  dir_path = search_term.replace(" ", "_")
  exploits = search_exploits(search_term)
  pathlib.Path(dir_path).mkdir(exist_ok=True)
  download_list(exploits, dir_path)
  rename_files(exploits, dir_path)
  # write_exploits_to_csv(exploits, "{}.csv".format(search_term))
