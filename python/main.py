import io
from fastapi import Response, HTTPException, Query, Request
from datetime import datetime, timezone
import requests
import os
from typing import Annotated
import modal
 

def download_model():
    from diffusers import AutoPipelineForText2Image
    import torch

    AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", 
                                                     torch_dtype=torch.float16, 
                                                     variant="fp16")
    
    
image = (modal.Image.debian_slim()
         .pip_install("fastapi[standard]","transformers","accelerate","diffusers","requests")
         .run_function(download_model))


app = modal.App("pentagram",image=image)

@app.cls(
    image=image,
    gpu="A10G",
    container_idle_timeout=300,  # 5 min
    secrets=[modal.Secret.from_name("API_KEY")]    
)

class Model:
    
    @modal.build()
    @modal.enter()
    def load_weights(self):
        from diffusers import AutoPipelineForText2Image
        import torch
        
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo",
            torh_dtype=torch.float16,
            variant="fp16"
        )
        
        self.pipe.to("cuda")
        
        self.API_KEY = os.environ["API_KEY"]
        
        
        
    @modal.web_endpoint()
    def generate(self,
                 request: Request, 
                 prompt : str = Query(..., description="The text prompt to generate the image from")):
        
        
        api_key = request.headers.get("X_API_KEY")
        if api_key != self.API_KEY:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )
        
        
        image = self.pipe(prompt, num_inference_steps = 1, guidance_scale = 0.0).images[0]
        
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        
        return Response(content=buffer.getvalue(), media_type="image/jpeg")        
    
    
    @modal.web_endpoint()
    def health(self):
        """"
        Health check endpoint
        """
        return {"status": "Healthy", "timestamp": datetime.now(timezone.utc).isoformat()}
        
        
@app.function(
    schedule=modal.Cron("*/5 * * * *"),
    secrets=[modal.Secret.from_name("API_KEY")]
)

def keep_warm():
    health_url = "HEALTH-URL-HERE.modal.run"
    generate_url = "GENERATE-URL-HERE.modal.run"

    health_response = requests.get(health_url)
    print(f"healthCheck at {health_response.json()['timestamp']}")
    
    headers = {"X_API_KEY": os.environ["API_KEY"]}    
    
    generate_response = requests.get(generate_url, headers=headers)
    
    print(f"generate endpoint tested successfully at : {datetime.now(timezone.utc).isoformat()}")
    
    
    