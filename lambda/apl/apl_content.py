import json

def apl_main_template(text):
    output = {
    "headlineTemplateData": {
        "type": "object",
        "objectId": "headlineSample",
        "properties": {
            "backgroundImage": {
                "sources": [
                    {
                        "url": "https://www.pixelstalk.net/wp-content/uploads/2016/06/Twitter-Image-HD.jpg",
                        "size": "large"
                    }
                ]
            },
            "textContent": {
                "primaryText": {
                    "type": "PlainText",
                    "text": text,
                    "fontSize": "5dp"
                }
            },
            "logoUrl": "https://trend-hero.s3.amazonaws.com/twitter-512.png",
            "hintText": "Try, \"Alexa, what is the latext tweet from Biden?\""
        }
        }
    }
    
    return output

def _load_apl_document(file_path):
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)    