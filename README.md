# CometAPI Image Generation Scripts

Python scripts for testing image generation with Flux and Gemini models via CometAPI.

## Setup

1. **Install dependencies**:
   ```bash
   pip install requests
   ```

2. **Configure API key**:
   ```bash
   cp config.example.py config.py
   ```
   Then edit `config.py` and add your CometAPI key.

3. **Get your API key**:
   - Sign up at [CometAPI](https://cometapi.com)
   - Get your API key from the dashboard

## Usage

### Shell Script (Flux)

For quick testing with curl:

```bash
# Set your API key
export COMETAPI_KEY="your-api-key-here"

# Or use .env file
cp .env.example .env
# Edit .env with your key, then:
source .env

# Run the script
./flux2-comet-api-script.sh
```

### Gemini 2.5 Flash Image Generation

Generate images using Google's Gemini model:

```bash
python3 test-gemini-image-api.py
```

Features:
- Text-to-image generation
- Synchronous response (no polling)
- Configurable aspect ratios (1:1, 16:9, etc.)
- Base64 image output

### Flux Image Generation

Generate images using Flux model:

```bash
python3 test-flux-api.py
```

Features:
- Text-to-image generation
- Asynchronous with polling
- Configurable dimensions and seed
- URL-based image output

## Documentation

- `gemini-image-cometapi-guide.md` - Comprehensive guide for Gemini image generation
- `flux-cometapi-guide.md` - Guide for Flux API usage
- `flux2-api-guide.md` - Additional Flux API documentation

## Security

⚠️ **Important**: Never commit your `config.py` file with your API key!

The `.gitignore` file is configured to exclude:
- `config.py` (contains your API key)
- Generated images
- Python cache files

## Files

- `test-gemini-image-api.py` - Gemini image generation script
- `test-flux-api.py` - Flux image generation script
- `config.example.py` - Configuration template
- `config.py` - Your actual config (not committed)

## Output

Generated images are saved as:
- `gemini_text_output.png` - Gemini generated images
- `output.png` - Flux generated images

## API Models

- **Gemini**: `gemini-2.5-flash-image`
- **Flux**: `flux-dev`

## License

MIT
