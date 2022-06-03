import json

def get_carousel(el):
    carousel = {"type" : "carousel", "elements" : []}
    for element in el:
        carousel["elements"].append({ 
            "photo_id": element[0], 
            "action": { 
                "type": "open_photo" 
            }, 
            "buttons": [{ 
                "action": { 
                    "type": "text", 
                    "label": element[1], 
                    "payload": "{}" 
                } 
            }] 
        })
    carousel = json.dumps(carousel, ensure_ascii = False).encode('utf-8')
    carousel = str(carousel.decode('utf-8'))
    return carousel

carous = get_carousel([
    ["-109837093_457242811", "button_text1"],
    ["-109837093_457242811", "button_text2"],
    ["-109837093_457242811", "button_text3"]
])

input(carous)