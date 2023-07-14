# osuExchange

An osu! API wrapper written in Python. Built to give developers a simple and easy-to-use interface to the osu! API.

## Usage

```
pip install osuExchange
```

## Building

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