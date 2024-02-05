# cresis_project
Some tools to work with CReSIS data without having to use MATLAB to do the data manipulation.

## A note on code style
Yes, pretty much all of this needs to be rewritten to be less... the way it is. If you
haven't read any of the code yet, maybe consider sticking with that. Right now the 
focus is on figuring out what I need it to do and what components will be 
required to make that happen. Once everything is mostly functional I'll go back 
and clean it up. 

This is very much a work in progress and very early in development. The 
requirements are changing rapidly and the code is changing to match.

## Installation
python dependencies (incomplete list): 
- numpy
- scipy
- matplotlib
- pickle
- basemap
- shapely


## Lessons Learned
- if it says that you need to load mat73, you didn't save the layer file in the OPR tools.
- using a WSL python configuration will break the paths that depend on C: as the root directory

## Data Structure Notes
- segment_ends: List (nesting level = 4)
  - a list of the indices of the endpoints in each segment
  - first index is the crossing point number
  - second index is the leg of the crossing point's X
    - 0 or 1 (first or second leg)
  - third index is the endpoint number 
    - 0 or 1 (start or end)
  - fourth index is the lat/lon pair
    - 0 or 1 (lat or lon)
  - e.g. 
      ```
        # all of the coordinates for all of the endpoints in all of the legs of crossing 0
        segment_ends[0]: [[(-81.11816244525122, -29.73509516444382), (-81.11804305866158, -29.73469645687178)], [(-81.11805932746817, -29.734692394860527), (-81.11802820171967, -29.735538584123283)]]
    
        # all of the coordinates for all of the endpoints in the first leg of crossing 0
        segment_ends[0][0]: [(-81.11816244525122, -29.73509516444382), (-81.11804305866158, -29.73469645687178)]
    
        # the coordinates for the first endpoint in the first leg of crossing 0
        segment_ends[0][0][0]: (-81.11816244525122, -29.73509516444382)
    
        # the latitude of the first endpoint in the first leg of crossing 0
        segment_ends[0][0][0][0]: -81.11816244525122
      ```
  - iceflow_data: List (nesting level = 3*)
    - a list with all of the iceflow data for the continent
    - in a completely different dataset and format so most of it needs convertin
    - first index is the attribute
      - 0:x, 1:y, 2:v_x, 3:v_y, 4:latitude, 5:longitude
      - just setting these equal to variables is probably the easiest way to work with them
    - second index is the x index*
      - for y this is actually the y index
    - third index is the y index
      - x and y do not have a third index
    - e.g.
    - velocity (in x and y) is in meters per year