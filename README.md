# Business Analyzer & Meme Generator

This project takes a website URL, analyzes the business behind it, and then generates creative meme concepts based on the business profile.

## How It Works

1. **Business Analysis:**  
   - The project fetches the webpage content.
   - It then extracts key business info (name, industry, offerings, target audience, brand tone) using the Business Analyzer.

2. **Meme Concept Generation:**  
   - The extracted business profile is used to generate meme concepts.
   - Each meme concept includes details like a meme template, captions, hashtags, and visual instructions (defined by the MemeContent model).

3. **Meme Creation (Future):**  
   - The generated meme concepts can be fed into an image generator to create final memes.

## Project Structure

- **app/agents/**  
  - `business_analyzer.py`: Extracts structured business info from a URL.
  - `meme_template_generator.py`: Generates meme concepts based on the business profile.

- **app/models/**  
  - `business_profile.py`: Defines the business profile structure.
  - `meme_content.py`: Defines the meme content and campaign structures.

## Quick Start

1. **Setup**  
   - Install dependencies listed in `requirements.txt`.

2. **Run the Business Analyzer**  
   - Provide a URL to extract the business profile.

3. **Generate Meme Concepts**  
   - Use the generated business profile to create meme concepts.

This repository aims to build a quick pipeline from understanding a business website to generating creative marketing memes.