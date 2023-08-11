# osuExchange

![osuExchange Logo](logo.png)

An osu! API wrapper written in Python. Built to give developers a simple and easy-to-use interface to the osu! API.

## Usage

```
pip install osuExchange
```

## Building

Install necessary packages:

```
pip install build
```

Run this command inside of the osuExchange environment:

```
python -m build
```

Inside testing environment

Create the virtual environment first:

```
python -m venv .
```

Enter the virtual environment:

- On Windows: `Scripts\activate`
- On Linux: `sh Scripts/activate`


Finally build the package:

```
python setup.py bdist_wheel
```