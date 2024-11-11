# Browser Agent Red Teaming
This repository will contain multiple **agents**, **red team (jailbreak) data** and **red teaming (jailbreaking) methods**
related with **Browser Agents**.

## Support
### AI Agents
- Claude For Computer Use (from Anthropic)

### Fake Websites
- Browser ART (from Scale AI)

## How to start
### Start Fake Testing Websites
Fake websites to test on.<br>
If you are testing on real websites, skip this part. <br>

Start running website server with the following command.
```bash
python -m http.server -d fake_websites 8000
```

### Start Running Agent

#### Claude for Computer Use
Add Anthropic API Key in .env <br>
This is the official version from Anthropic.
```bash
./claude-for-computer-use/start-agent.sh
```

### Run test data with agent
```bash
python ./claude-for-computer-use/test.py --test "captcha/captcha-1"
```