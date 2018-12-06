# nxcontrol
A python package based on networkx that provides methods for graph controllability

It provides the following:

* Detection of driver nodes according to the Liu et. al model and MDS models of controllability
* Detection of all candidate driver nodes in the Liu et. al model as implemented by Zhang et. al
* Utility functions for random graph generation algorithms notably the G(n,p), G(n,m) and the degree preserving generation.

## Requirements

* Python 3
* networkx graph library

```
pip install networkx
```
Or alternatively

```
pip3 install networkx
```

## Development

```
git clone https://github.com/chahak13/nxcontrol.git
```
Switch to the `nxcontrol` directory
```
cd nxcontrol
```
Now install the package
```
pip install -e .
```
The above command creates a symlink to the nxcontrol repository cloned. This enables the package to be developed. All changes made the the nxcontrol directory are reflected globally.
