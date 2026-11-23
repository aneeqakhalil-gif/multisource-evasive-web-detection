import glob, json, re

def parse_decision(data):
    rat = data.get("llm_analysis", {}).get("rationale", "")
    m = re.search(r'\{.*\}', rat, re.DOTALL)
    if m:
        try:
            inner = json.loads(m.group(0))
            return inner.get("is_phishing"), inner.get("rationale", "")
        except Exception:
            pass
    return data.get("is_phishing"), rat

def evaluate_folder(folder):
    files = sorted(glob.glob(f"{folder}/*.json"))
    bypassed = 0
    for fp in files:
        with open(fp) as f:
            data = json.load(f)
        is_phish, _ = parse_decision(data)
        if not is_phish:
            bypassed += 1
    asr = (bypassed / len(files) * 100) if files else 0.0
    print(f"{folder}: ASR = {bypassed}/{len(files)} ({asr:.1f}%)")

if __name__ == "__main__":
    evaluate_folder("results/standard_mode")
    evaluate_folder("results")
