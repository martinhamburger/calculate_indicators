"""
AI Image Generator

Generate images using AI services like OpenAI DALL-E.
"""

import os
from typing import Optional, List


class AIGenerator:
    """Generate images using AI."""
    
    def __init__(self, api_key: Optional[str] = None, 
                 provider: str = 'openai',
                 model: str = 'dall-e-3'):
        """
        Initialize AI image generator.
        
        Args:
            api_key: API key for the service (can also be set via environment variable)
            provider: AI service provider ('openai' or 'replicate')
            model: Model to use (e.g., 'dall-e-3', 'dall-e-2')
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.provider = provider
        self.model = model
    
    def generate(self, prompt: str, 
                output_path: str,
                size: str = "1024x1024",
                quality: str = "standard",
                style: Optional[str] = None) -> str:
        """
        Generate an image from a text prompt.
        
        Args:
            prompt: Text description of the image to generate
            output_path: Path to save the generated image
            size: Image size ("1024x1024", "1792x1024", "1024x1792" for DALL-E 3)
            quality: Image quality ("standard" or "hd" for DALL-E 3)
            style: Image style ("vivid" or "natural" for DALL-E 3)
            
        Returns:
            Path to the saved image
        """
        if self.provider == 'openai':
            return self._generate_openai(prompt, output_path, size, quality, style)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _generate_openai(self, prompt: str, output_path: str,
                        size: str, quality: str, style: Optional[str]) -> str:
        """Generate image using OpenAI DALL-E."""
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI is required for AI image generation. "
                "Install it with: pip install openai"
            )
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. "
                "Set it via OPENAI_API_KEY environment variable or pass to constructor"
            )
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        client = OpenAI(api_key=self.api_key)
        
        print(f"Generating image with prompt: {prompt}")
        print(f"Model: {self.model}, Size: {size}, Quality: {quality}")
        
        # Prepare generation parameters
        gen_params = {
            "model": self.model,
            "prompt": prompt,
            "n": 1,
        }
        
        # Add parameters based on model
        if self.model == 'dall-e-3':
            gen_params["size"] = size
            gen_params["quality"] = quality
            if style:
                gen_params["style"] = style
        elif self.model == 'dall-e-2':
            # DALL-E 2 supports different sizes
            valid_sizes = ["256x256", "512x512", "1024x1024"]
            if size not in valid_sizes:
                print(f"Warning: Size {size} not supported for DALL-E 2, using 1024x1024")
                size = "1024x1024"
            gen_params["size"] = size
        
        try:
            response = client.images.generate(**gen_params)
            
            image_url = response.data[0].url
            
            # Download and save image
            import requests
            print(f"Downloading image from: {image_url}")
            img_data = requests.get(image_url).content
            
            with open(output_path, 'wb') as f:
                f.write(img_data)
            
            print(f"Image saved to: {output_path}")
            return output_path
            
        except Exception as e:
            raise Exception(f"Error generating image: {e}")
    
    def generate_variations(self, base_image_path: str,
                          output_dir: str,
                          n: int = 3,
                          size: str = "1024x1024") -> List[str]:
        """
        Generate variations of an existing image.
        
        Args:
            base_image_path: Path to the base image
            output_dir: Directory to save variations
            n: Number of variations to generate
            size: Image size
            
        Returns:
            List of paths to generated variations
        """
        if self.provider != 'openai':
            raise ValueError("Image variations only supported for OpenAI")
        
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI is required for AI image generation. "
                "Install it with: pip install openai"
            )
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        os.makedirs(output_dir, exist_ok=True)
        
        client = OpenAI(api_key=self.api_key)
        
        print(f"Generating {n} variations of: {base_image_path}")
        
        with open(base_image_path, 'rb') as image_file:
            response = client.images.create_variation(
                image=image_file,
                n=n,
                size=size
            )
        
        saved_files = []
        for i, image_data in enumerate(response.data):
            image_url = image_data.url
            output_path = os.path.join(output_dir, f"variation_{i+1}.png")
            
            # Download and save
            import requests
            img_data = requests.get(image_url).content
            with open(output_path, 'wb') as f:
                f.write(img_data)
            
            saved_files.append(output_path)
            print(f"Variation {i+1} saved to: {output_path}")
        
        return saved_files
    
    def optimize_prompt(self, prompt: str) -> str:
        """
        Optimize a prompt for better image generation.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Optimized prompt
        """
        # Basic prompt optimization rules
        optimized = prompt.strip()
        
        # Add detail enhancement if prompt is short
        if len(optimized.split()) < 10:
            optimized += ", highly detailed, professional quality"
        
        # Ensure proper grammar
        if not optimized.endswith(('.', '!', '?')):
            optimized += '.'
        
        return optimized


# Command-line usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_generator.py <prompt> [output_file]")
        print("Example: python ai_generator.py 'a beautiful sunset' sunset.png")
        print("\nNote: Requires OPENAI_API_KEY environment variable to be set")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'generated_image.png'
    
    generator = AIGenerator()
    
    # Check if API key is available
    if not generator.api_key:
        print("Error: OPENAI_API_KEY environment variable is not set")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
    
    print(f"Generating image with prompt: {prompt}")
    result = generator.generate(prompt, output_file)
    
    print(f"\nImage generated and saved to: {result}")
