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

### Flux Image Generation (CometAPI)

Generate images using Flux model via CometAPI's Replicate endpoint:

```bash
python3 test-flux-api.py
```

Features:
- Text-to-image generation via Replicate-compatible endpoint
- Asynchronous with polling
- Configurable dimensions and seed
- URL-based image output

### FLUX.2 Image Generation (BFL Direct API)

Generate images using FLUX.2 models directly from Black Forest Labs:

```bash
export BFL_API_KEY="your-bfl-api-key-here"
python3 test-flux2-bfl-api.py
```

Features:
- FLUX.2 [pro] - Fast production model (~6s generation)
- FLUX.2 [flex] - High quality with adjustable steps and guidance
- Direct BFL API integration
- Photorealistic output with accurate colors (hex code support)
- Configurable dimensions, seed, steps, and guidance

Get your BFL API key from [BFL Dashboard](https://api.bfl.ai/)

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
- `test-flux-api.py` - Flux image generation script (CometAPI)
- `test-flux2-bfl-api.py` - FLUX.2 image generation script (BFL Direct API)
- `test-api-key.py` - API key diagnostic tool
- `config.example.py` - Configuration template
- `config.py` - Your actual config (not committed)

## Output

Generated images are saved as:
- `gemini_text_output.png` - Gemini generated images
- `output.png` - Flux generated images

## API Models

- **Gemini**: `gemini-2.5-flash-image` (CometAPI)
- **Flux**: `flux-dev` (CometAPI via Replicate endpoint)
- **FLUX.2**: `flux-2-pro`, `flux-2-flex` (BFL Direct API)

## License

MIT
