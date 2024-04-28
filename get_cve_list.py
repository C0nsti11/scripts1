import subprocess
import csv

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
    process = subprocess.run(['searchsploit','--disable-color', '-w', search_term], capture_output=True, text=True, check=True)
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
        if '---' not in line and "Title" not in line:
            # Extract title (between brackets)
            title, url= line.split("| h")
            # print(title.strip(), url.strip())
        # elif line.startswith("php"):
        #     # Extract URL (assuming the first valid URL is the Exploit-DB link)
        #     url = line.strip()
            exploits.append({'title': title.strip(), 'url': "h" + url.strip()})
        

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

if __name__ == "__main__":
  search_term = input("Enter search term for exploits (e.g., 'windows remote code execution'): ")
  exploits = search_exploits(search_term)
  write_exploits_to_csv(exploits, "exploits.csv")
