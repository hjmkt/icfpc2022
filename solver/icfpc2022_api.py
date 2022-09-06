import requests
import json

url = "https://robovinci.xyz/api"


def get_users(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/users", headers=headers)
    results = json.loads(response.text)
    return results


def post_submission(problem_id, isl_path, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    with open(isl_path, "rb") as f:
        response = requests.post(
            f"{url}/problems/{problem_id}", headers=headers, files={"file": f}
        )
        submission_id = response.text
    return submission_id


def get_submission(submission_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/submissions/{submission_id}", headers=headers)
    results = json.loads(response.text)
    return results


def get_results(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/results/user", headers=headers)
    results = json.loads(response.text)
    return results


def get_submissions(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.get(f"{url}/submissions", headers=headers)
    results = json.loads(response.text)
    return results


def get_best_submissions(api_token):
    results = get_submissions(args.token)
    submissions = results["submissions"]
    submissions_by_problem = [[] for i in range(40)]
    for submission in submissions:
        submissions_by_problem[submission["problem_id"] - 1].append(submission)
    for problem_submissions in submissions_by_problem:
        problem_submissions.sort(key=lambda x: x["score"])
    for i in range(40):
        submissions_by_problem[i] = submissions_by_problem[i][:1]
    pprint.pprint(submissions_by_problem)


if __name__ == "__main__":
    import argparse
    import pprint

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", type=str)
    args = parser.parse_args()
    results = get_submissions(args.token)
    pprint.pprint(results)
