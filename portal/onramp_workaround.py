# Workaround for 
regions = ["us-east1", "us-central1", "us-west4", "us-south1", "us-east5", "us-east4", "us-west1", "europe-west4","europe-north1"]

regions_thinking = ["us-central1", "us-central1"]

last_region_used=0
last_thinking_region_used=0


def get_next_region():
    global last_region_used 
    last_region_used = (last_region_used + 1) % len(regions)
    return regions[last_region_used]

def get_next_thinking_region():
    global last_thinking_region_used 
    last_thinking_region_used = (last_thinking_region_used + 1) % len(regions_thinking)
    return regions_thinking[last_thinking_region_used]
