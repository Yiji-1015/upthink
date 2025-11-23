"""LLM client for Upstage API interaction including Information Extraction."""
import base64
import json
import httpx
from typing import List, Optional, Dict, Any
from pathlib import Path
from ..config import Config
from ..models import DescriptionTemplate


class UpstageClient:
    """Client for interacting with Upstage Solar API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.UPSTAGE_API_KEY
        self.api_base = api_base or Config.UPSTAGE_API_BASE
        self.model = model or Config.MODEL_NAME

        if not self.api_key:
            raise ValueError("UPSTAGE_API_KEY is required")

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def make_request_sync(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None
    ) -> Optional[str]:
        """Make a synchronous request to the Upstage API."""
        temperature = temperature or Config.DEFAULT_TEMPERATURE
        max_tokens = max_tokens or Config.DEFAULT_MAX_TOKENS

        url = f"{self.api_base}/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            with httpx.Client(timeout=Config.HTTP_TIMEOUT_SYNC) as client:
                response = client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error making request: {e}")
            return None

    def extract_information(
        self,
        document_path: Path,
        description: str
    ) -> Optional[Dict[str, Any]]:
        """Extract information from a document using Upstage Information Extraction API.

        Args:
            document_path: Path to the document file (docx)
            description: Description of what to extract with response format

        Returns:
            Extracted information as dictionary or None on error
        """
        try:
            # Read and encode document
            with open(document_path, 'rb') as f:
                document_data = base64.standard_b64encode(f.read()).decode('utf-8')

            url = Config.UPSTAGE_IE_API_BASE

            # Prepare multipart form data
            files = {
                'document': ('document.docx', open(document_path, 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            }
            data = {
                'model': 'information-extract',
                'schema': description
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }

            with httpx.Client(timeout=Config.HTTP_TIMEOUT_SYNC) as client:
                response = client.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data
                )
                response.raise_for_status()
                result = response.json()

                # Parse the extraction result
                if 'extraction' in result:
                    return result['extraction']
                elif 'choices' in result and result['choices']:
                    content = result['choices'][0].get('message', {}).get('content', '')
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        return {'raw': content}
                return result

        except httpx.HTTPStatusError as e:
            print(f"HTTP error during information extraction: {e}")
            print(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            return None
        except Exception as e:
            print(f"Error during information extraction: {e}")
            return None
        finally:
            # Close the file if it was opened
            if 'files' in locals() and files.get('document'):
                files['document'][1].close()

    def generate_freshness_guide(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3
    ) -> Optional[str]:
        """Generate freshness guide using Solar model.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt with context
            temperature: Lower temperature for more focused output

        Returns:
            Generated guide content or None on error
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return self.make_request_sync(messages, temperature=temperature)
