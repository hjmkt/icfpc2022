import requests
import json

url = "https://robovinci.xyz/api"

def get_users(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/users", headers=headers)

def post_submission(problem_id, isl_path, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    with open(isl_path, "rb") as f:
        response = requests.post(f"{url}/problems/{problem_id}", headers=headers, files={"file": f})
        submission_id = response.text
    return submission_id

def get_submission(submission_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/submissions/{submission_id}", headers=headers)
    return response.text

def get_results(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/results/user", headers=headers)
    results = json.loads(response.text)
    return results

if __name__ == "__main__":
    import argparse
    import pprint
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str)
    args = parser.parse_args()
    pprint.pprint(get_results(args.token))
