# :sunny: Memory Manager Simulator
This is a memory manager simulator in Python.

## :computer: Requirements

Python3 and pip3.

(opcional) If you want, you can create a virtual environment:

```shell
python3 -m venv env
```

Activate virtual environment:

- Unix/macOS

```shell
source env/bin/activate
```

- Windows

```shell
./env\Script\activate
```

### Install requirements:

```shell
pip3 install -r requirements.txt
```

For install coverage

## :fire: For run it

```shell
python3 main.py
```

## :bulb: How to use it

You have 4 commands:

i. RESERVAR <nombre> <cantidad>
Represents a space reservation of <number> blocks, associated with the identifier <name>.

ii. LIBERAR <nombre>
Represents a release of the space containing the identifier <name>.

iii. MOSTRAR
To show the structure

iv. SALIR
To exit.

## :mag: For run the tests

```shell
cd tests
coverage3 run --source=memory_manager -m unittest test_memory_manager.py
```

#### Coverage of the tests

```shell
coverage3 report -m
```

| Module | Coverage |
|:----:|:--:|
| Memory Manager | 87% |