import requests
import json
from rich import print
from urllib.parse import urlparse
from urllib.parse import parse_qs
import argparse
import re
import datetime

def get_tiktok_response(id):
  url = f"https://vm.tiktok.com/{id}/"
  
  headers = {
    'Host': 'vm.tiktok.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.4 Mobile/15E148 Safari/604.1',
    'Accept-Encoding': 'gzip, deflate, br',
  }

  response = requests.post(url, headers=headers, allow_redirects=False)

  location = response.headers.get("Location")
  parsed_url = urlparse(location)
  parsed_qs = parse_qs(parsed_url.query)

  if (not "user_id" in parsed_qs):
    return False
  
  user_id = parsed_qs['user_id'][0]

  profile_response = requests.get(f"https://tiktok.com/@{user_id}")

  return profile_response.text

def get_instagram_response(shid):
  url = "https://www.instagram.com/graphql/query"

  payload = {
    'fb_api_req_friendly_name': 'PolarisPostActionLoadPostQuerySharerQuery',
    'variables': json.dumps({
      'shid': shid
    }),
    'server_timestamps': 'true',
    'doc_id': '25621259580853638'
  }

  headers = {
    'Host': 'www.instagram.com',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Fb-Friendly-Name': 'PolarisPostActionLoadPostQuerySharerQuery',
    'X-Ig-App-Id': '1217981644879628',
    'Origin': 'https://www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.4 Mobile/15E148 Safari/604.1',
    'X-Csrftoken': 'missing'
  }

  response = requests.post(url, headers=headers, data=payload)

  return json.loads(response.text)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--instagram", help="IGSH value (or URL containing it) for finding an instagram account")
  parser.add_argument("-t", "--tiktok", help="VM value (or URL containing it) for finding a tiktok account")
  args = parser.parse_args()

  if args.instagram:
    igsh = args.instagram
    if (igsh.startswith("https://")):
      igsh = igsh.split("?igsh=")[1]
    print(f"Fetching data for [bold]{igsh}[/bold]...")

    user_response = get_instagram_response(igsh)

    if (user_response.get("message") == "Please wait a few minutes before you try again."):
      print("[bold yellow][!][/bold yellow] You're currently rate-limited. Use another IP or wait a bit.")
      return

    if ("errors" in user_response):
      print("[bold yellow][!][/bold yellow] Errors were found. It's likely that the ID you entered is invalid.")
      return

    user_data = user_response.get("data").get("xdt_get_relationship_for_shid_logged_out")

    if (user_data == None):
      print("[bold red][X][/bold red] No data was found. This ID is probably invalid or has expired.")
      return

    user = user_data.get("sender")

    print("[bold green][+][/bold green] Data was found!")
    print(f":right_arrow: [bold green]Username:[/bold green] {user.get("username")}")
    print(f":right_arrow: [bold green]ID:[/bold green] {user.get("id")}")
    print(f":right_arrow: [bold green]Full name:[/bold green] {user.get("full_name")}")
    print(f":right_arrow: [bold green]Profile URL:[/bold green] https://www.instagram.com/{user.get("username")}/")

    profile_pic_url = user.get("profile_pic_url")
    if profile_pic_url:
      decoded_url = profile_pic_url.encode('utf-8').decode('unicode_escape')
      print(f":right_arrow: [bold green]Profile picture:[/bold green] {decoded_url}")
    else:
      print(":right_arrow: [bold green]Profile picture:[/bold green] No profile picture available")
  elif args.tiktok:
    vm = args.tiktok
    if (vm.endswith("/")):
      vm = vm[:-1]
    if (vm.startswith("https://")):
      vm = vm.split("/")[-1].split("?")[0]
    
    print(f"Fetching data for [bold]{vm}[/bold]...")

    user_response = get_tiktok_response(vm)
    if (not user_response):
      print("[bold red][X][/bold red] No data was found. This ID is probably invalid / expired, or the user has disabled profile suggestions.")
      return

    data = re.findall('"userInfo":{"user":({.*?})', user_response)
    user = json.loads(data[0]  + "}")
    
    print("[bold green][+][/bold green] Data was found!")
    print(f":right_arrow: [bold green]ID:[/bold green] {user.get("id")}")
    print(f":right_arrow: [bold green]Unique ID:[/bold green] {user.get("uniqueId")}")
    print(f":right_arrow: [bold green]Nickname:[/bold green] {user.get("nickname")}")
    print(f":right_arrow: [bold green]Avatar:[/bold green] {user.get("avatarLarger")}")
    print(f":right_arrow: [bold green]Account creation date:[/bold green] {datetime.datetime.fromtimestamp(user.get("createTime"), datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')} GMT")
    print(f":right_arrow: [bold green]Profile URL:[/bold green] https://www.tiktok.com/@{user.get("uniqueId")}/")
  else:
    parser.print_usage()

if __name__ == "__main__":
    main()