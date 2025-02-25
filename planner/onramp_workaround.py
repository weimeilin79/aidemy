# Workaround for 
regions = ["us-east1", "us-central1", "us-west4", "us-south1", "us-east5", "us-east4", "us-west1", "europe-west4","europe-north1"]

last_region_used=0
#create a function that looks at the last last_region_used and return the next region from regions, if there no more at the end, move to the begining 
def get_next_region():
    global last_region_used 
    last_region_used = (last_region_used + 1) % len(regions)
    return regions[last_region_used]
