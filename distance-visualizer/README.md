# Visual RSE Mappings
### The first script gets the distances between all the rucio storage elements then sort them into the respective data facilities then generate a `Mapping.png` file.
### The second script takes the `Mapping.png` file and converts it into a printable visual in the terminal.

To get the mappings and generate the Mapping.png file run:

    python3 rse_distance_mapper.py

To visualize in the console run:

    python3 img_viewer.py Mapping.png
