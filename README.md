# nxcontrol
A python package that provides methods for graph controllability

## Development

1. `git clone https://github.com/chahak13/nxcontrol.git`
2. `cd nxcontrol`
3. `pip install -e .` 

This creates a symlink, so all changes to package are reflected across the system.

TODO:

1. Modularize code, document, register in pip (Last, before presentation)
2. Find driver nodes in karate-club before and after community detection and compare parameters like avg degree, number of drivers etc
3. Implement algo to find all driver nodes. **[MAJOR]**
4. Check if the leaders of the clubs are driver nodes or not
5. Infect from driver nodes inside the community driver nodes. See if the graph comes colored
6. Read paper and implement in karate club **[MAJOR]**
