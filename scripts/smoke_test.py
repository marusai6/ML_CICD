import json
import sys
import urllib.request

def get_json(url):
    with urllib.request.urlopen(url, timeout=8) as response:
        if response.status != 200:
            raise RuntimeError(f"{url} returned {response.status}")
        return json.loads(response.read().decode("utf-8"))

def main(base_url):
    base = base_url.rstrip("/")
    health = get_json(base + "/health")
    ready = get_json(base + "/ready")
    version = get_json(base + "/version")
    if health.get("status") != "ok" or ready.get("status") != "ready":
        raise RuntimeError("health/readiness response is invalid")
    if not version.get("app_version") or not version.get("model_version"):
        raise RuntimeError("version response missing required fields")
    request = urllib.request.Request(
        base + "/predict",
        data=json.dumps({"features": [0, 0, 0, 0, 0]}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        result = json.loads(response.read().decode("utf-8"))
    for key in ("prediction", "probability", "model_version", "request_id"):
        if key not in result:
            raise RuntimeError(f"prediction response missing {key}")
    if result["model_version"] != version["model_version"]:
        raise RuntimeError("model version differs between endpoints")
    print("SMOKE_TEST=PASS health=PASS ready=PASS version=PASS predict=PASS")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/smoke_test.py https://staging.example.com")
    main(sys.argv[1])
  